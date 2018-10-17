"""
根据时间变换日志文件的一个类
"""
# coding: utf-8
import logging
import datetime
import os


class FloggerHandler(logging.FileHandler):
    def __init__(self, filename, when='D', encoding=None, delay=False):
        dir_name, base_name = os.path.split(filename)
        self.prefix = base_name
        self.when = when.upper()
        # S - Every second a new file
        # M - Every minute a new file
        # H - Every hour a new file
        # D - Every day a new file
        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
        elif self.when == 'D':
            self.suffix = "%Y-%m-%d"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)
        self.file_format = "{}.{}".format(filename, self.suffix)
        self.file_path = datetime.datetime.now().strftime(self.file_format)
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
        except Exception:
            print("cannot make dirs, file_path is {}".format(self.file_path))
            pass

        self.delay = delay
        logging.FileHandler.__init__(self, self.file_path, 'a', encoding, delay)

    def do_change(self):
        """
        Do a rollover, as described in __init__().
        """
        self.baseFilename = os.path.abspath(self.file_path)
        if self.stream:
            self.stream.close()
            self.stream = None
        if not self.delay:
            self.stream = self._open()

    def should_change_file_to_write(self):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        _new_file_path = datetime.datetime.now().strftime(self.file_format)
        if _new_file_path != self.file_path:
            self.file_path = _new_file_path
            return 1
        return 0

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.should_change_file_to_write():
                self.do_change()
            logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
