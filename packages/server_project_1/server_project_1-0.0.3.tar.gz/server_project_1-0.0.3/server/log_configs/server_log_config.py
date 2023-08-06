import logging
import os
from . import base_logger
import logging.handlers

class ServerLogger(base_logger.BaseLogger):
    def set_up(self):
        self.set_stream_handler()
        path = os.path.join(str(self.path) + '\logs', 'server.log')
        log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='D')
        log_file.setFormatter(self.log_format)
        self.logger = logging.getLogger('server')
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(log_file)
        self.logger.setLevel(self.logging_level)
        self.set_color()
        self.logger = logging.LoggerAdapter(self.logger, {"app": "Сервер"})

if __name__ == '__main__':
    logger = ServerLogger()
    logger.set_up()
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')