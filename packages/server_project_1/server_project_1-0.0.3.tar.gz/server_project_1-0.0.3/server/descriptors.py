import logging
import decos
import ipaddress

logger = logging.getLogger('server')

class Port:
    '''
        Класс - дескриптор для номера порта.
        Позволяет использовать только порты с 1023 по 65536.
        При попытке установить неподходящий номер порта генерирует исключение.
        '''
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            decos.logger.critical(f'[CRITICAL] Неверное указание порта - {value}. Допустимы только адреса с 1024 до 65535!')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class Address:
    '''
            Класс - дескриптор для номера адреса.
            '''
    def __set__(self, instance, value):
        try:
            ipaddress.ip_address(value)
        except ValueError:
            decos.logger.critical(
                f'[CRITICAL] Неверное указание адреса - {value}.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name



