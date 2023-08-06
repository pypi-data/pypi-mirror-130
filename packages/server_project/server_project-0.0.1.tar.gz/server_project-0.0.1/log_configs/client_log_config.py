import logging
import os
from . import base_logger

class ClientLogger(base_logger.BaseLogger):
    def set_up(self):
        self.set_stream_handler()
        path = os.path.join(str(self.path) + '\logs', 'client.log')
        log_file = logging.FileHandler(path, encoding='utf8')
        log_file.setFormatter(self.log_format)
        self.logger = logging.getLogger('client')
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(log_file)
        self.logger.setLevel(self.logging_level)
        self.set_color()
        self.logger = logging.LoggerAdapter(self.logger, {"app": "Клиент"})

if __name__ == '__main__':
    logger = ClientLogger()
    logger.set_up()
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
