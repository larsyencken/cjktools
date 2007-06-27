#----------------------------------------------------------------------------#
# progressBar.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Feb 10 12:25:51 EST 2005
#
#----------------------------------------------------------------------------#

""" A simple console progress bar, with support for *nice* features like
    one-call wrapping around iterators.
"""

#----------------------------------------------------------------------------#

import shellColor
import sys
import time

import common

#----------------------------------------------------------------------------#

_currentBar = None

def withProgress(iterator, modValue=1, size=None):
    """ A wrapper for a sized iterator which adds a progress bar.
    """
    global _currentBar

    progress = ProgressBar()
    if size is not None:
        progress.start(size)
    else:
        progress.start(len(iterator))

    _currentBar = progress

    count = 0
    for item in iterator:
        yield item
        count += 1
        if count % modValue == 0:
            progress.update(count)

    progress.finish()

    _currentBar = None
    return

#----------------------------------------------------------------------------#

def tick():
    global _currentBar

    if _currentBar is not None:
        _currentBar.tick()
    return

#----------------------------------------------------------------------------#

class ProgressBar:
    """ A progress bar which gets printed to stdout.
    """
    def __init__(self, stringSize=20):
        """ Creates a new instance, setting the size as needed.
        """
        self._stringSize = stringSize
        self._count = 0
        self._totalCount = None
        self._lastLineSize = None
        self._lastRotation = 0
        self._startTime = None

        self._rotation = ['/', '-', '\\', '|']
        self._numRotations = len(self._rotation)

        return

    def reset(self):
        """ Resets the progress bar to initial conditions.
        """
        self._count = 0
        self._totalCount = None
        self._lastLineSize = None
        self._lastRotation = 0
        self._startTime = None

        return
    
    def start(self, totalCount):
        """ Starts the progress bar. This will be the first output from the
            bar. At this stage it needs the total count so that it can
            calculate percentages.

            @param totalCount: The count which represents 'finished'.
        """
        assert self._count == 0, "Progress bar already started, call reset()"
        assert totalCount > 0, "Progress bar needs a non-zero total count"
        self._totalCount = totalCount
        progressLine = '[' + shellColor.color('/', 'red') + \
                (self._stringSize-1)*' ' + ']   0%'
        sys.stdout.write(progressLine)
        sys.stdout.flush()
        self._lastLineSize = shellColor.realLen(progressLine)

        self._startTime = time.time()

        return

    def update(self, count):
        """ Updates the progress bar with the current count. This is useful
            to call even if the count has not increased, since it provides
            visual feedback to the user that the process is active.

            @param count: The current count
        """
        count = int(count)
        self._count = count
        if count < 0 or count > self._totalCount:
            raise Exception, 'Bad count for progress bar'

        n = (count * self._stringSize) / self._totalCount
        percent = (100*count) / self._totalCount
        m = self._stringSize - n - 1 # subtract one for the rotating char

        self._lastRotation = (self._lastRotation + 1) % self._numRotations
        if percent < 100:
            rotChar = self._rotation[self._lastRotation]
        else:
            rotChar = ''

        progressLine = '[' + shellColor.color(n*'-' + rotChar, 'red') + \
                m*' ' + '] ' + str('%3d%%' % percent)
        sys.stdout.write('\b'*(self._lastLineSize))
        sys.stdout.write(progressLine)
        sys.stdout.flush()
        self._lastLineSize = shellColor.realLen(progressLine)

        return

    def tick(self):
        """ Perform a quick update.
        """
        self.update(self._count)
        return

    def fractional(self, fraction):
        """ Set a fractional percentage completion, e.g. 0.3333 -> 33%.
        """
        assert fraction >= 0 and fraction <= 1
        self.update(int(fraction * self._totalCount))

        return
    
    def finish(self):
        """ Fixes to 100% complete, and writes the time taken.
        """
        assert self._totalCount > 0, "Progress bar wasn't initialised"
        self.update(self._totalCount)

        timeTaken = int(time.time() - self._startTime)
        (mins, secs) = divmod(timeTaken, 60)
        if not mins:
            timeString = ' (%ds)\n' % secs
        else:
            (hours, mins) = divmod(mins, 60)
            if not hours:
                timeString = ' (%dm %ds)\n' % (mins, secs)
            else:
                timeString = ' (%dh %dm %ds)\n' % (hours, mins, secs)

        sys.stdout.write(timeString)

        # precautionary, in case finish() is called more than once
        self._lastLineSize += len(timeString)

        return

#----------------------------------------------------------------------------#

def linesWithProgress(filename, encoding='utf8', modValue=None):
    """ A progress bar over the lines in an uncompressed file.
    """
    # We can't provide progress in these cases.
    if filename.endswith('.gz') or filename.endswith('.bz2'):
        iStream = common.sopen(filename, 'r', encoding)
        for line in iStream:
            yield line
        iStream.close()
        return

    fileSize = os.stat(filename).st_size
    offset = 0
    iStream = common.sopen(filename, 'r', encoding)
    progress = progressBar.ProgressBar()
    progress.start(fileSize)
    n = 0
    for line in iStream:
        yield line
        offset += len(line)
        n += 1

        if not modValue or n % modValue == 0:
            progress.update(offset)

    iStream.close()
    progress.finish()
    return

#----------------------------------------------------------------------------#

