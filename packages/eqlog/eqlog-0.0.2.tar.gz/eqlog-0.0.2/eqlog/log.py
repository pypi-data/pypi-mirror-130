from logging import getLogger, FileHandler, Formatter, ERROR, DEBUG, INFO
from functools import wraps
from time import strftime, localtime
import os


class Logger:
    # 成员变量 logger
    logger = getLogger()

    # 初始化
    def __init__(self, file_name='', level='INFO'):
        date_time = strftime("%Y-%m-%d", localtime())
        if file_name == '':
            file_name = './log/run_' + date_time + '.log'
        else:
            file_name = file_name + date_time + '.log'
        if not os.path.exists(file_name):
            os.path.dirname(file_name)
            print(str(os.path.dirname(file_name)))
            os.makedirs(os.path.dirname(file_name))
            try:
                os.mknod(file_name)
            except AttributeError as e:
                print(str(e))
                f = open(file_name, 'w')
                f.close()
        if level == 'ERROR':
            log_level = ERROR
        elif level == 'DEBUG':
            log_level = DEBUG
        else:
            log_level = INFO
        lfh = FileHandler(file_name, encoding='utf-8', mode='a')
        formatter = Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")
        lfh.setFormatter(formatter)
        self.logger.addHandler(lfh)
        self.logger.setLevel(log_level)

    # 日志输出注解
    def log(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(func.__name__ + '[入参]: ' + str(args))
            # noinspection PyBroadException
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(func.__name__ + ': ' + str(e))

        return wrapper

    # info 级别日志
    def info(self, info):
        self.logger.info(info)

    # error 级别日志
    def error(self, error):
        self.logger.error(error)

    # waring 级别日志
    def waring(self, waring):
        self.logger.warning(waring)
