"""Unit-тесты сервера"""

import sys
import os
import time
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))

from server import Server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server()

        self.err_dict = {
            self.server.response: 400,
            self.server.error: 'Bad Request'
        }
        self.ok_dict = {self.server.response: 200}

    def test_check_server(self):
        self.assertEqual(self.server.check_server(), 1)

    def test_listen_socket(self):
        self.server.create_socket()
        self.server.bind_socket()
        listen = self.server.listen_connection()
        self.assertEqual(listen, 1)

    # def test_listen_and_accept_connection(self):
    #     self.server.listen_connection(), self.server.accept_connection()
    #     self.assertEqual((self.server.listen_connection(), self.server.accept_connection()), (1, 1))

    def test_no_action(self):
        self.assertEqual(self.server.answer_status_to_client({self.server.time: time.time(), self.server.user: {self.server.account_name: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(self.server.answer_status_to_client({self.server.action: 'Wrong', self.server.time: time.time(), self.server.user: {self.server.account_name: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(self.server.answer_status_to_client({self.server.action: self.server.presence, self.server.user: {self.server.account_name: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(self.server.answer_status_to_client(
            {self.server.action: self.server.presence, self.server.time: time.time()}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(self.server.answer_status_to_client({self.server.action: self.server.presence, self.server.time: time.time(), self.server.user: {self.server.account_name: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        self.assertEqual(self.server.answer_status_to_client({self.server.action: self.server.presence, self.server.time: time.time(), self.server.user: {self.server.account_name: 'Guest'}}), self.ok_dict)

    # def tearDown(self):
    #     self.server.close_connection()

if __name__ == '__main__':
    unittest.main()
