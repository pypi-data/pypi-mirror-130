#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"

import os
import time
import pprint
import datetime
import traceback
import importlib
import multiprocessing
import multiprocessing.pool

from pypushflow.AbstractActor import AbstractActor
from pypushflow.logutils import PyPushflowLoggedObject


#############################################################################
# Create no daemon processes
# See : https://stackoverflow.com/a/53180921
#


class NoDaemonProcess(multiprocessing.Process):
    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    Process = NoDaemonProcess


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class Edna2Pool(multiprocessing.pool.Pool):
    def __init__(self, *args, **kwargs):
        kwargs["context"] = NoDaemonContext()
        super().__init__(*args, **kwargs)


#
#
#############################################################################


class AsyncFactory(PyPushflowLoggedObject):
    def __init__(self, func, callback=None, errorCallback=None, parent=None):
        super().__init__(parent=parent)
        self.func = func
        self.callback = callback
        self.errorCallback = errorCallback
        self.pool = Edna2Pool(1)

    def call(self, *args, **kwargs):
        self.logger.debug(
            "asynchronous execution of '%s.%s'",
            self.func.__module__,
            self.func.__name__,
        )
        self.pool.apply_async(
            self.func,
            args=args,
            kwds=kwargs,
            callback=self.callback,
            error_callback=self.errorCallback,
        )
        self.pool.close()


class PythonActor(AbstractActor):
    def __init__(
        self, parent=None, name="Python Actor", errorHandler=None, script=None, **kw
    ):
        super().__init__(parent=parent, name=name, **kw)
        self.parentErrorHandler = errorHandler
        self.listErrorHandler = []
        self.script = script
        self.inData = None
        self.af = None

    def connectOnError(self, actor):
        self.logger.debug("connect to error handler '%s'", actor.name)
        self.listErrorHandler.append(actor)

    def trigger(self, inData: dict):
        self.logger.info("triggered with inData =\n %s", pprint.pformat(inData))
        self.setStarted()
        self.inData = dict(inData)
        self.uploadInDataToMongo(actorData={"inData": inData}, script=self.script)

        try:
            module = importlib.import_module(os.path.splitext(self.script)[0])
        except Exception as e:
            self.logger.error("Error when trying to import script '%s'", self.script)
            time.sleep(1)
            self.errorHandler(e)
            return

        with self._postpone_end_thread(self.resultHandler, self.errorHandler) as (
            resultHandler,
            errorHandler,
        ):
            self.af = AsyncFactory(
                module.run,
                callback=resultHandler,
                errorCallback=errorHandler,
                parent=self,
            )
            self.af.call(**self.inData)

    def resultHandler(self, result: dict):
        """Async callback in case of success"""
        try:
            # Handle the result
            self._finishedSuccess(result)

            # Trigger actors
            downstreamData = dict(self.inData)
            downstreamData.update(result)
            self._triggerDownStreamActors(downstreamData)
        except Exception as e:
            self.errorHandler(e)

    def errorHandler(self, exception: Exception):
        """Async callback in case of exception"""
        try:
            # Handle the result
            self._logException(exception)
            result = self._parseException(exception)
            self._finishedFailure(result)

            # Trigger actors
            downstreamData = dict(self.inData)
            downstreamData["WorkflowException"] = result
            self._triggerErrorHandlers(downstreamData)
        except Exception:
            self.logger.exception("In errorHandler for '%s'", self.name)

    def _logException(self, exception: Exception) -> None:
        if isinstance(exception.__cause__, multiprocessing.pool.RemoteTraceback):
            exception = exception.__cause__
            logfunc = self.logger.error
        elif isinstance(exception, multiprocessing.pool.MaybeEncodingError):
            # This exception has no traceback
            logfunc = self.logger.error
        else:
            logfunc = self.logger.exception
        logfunc(
            "Error in python actor '%s'!\n Not running down stream actors %s\n Exception:%s",
            self.name,
            [actor.name for actor in self.listDownStreamActor],
            exception,
        )

    def _parseException(self, exception: Exception) -> dict:
        errorMessage = str(exception)
        if isinstance(exception.__cause__, multiprocessing.pool.RemoteTraceback):
            exception = exception.__cause__
        traceBack = traceback.format_exception(
            type(exception), exception, exception.__traceback__
        )
        return {
            "errorMessage": errorMessage,
            "traceBack": traceBack,
        }

    def _triggerDownStreamActors(self, downstreamData: dict):
        for downStreamActor in self.listDownStreamActor:
            self.logger.debug(
                "trigger actor '%s' with inData =\n %s",
                downStreamActor.name,
                pprint.pformat(downstreamData),
            )
            downStreamActor.trigger(downstreamData)

    def _triggerErrorHandlers(self, downstreamData: dict):
        for errorHandler in self.listErrorHandler:
            errorHandler.trigger(downstreamData)
        if self.parentErrorHandler is not None:
            self.parentErrorHandler.triggerOnError(inData=downstreamData)

    def _finishedSuccess(self, result: dict):
        self.setFinished()
        self.uploadOutDataToMongo(
            actorData={
                "stopTime": datetime.datetime.now(),
                "status": "finished",
                "outData": result,
            }
        )
        if "workflowLogFile" in result:
            self.setMongoAttribute("logFile", result["workflowLogFile"])
        if "workflowDebugLogFile" in result:
            self.setMongoAttribute("debugLogFile", result["workflowDebugLogFile"])

    def _finishedFailure(self, result: dict):
        self.setFinished()
        self.uploadOutDataToMongo(
            actorData={
                "stopTime": datetime.datetime.now(),
                "status": "error",
                "outData": result,
            }
        )
