"""
日志工具类
"""

from logging import getLogger, FileHandler, Formatter, ERROR, DEBUG, INFO, WARN
from eqlog.common import get_xml_path, read_xml, create_log_file
from functools import wraps
from time import strftime, localtime


class Logger:
    level_dictionary = {  # 日志级别字典
        'INFO': INFO,
        'ERROR': ERROR,
        'DEBUG': DEBUG,
        'WARNING': WARN
    }

    def __init__(self, module_name='common', level='INFO', log_files_dir='', config=''):
        """
        日志工具初始化
        :param module_name: 日志模块名称
        :param level: 日志级别
        :param log_files_dir: 日志根目录
        """
        _config = config if config != '' else get_xml_path()  # 获取 xml 配置文件路径
        self._root = log_files_dir if log_files_dir != '' else (
            read_xml(_config) if read_xml(_config) != '' else './logs')  # 日志文件路径

        self._logger = getLogger()  # logger
        self._date_time = strftime("%Y-%m-%d", localtime())  # 时间后缀
        self._log_module_name = module_name  # 日志模块名
        file_name = self.set_log_file_name()  # 日志文件名
        create_log_file(file_name)  # 创建日志文件

        self._logger.setLevel(self.level_dictionary[level])  # 日志级别
        self._formatter = Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")  # 日志格式
        self._file_handler = FileHandler(file_name, encoding='utf-8', mode='a')  # 日志文件编码
        self._file_handler.setFormatter(self._formatter)  # 日志文件格式

    # 函数装饰器：被装饰函数隐式输出日志
    # param func: 被装饰函数
    # return 装饰后的新函数
    def log(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # noinspection PyBroadException
            try:
                self.common_log('info', func.__name__ + '[参数]: ' + str(args) + str(**kwargs))  # 日志中打印函数参数
                return func(*args, **kwargs)
            except Exception as e:
                self.common_log('error', func.__name__ + '[执行异常]: ' + str(e))

        return wrapper

    def common_log(self, level='info', message=''):
        """
        通用日志处理
        :param level: 输出日志级别
        :param message: 日志字符串
        :return: None
        """
        # 日志时间
        if strftime("%Y-%m-%d", localtime()) == self._date_time:
            pass
        else:
            self._date_time = strftime("%Y-%m-%d", localtime())
            file_name = self.set_log_file_name()
            self._file_handler = FileHandler(file_name, encoding='utf-8', mode='a')
            self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)
        # 日志级别
        if level == 'info':
            self._logger.info(message)
        elif level == 'warning':
            self._logger.warning(message)
        elif level == 'debug':
            self._logger.debug(message)
        else:
            self._logger.error(message)
        self._logger.removeHandler(self._file_handler)

    def set_log_file_name(self):
        """
        日志文件名设置
        :return: 日志文件完整路径
        """
        if self._log_module_name == 'common':
            file_name = self._root + 'common_' + self._date_time + '.log'
        else:
            file_name = self._root + self._log_module_name + '_' + self._date_time + '.log'
        return file_name

    def info(self, info):
        """
        info 级别日志
        :param info: 日志信息
        :return: None
        """
        self.common_log('info', info)

    def error(self, error):
        """
        error 级别日志
        :param error: 日志信息
        :return: None
        """
        self.common_log('error', error)

    def waring(self, waring):
        """
        waring 级别日志
        :param waring: 日志信息
        :return: None
        """
        self.common_log('warning', waring)

    def debug(self, debug):
        """
        debug 级别日志
        :param debug: 日志信息
        :return: None
        """
        self.common_log('debug', debug)
