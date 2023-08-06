import logging, os, time, re
from stat import ST_MTIME
from logging.handlers import TimedRotatingFileHandler


class TimedHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        super(TimedHandler, self).__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.when = when.upper()
        self.backupCount = backupCount
        self.utc = utc
        self.atTime = atTime
        if self.when == 'S':
            self.interval = 1  # one second
            self.suffix = "%Y%m%d.%H%M%S"
            self.extMatch = r"^\d{4}\d{2}\d{2}.\d{2}\d{2}\d{2}(\.\w+)?$"
        elif self.when == 'M':
            self.interval = 60  # one minute
            self.suffix = "%Y%m%d.%H%M"
            self.extMatch = r"^\d{4}\d{2}\d{2}.\d{2}\d{2}(\.\w+)?$"
        elif self.when == 'H':
            self.interval = 60 * 60  # one hour
            self.suffix = "%Y%m%d.%H"
            self.extMatch = r"^\d{4}\d{2}\d{2}.\d{2}(\.\w+)?$"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.interval = 60 * 60 * 24  # one day
            self.suffix = "%Y%m%d"
            self.extMatch = r"^\d{4}\d{2}\d{2}(\.\w+)?$"
        elif self.when.startswith('W'):
            self.interval = 60 * 60 * 24 * 7  # one week
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: %s" % self.when)
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y%m%d"
            self.extMatch = r"^\d{4}\d{2}\d{2}(\.\w+)?$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)
        
        self.extMatch = re.compile(self.extMatch, re.ASCII)
        self.interval = self.interval * interval  # multiply by units requested
        filename = self.baseFilename
        if os.path.exists(filename):
            t = os.stat(filename)[ST_MTIME]
        else:
            t = int(time.time())
        self.rolloverAt = self.computeRollover(t)


def get_logger(file_name=None, log_path='logs', when='D', backup_count=3, level='info'):
    """
    :param file_name: 自定义log名称（创建的log会放在此路径下），None 会通过时间戳来创建文件夹
    :param log_path: log的根目录
    :param when: 拆分日志的时间间隔：周(W)、天(D)、时(H)、分(M)、秒(S)切割。
    :param backup_count: 保留拆分后最新的文件数量，比如如果为3，则表示保留3天内的日志，3天前的日志会被删除；如果为0，则所有拆分的日志都会保存
    :param level: 日志输出等级，分为 info，debug，warning（warn），error 四个等级
    :return:  返回logger对象，通过调用info，debug，error等方法可以写入日志
    """
    # 选择日志输出等级
    level = level.lower()
    logger_infos = {
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warning': logging.WARNING,
        'warn': logging.WARNING,
        'error': logging.ERROR
    }
    cur_time = time.strftime('%Y%m%d')
    if file_name is None:
        file_name = cur_time
    logger = logging.getLogger(file_name)
    logger.setLevel(logger_infos[level])
    if file_name == cur_time:  # 未传入名称的，以日期作为文件夹类别
        log_file_path = os.path.join(log_path, file_name)
    else:  # 传入名称的，以传入的名称作为类别
        log_file_path = os.path.join(log_path, file_name, cur_time)
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
    file_name = os.path.join(log_file_path, 'log')
    # 定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh = TimedHandler(filename=file_name, when=when, backupCount=backup_count, encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 将logger添加到handler里面
    return logger


if __name__ == '__main__':
    # logger = get_logger(file_name='abcd', log_path='./logs', when='S', level='debug')
    # logger = get_logger('classifier', log_path='./logs', when='S', level='debug')
    # import warnings
    # warnings.filterwarnings("ignore")

    logger = get_logger(log_path='../../logs', when='S', level='info')
    for i in range(100):
        logger.info(i)
        if i % 3 == 0:
            logger.error(i)
        if i % 2 == 0:
            logger.warning(i)
        time.sleep(0.1)

