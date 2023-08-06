import sys
import socket
import traceback
import inspect
from log_configs import server_log_config, client_log_config

if sys.argv[0].find('client') == -1:
    logger = server_log_config.ServerLogger()
    logger.set_up()
else:
    logger = client_log_config.ClientLogger()
    logger.set_up()

class DecoratorLogger:
    '''
       Декоратор, выполняющий логирование вызовов функций.
       Сохраняет события типа debug, содержащие
       информацию о имени вызываемой функиции, параметры с которыми
       вызывается функция, и модуль, вызывающий функцию.
       '''
    def __init__(self, logging_level, inside_logger = logger):
        self.logging_level = logging_level
        self.logger = inside_logger

    def dispatch_level(self, content):
        return {
            'critical': lambda: self.logger.critical(content),
            'error': lambda: self.logger.error(content),
            'debug': lambda: self.logger.debug(content),
            'info': lambda: self.logger.info(content)
        }.get(self.logging_level, lambda: None)()

    def __call__(self, func_to_log):
        def decorated(*args, **kwargs):
            frame = inspect.currentframe()
            stack_trace = traceback.format_stack(frame)
            result = func_to_log(*args, **kwargs)
            try:
                self.logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                    f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                    f' ФУНКЦИИ {stack_trace[0].strip().split()[-1]}. Вызов из'
                    f' метода {stack_trace[1].strip().split()[-1]}.'
                    f' Вызов конкретного метода {stack_trace[2].strip().split()[-1]}')
            except Exception:
                self.logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                                  f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                                  f' Вызов конкретного метода {stack_trace}')
            return result
        return decorated

def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from data.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker

