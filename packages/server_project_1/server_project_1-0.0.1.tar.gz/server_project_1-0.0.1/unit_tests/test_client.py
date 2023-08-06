"""Unit-тесты клиента"""
import sys
import os
import unittest
import time

sys.path.append(os.path.join(os.getcwd(), '..'))

from client import Client
from server import Server

class TestClientClass(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.check_server()
        self.client.create_socket()
        self.client.connect_socket()

    def test_check_server(self):
        self.assertEqual(self.client.check_server(), 1)

    def test_presense(self):
        test = self.client.create_presence()
        self.assertEqual(test, {"action": self.client.presence, "time": time.time(), "user": {"account_name": 'Guest'}})

    def test_process_answer_200(self):
        process_answer = self.client.process_answer({self.client.response: 200})
        self.assertEqual(process_answer, '200 : OK')

    def test_process_answer_400(self):
        process_answer = self.client.process_answer({self.client.response: 400, self.client.error: 'Bad Request'})
        self.assertEqual(process_answer, '400 : Bad Request')

    def test_process_answer_no_response(self):
        process_answer = self.client.process_answer({self.client.error: 'Bad Request'})
        self.assertRaises(ValueError, process_answer)

if __name__ == '__main__':
    unittest.main()
