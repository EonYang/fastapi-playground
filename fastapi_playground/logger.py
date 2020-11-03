import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

root_logger = logging.getLogger('root')


def get_basic_logger(name, level=None):

    logger = logging.getLogger(name)

    if level:
        logger.setLevel(level)

    return logger


class NoHealth(logging.Filter):
    def filter(self, record):
        return 'healthcheck' not in record.getMessage()


# hide health_check logs
logging.getLogger('uvicorn.access').addFilter(NoHealth())
