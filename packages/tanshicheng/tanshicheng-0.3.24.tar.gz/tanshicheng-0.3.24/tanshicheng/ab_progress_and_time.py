import time
import datetime
import sys


class ProgressOut:
    def __init__(self):
        self._isStart = False
        self._startTime = None
        self._timeTrack = [time.time()]
        self._startOut = False
        self._outputTimes = 0

    def _timeTransformation(self, seconds):
        if seconds < 60:
            return '%.2fs' % seconds
        elif seconds < 60 ** 2:
            return '%.2fm' % (seconds / 60)
        elif seconds < 60 ** 2 * 100:
            return '%.2fh' % (seconds / 60 / 60)
        else:
            return '%.2fd' % (seconds / 60 / 60 / 24)

    def start(self, outCurrent=False, text=''):
        self._timeTrack.append(time.time())
        self._startTime = self._timeTrack[-1]
        self._startOut = False
        self._outputTimes = 0
        self._isStart = True

        if outCurrent:
            print(text + str(datetime.datetime.now()))
        return self

    def output(self, text: str = '', outTime=True, sumTimes=None, outSpeed=False, outCurrent=False):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        self._startOut = True

        outText = text
        if outTime:
            outText += '\tTime consuming: %s(all: %s).' % (
            self._timeTransformation(self._timeTrack[-1] - self._timeTrack[-2]),
            self._timeTransformation(self._timeTrack[-1] - self._startTime))
        if outSpeed and self._outputTimes > 0:
            speedT = (self._timeTrack[-1] - self._startTime) / self._outputTimes
            outText += ' Speed: %s/times.' % (self._timeTransformation(speedT))
        if sumTimes != None and self._outputTimes > 0:
            remaining = (self._timeTrack[-1] - self._startTime) * sumTimes / self._outputTimes - (
                        self._timeTrack[-1] - self._startTime)
            outText += ' Time remaining: %s.' % (self._timeTransformation(remaining))
        if outCurrent:
            outText += ' ' + str(datetime.datetime.now())

        if outText == None or len(outText.strip()) == 0:
            return

        sys.stdout.write('\r')
        print(outText, end='')
        sys.stdout.flush()

        self._outputTimes += 1

    def end(self, text='', saveText=False, outCurrent=False, outTime=True):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        if self._startOut:
            if saveText:
                print()
            else:
                sys.stdout.write('\r')
            self._isStart = False

        outText = text
        if outTime:
            outText += '\tTime consuming: %s.' % (self._timeTransformation(self._timeTrack[-1] - self._startTime))
        if outCurrent:
            outText += ' ' + str(datetime.datetime.now())

        if outText != None and len(outText.strip()) > 0:
            print(outText)
        sys.stdout.flush()

    def addOutputTimes(self, times=1):
        if not self._isStart:
            return
        self._outputTimes += times


class ProgressOut2:
    def __init__(self):
        self._isStart = False
        self._startTime = None
        self._timeTrack = [time.time()]
        self._startOut = False
        self._outputTimes = 0
        self._sumTimes = None

    def _timeTransformation(self, seconds):
        if seconds < 60:
            return '%.2fs' % seconds
        elif seconds < 60 ** 2:
            return '%.2fm' % (seconds / 60)
        elif seconds < 60 ** 2 * 100:
            return '%.2fh' % (seconds / 60 / 60)
        else:
            return '%.2fd' % (seconds / 60 / 60 / 24)

    def start(self, text='', sumTimes=None):
        self._timeTrack.append(time.time())
        self._startTime = self._timeTrack[-1]
        self._startOut = False
        self._outputTimes = 0
        self._isStart = True
        self._sumTimes = sumTimes

        if text != None and len(text) > 0:
            print(text)
        return self

    def output(self, text='', sumTimes=None):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        if sumTimes != None:
            self._sumTimes = sumTimes

        outText = text
        # outTime:
        outText += '\t[Time: %s(%s)' % (self._timeTransformation(self._timeTrack[-1] - self._startTime),
                                        self._timeTransformation(self._timeTrack[-1] - self._timeTrack[-2]))
        # sumTimes:
        if self._sumTimes != None and self._outputTimes > 0:
            remaining = (self._timeTrack[-1] - self._startTime) * self._sumTimes / self._outputTimes - (
                    self._timeTrack[-1] - self._startTime)
            outText += '+%s' % (self._timeTransformation(remaining))
        # outSpeed:
        if self._outputTimes > 0:
            speedT = (self._timeTrack[-1] - self._startTime) / self._outputTimes
            outText += ', %s/times(%d)' % (self._timeTransformation(speedT), self._outputTimes)
        # outCurrent:
        currentTime = str(datetime.datetime.now())
        currentTime = currentTime.split('.')[0].split('-', 1)[1]
        outText += ', ' + currentTime + ']'

        sys.stdout.write('\r')
        print(outText, end='')
        sys.stdout.flush()

        self.addOutputTimes()
        self._startOut = True

    def end(self, text='', saveText=False):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        if self._startOut:
            if saveText:
                print()
            else:
                sys.stdout.write('\r')
            self._isStart = False
            self._startOut = False

        outText = text
        # outTime:
        outText += '\t[Time consuming: %s' % (self._timeTransformation(self._timeTrack[-1] - self._startTime))
        # outCurrent:
        currentTime = str(datetime.datetime.now())
        currentTime = currentTime.split('.')[0].split('-', 1)[1]
        outText += ', ' + currentTime + ']'

        if outText != None and len(outText.strip()) > 0:
            print(outText)
        sys.stdout.flush()

    def addOutputTimes(self, times=1):
        if not self._isStart:
            return
        self._outputTimes += times

    @staticmethod
    def outputCurrent():
        print('Current time: ' + str(datetime.datetime.now()))

    @staticmethod
    def flush():
        sys.stdout.flush()


class ProgressOut3:
    Desc = None

    def __init__(self, iterable, desc='', total=None, leave=True, mininterval=0.1):
        try:
            total = len(iterable)
        except:
            ...

        self._iterable = iterable
        self._desc = str(desc)
        self._total = total
        self._leave = leave
        self._mininterval = mininterval

        self._isStart = False
        self._startTime = None
        self._timeTrack = [time.time()]
        self._startOut = False
        self._outputTimes = 0
        self._sumTimes = None

    def _timeTransformation(self, seconds):
        if seconds < 60:
            return '%.2fs' % seconds
        elif seconds < 60 ** 2:
            return '%.2fm' % (seconds / 60)
        elif seconds < 60 ** 2 * 100:
            return '%.2fh' % (seconds / 60 / 60)
        else:
            return '%.2fd' % (seconds / 60 / 60 / 24)

    def _start(self, text='', sumTimes=None):
        self._timeTrack.append(time.time())
        self._startTime = self._timeTrack[-1]
        self._startOut = False
        self._outputTimes = 0
        self._isStart = True
        self._sumTimes = sumTimes
        ProgressOut3.Desc = None

        if text != None and len(text) > 0:
            print(text)
        return self

    def _output(self, text='', sumTimes=None):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        if sumTimes != None:
            self._sumTimes = sumTimes

        if self._timeTrack[-1] - self._timeTrack[-2] >= self._mininterval:
            outText = text
            # outTime:
            outText += '\t[Time: %s(%s)' % (self._timeTransformation(self._timeTrack[-1] - self._startTime),
                                            self._timeTransformation(self._timeTrack[-1] - self._timeTrack[-2]))
            # sumTimes:
            if self._sumTimes != None and self._outputTimes > 0:
                remaining = (self._timeTrack[-1] - self._startTime) * self._sumTimes / self._outputTimes - (
                        self._timeTrack[-1] - self._startTime)
                outText += '+%s' % (self._timeTransformation(remaining))
            # outSpeed:
            if self._outputTimes > 0:
                speedT = (self._timeTrack[-1] - self._startTime) / self._outputTimes
                outText += ', %s/times(%d)' % (self._timeTransformation(speedT), self._outputTimes)
            # outCurrent:
            currentTime = str(datetime.datetime.now())
            currentTime = currentTime.split('.')[0].split('-', 1)[1]
            outText += ', ' + currentTime + ']'

            sys.stdout.write('\r')
            print(outText, end='')
            sys.stdout.flush()

        self.addOutputTimes()
        self._startOut = True

    def _end(self, text='', saveText=False):
        if not self._isStart:
            return
        self._timeTrack.append(time.time())
        if self._startOut:
            sys.stdout.write('\r')
            self._isStart = False
            self._startOut = False

        outText = text
        # outTime:
        outText += '\t[Time consuming: %s' % (self._timeTransformation(self._timeTrack[-1] - self._startTime))
        # outSpeed:
        if self._outputTimes > 0:
            speedT = (self._timeTrack[-1] - self._startTime) / self._outputTimes
            outText += ', %s/times(%d)' % (self._timeTransformation(speedT), self._outputTimes)
        # outCurrent:
        currentTime = str(datetime.datetime.now())
        currentTime = currentTime.split('.')[0].split('-', 1)[1]
        outText += ', ' + currentTime + ']'

        if outText != None and len(outText.strip()) > 0 and saveText:
            print(outText)
        sys.stdout.flush()
        ProgressOut3.Desc = None

    def addOutputTimes(self, times=1):
        if not self._isStart:
            return
        self._outputTimes += times

    def reDesc(self, desc):
        self._desc = desc

    @staticmethod
    def outputCurrent():
        print('Current time: ' + str(datetime.datetime.now()))

    @staticmethod
    def flush():
        sys.stdout.flush()

    def __iter__(self):
        self._start()
        for obj in self._iterable:
            self._output(self._desc if not ProgressOut3.Desc else str(ProgressOut3.Desc), self._total)
            yield obj
        self._end(saveText=self._leave)


if __name__ == '__main__':
    x = 10
    import random

    # progressOut=ProgressOut().start()
    # for i in range(x):
    #     progressOut.output(text='x',outTime=True,sumTimes=x,outSpeed=True)
    #     time.sleep(random.random()*2)
    # progressOut.end(saveText=False,text='x',outCurrent=True,outTime=True)

    # progressOut2=ProgressOut2().start(sumTimes=x)
    # for i in range(x):
    #     progressOut2.output(text='x')
    #     time.sleep(random.random()*2)
    # progressOut2.end(saveText=False)
    # progressOut2.outputCurrent()

    for i in ProgressOut3(range(10)):
        ProgressOut3.Desc = i
        time.sleep(random.random())
