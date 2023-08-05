import sys
import time

class ProgressBar(object):
    def __init__(self, size=100, length=100, prefix='', suffix='', decimals=1, fill='█', infos=False, printEnd ="\r", file=sys.stdout):
        """
        Call to create a terminal progressbar object
        @params:
            size        - Required  : total value of the progress (Int)                         | Default is 100
            length      - Optional  : character length of bar (Int)                             | Default is 100
            prefix      - Optional  : prefix string (Str)                                       | Default is ""
            suffix      - Optional  : suffix string (Str)                                       | Default is ""
            decimals    - Optional  : positive number of decimals in percent complete (Int)     | Default is 1
            fill        - Optional  : bar fill character (Str)                                  | Default is "█"
            infos       - Optional  : show infos of the progress (Bool)                         | Default is False
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)                   | Default is "\r"
            file        - Optional  : where the system is writing (Object)                      | Default is sys.stdout
        """

        self.size = size
        self.total = size
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        self.file = file
        self.elapsed = 0
        self.last_t = 0
        self.latest_t = 0
        self.delta_t = 0
        self.percent = 0
        self.remaining = 0
        self.bps = 0
        self.remaining_time = 0
        self.seconds = 0
        self.minutes = 0
        self.infos = infos

    def update(self, value):
        """
        Call to update the created terminal progressbar object
        @params:
            value       - Required  : value of the progression (Int)    | For example the downloaded size of a file
        """

        self.value = value

        if self.infos:
            self.elapsed = round((self.last_t + self.latest_t), 1)
            self.last_t = time.perf_counter()
            try:
                self.delta_t = self.last_t- self.latest_t
                self.bps = self.value / self.delta_t
                self.remaining = (self.total - self.value) / self.bps
                self.remaining_time = int(round((self.remaining / self.delta_t), 0))
                self.seconds = self.remaining_time % 60
                self.minutes = int(self.remaining_time / 60)
            except ZeroDivisionError:
                pass
            self.percent = ("{0:." + str(self.decimals) + "f}%").format(100 * (self.value / float(self.total)))
            filledLength = int(self.length * self.value // self.total)
            bar = self.fill * filledLength + '-' * (self.length - filledLength)
            self.file.write("%s |%s| %s %s [Elapsed: %ss Left: %s:%s] %s" % (self.prefix, bar, self.percent, self.suffix, self.elapsed, self.minutes, self.seconds, self.printEnd))
            self.file.flush()
            self.latest_t = time.perf_counter()
        else:
            self.percent = ("{0:." + str(self.decimals) + "f}%").format(100 * (self.value / float(self.total)))
            filledLength = int(self.length * self.value // self.total)
            bar = self.fill * filledLength + '-' * (self.length - filledLength)
            self.file.write("%s |%s| %s %s %s" % (self.prefix, bar, self.percent, self.suffix, self.printEnd))
            self.file.flush()

