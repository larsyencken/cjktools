# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# niceThread.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Feb  2 14:02:41 EST 2006
#
#----------------------------------------------------------------------------#

""" Support for automagically threading a call to map so that each thread 
    applied the method to part of the sequence input to map.
    
    XXX Did this before I understood Python's global interpreter lock
    prevented threads from running on more than one cpu at once. Not useful
    in its current state.
"""

#----------------------------------------------------------------------------#

import threading

#----------------------------------------------------------------------------#

class MapThreadPool:
    def __init__(self, nThreads):
        """ Create n threads for threadedMap and keep them around.
        """
        self._nThreads = nThreads
        self._pool = []
        for i in range(nThreads):
            self._pool.append(MapThread())

        self._usageLock = threading.Lock()

        return

    def _divideInput(self, inputList):
        """ Divides the input into equitable portions for each thread.
        """
        inputList = list(inputList)
        threadInputSize, remainder = divmod(len(inputList), self._nThreads)
    
        # divide the input into chunks for the threads
        threadInputs = []
    
        start = end = 0
        for i in xrange(self._nThreads):
            end += threadInputSize
    
            # distribute the remainder
            if i < remainder:
                end += 1
                
            threadInputs.append(inputList[start:end])
            start = end

        return threadInputs

    def map(self, method, args):
        """ Performs the same as map, but using the thread pool created.
        """
        threadInputs = self._divideInput(args)

        resultList = []
        self._usageLock.acquire()

        # set off the threads
        for thread, threadInput in zip(self._pool, threadInputs):
            thread.setup(method, threadInput)
            thread.start()

        # fetch their results
        for thread in self._pool:
            thread.join()
            resultList.extend(thread.results())

        self._usageLock.release()

        return resultList

#----------------------------------------------------------------------------#

class MapThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._method = None
        self._args = None
        self._result = None
        self._varLock = threading.Lock()
        return

    def setup(self, method, args):
        self._varLock.acquire()
        self._method = method
        self._args = args
        self._varLock.release()
        return

    def run(self):
        self._varLock.acquire()
        if self._method is None or self._args is None:
            raise Exception, "Thread run before setup"

        self._result = map(self._method, self._args)
        self._varLock.release()
        return
    
    def results(self):
        return self._result

#----------------------------------------------------------------------------#
