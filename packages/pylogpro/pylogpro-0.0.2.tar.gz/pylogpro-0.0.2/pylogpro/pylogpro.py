import time
from .level import *

class Loger:
    def __init__(self):
        self.to_file = False
        self.log_file = "log.txt"
        self.level = WARNING #日志记录级别
        self.format = "{level}: {msg}"
        self.time_format = "%Y-%m-%d %H:%M:%S" #时间格式
    def __format_msg(self, level, msg):
        """格式化msg"""
        msg = self.format.replace("{msg}", msg)
        if level == DEBUG:
            msg = msg.replace("{level}", "DEBUG")
        elif level == INFO:
            msg = msg.replace("{level}", "INFO")
        elif level == WARNING:
            msg = msg.replace("{level}", "WARNING")
        elif level == ERROR:
            msg = msg.replace("{level}", "ERROR")
        msg = msg.replace("{asctime}", time.asctime(time.localtime()))
        msg = msg.replace("{time}", time.strftime(self.time_format, time.localtime()))
        return msg
    def __write_log_file(self, msg):
        """将日志写入文件"""
        with open(self.log_file, "a") as f:
            f.write(msg)
            f.write("\n")
    def set_level(self, level):
        """设置日志记录级别"""
        if type(level) == type(int()):
            self.level = level
        elif type(level) == type(str()):
            if level == "DEBUG":
                self.level = DEBUG
            elif level == "INFO":
                self.level = INFO
            elif level == "WARNING":
                self.level = WARNING
            elif level == "ERROR":
                self.level = ERROR
    def set_format(self, str_format: str):
        """设置日志格式"""
        self.format = str_format
    def set_time_format(self, str_format: str):
        """设置时间格式"""
        self.time_format = str_format
    def set_logfile(self, str_format: str):
        """设置日志文件名"""
        self.format = str_format
        self.to_file = True
    def debug(self, msg: str):
        if DEBUG >= self.level:
            msg = self.__format_msg(DEBUG, msg)
            print(msg)
            self.__write_log_file(msg)
    def info(self, msg: str):
        if INFO >= self.level:
            msg = self.__format_msg(INFO, msg)
            print(msg)
            self.__write_log_file(msg)
    def warning(self, msg: str):
        if WARNING >= self.level:
            msg = self.__format_msg(WARNING, msg)
            print(msg)
            self.__write_log_file(msg)
    def error(self, msg: str):
        if ERROR >= self.level:
            msg = self.__format_msg(ERROR, msg)
            print(msg)
            self.__write_log_file(msg)
