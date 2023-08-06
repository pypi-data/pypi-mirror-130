import dis

class BaseMaker(type):
    '''
       Метакласс, проверяющий что в результирующем классе нет клиентских
       вызовов таких как: connect. Также проверяется, что серверный
       сокет является TCP и работает по IPv4 протоколу.
       '''
    def __init__(self, clsname, bases, clsdict):
        methods_for_server = []
        methods_for_client = []
        for func in clsdict:
            try:
                list_of_instructions = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for instruction in list_of_instructions:
                    if clsname == 'Server':
                        if instruction.argval == 'socket':
                            info_socket = dis.code_info(clsdict[func])
                            if 'create_socket' in info_socket:
                                if not ('AF_INET' in info_socket and 'SOCK_STREAM' in info_socket):
                                    raise TypeError('Некорректная инициализация сокета.')

                        if instruction.opname == 'LOAD_METHOD':
                            if instruction.argval not in methods_for_server:
                                methods_for_server.append(instruction.argval)
                    if clsname == 'Client':
                        if instruction.opname == 'LOAD_METHOD':
                            if instruction.argval not in methods_for_client:
                                methods_for_client.append(instruction.argval)
        if 'connect_socket' in methods_for_server and len(methods_for_server) > 0:
            raise TypeError('Использование метода connect недопустимо в серверном классе')

        for command in ('listen_connection', 'listen_connection', 'bind_socket'):
            if command in methods_for_client and len(methods_for_client) > 0:
                raise TypeError('В классе обнаружено использование запрещённого метода')

        if len(methods_for_client) > 0:
            if 'get_message' in methods_for_client or 'send_message' in methods_for_client:
                pass
            else:
                raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)