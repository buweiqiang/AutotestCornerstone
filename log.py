import logging
import time
import sys
import os

LOG_LEVEL = 'info'
LOG_TO_FILE = False
LOG_FOLDER = os.path.join(os.path.dirname(__file__), '../TestLog')


def initLogger(name=__file__, level='INFO', logfile=None):
    logging.basicConfig(level=level, format='%(asctime)s %(name)-10s: %(levelname)+8s: %(message)s')
    logger = logging.getLogger(name)
    # 加了输出到sys.stdout后，日志会输出两遍，所以注释掉
    # _handler = logging.StreamHandler(sys.stdout)
    # logger.addHandler(_handler)

    if logfile is not None:
        fh = logging.FileHandler(logfile)
        fh.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s @%(filename)s[%(lineno)d]')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger


def getLogger(name='autotest'):
    global LOG_LEVEL, LOG_TO_FILE, LOG_FOLDER
    try:
        from conf import config
        g_config = config.getGlobalConfig()
        LOG_LEVEL = g_config.getLogLevel()
        if g_config.getLogToFile().lower() == 'true':
            LOG_TO_FILE = True
            LOG_FOLDER = g_config.getLogDir()
        LOG_FOLDER = os.path.realpath(LOG_FOLDER)
    except Exception as e:
        print(e)
        pass

    log_file = None
    if LOG_TO_FILE:
        filename = name + '_' + time.strftime('%Y-%m-%d.log')
        log_file = os.path.join(LOG_FOLDER, filename)

    return initLogger(name, LOG_LEVEL, log_file)


if __name__ == '__main__':
    logger = initLogger(level=23)
    # logger = initLogger('test',logfile='/Users/boweiqiang/autotest.log')
    logger.info('info by logger')
    logger.warning('warning by logger')
    logger = getLogger()
    logger.warning('test by bwq')
    logger.error(LOG_FOLDER)
