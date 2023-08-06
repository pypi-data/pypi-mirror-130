from logging import getLogger, FileHandler, Formatter, ERROR, DEBUG, INFO, WARN
from functools import wraps
from time import strftime, localtime
import os


class Logger:

    def __init__(self, module_name='common', level='INFO', log_files_root='./log/'):
        """
        日志工具初始化
        :param module_name: 日志模块名称
        :param level: 日志级别
        :param log_files_root: 日志根目录
        """
        # logger
        self._logger = getLogger()
        # 日志文件跟目录
        self._root = log_files_root

        # 时间后缀
        date_time = strftime("%Y-%m-%d", localtime())

        # 日志文件名
        if module_name == 'common':
            file_name = self._root + 'common_' + date_time + '.log'
        else:
            file_name = self._root + module_name + '_' + date_time + '.log'

        # 判断日志路径是否存在
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except FileExistsError as e:
                print(str(e))

        # 判断日志文件是否存在
        if not os.path.exists(file_name):
            try:
                os.mknod(file_name)
            except AttributeError as e:
                print(str(e))
                f = open(file_name, 'w')
                f.close()

        # 日志级别
        if level == 'INFO':
            log_level = INFO
        elif level == 'DEBUG':
            log_level = DEBUG
        elif level == 'DEBUG':
            log_level = DEBUG
        else:
            log_level = ERROR

        # 日志输出设置
        self._logger.setLevel(log_level)
        self.formatter = Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
        self.file_handler = FileHandler(file_name, encoding='utf-8', mode='a')
        self.file_handler.setFormatter(self.formatter)

    def log(self, func):
        """
        日志输出装饰器
        :param func:
        :return:
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            self._logger.addHandler(self.file_handler)
            # noinspection PyBroadException
            try:
                # 日志中打印函数参数
                self._logger.info(func.__name__ + '[参数]: ' + str(args) + str(**kwargs))
                return func(*args, **kwargs)
            except Exception as e:
                self._logger.error(func.__name__ + '[执行异常]: ' + str(e))
            self._logger.removeHandler(self.file_handler)

        return wrapper

    # info 级别日志
    def info(self, info):
        self._logger.addHandler(self.file_handler)
        self._logger.info(info)
        self._logger.removeHandler(self.file_handler)

    # error 级别日志
    def error(self, error):
        self._logger.addHandler(self.file_handler)
        self._logger.error(error)
        self._logger.removeHandler(self.file_handler)

    # waring 级别日志
    def waring(self, waring):
        self._logger.addHandler(self.file_handler)
        self._logger.warning(waring)
        self._logger.removeHandler(self.file_handler)
