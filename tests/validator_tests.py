# -*- coding: utf-8 -*-

'Тесты для модуля validator'

import os, sys, operator, unittest
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

from models.validator import *

class NormalizeTest(unittest.TestCase):
    'Тесты для процедуры normalize'
    
    def test_positive(self):
        'Простейший положительный тест'
        
        args = {
            'a' : 1,
            'b' : {
                'c': 2,
                'y': '9',
            },
            'z': 10,
        }
        
        accepts = {
            'a' : 1,
            'b' : {
                'c': 2,
            },
        }
        
        self.assertEqual(normalize(args, accepts), accepts)

class ValidateTest(unittest.TestCase):
    'Тесты функции validate'
    
    def test_positive(self):
        'Входные данные корректны'
        
        args  = {
            'a': '-0.5',
            'b': '1',
            'c': {
                'd': '0',
            }
        }
        
        accepts = {
            'a': rational,
            'b': (integer, positive),
            'c': {
                'd': (rational, unsigned),
            }
        }
        
        output = {
            'a': -0.5,
            'b': 1,
            'c': {
                'd': 0.0,
            }
        }
        
        self.assertEqual(validate(args, accepts), output)
        
    def test_incorrect_value(self):
        'Неверное значение'
        
        args = {
            'a': '-0.5',
            'b': '1',
            'c': {
                'd': '0',
            }
        }
        
        accepts = {
            'a': (rational, positive),
            'b': (integer, positive),
            'c': {
                'd': (rational, unsigned),
            }
        }
        
        self.assertRaises(Exception, validate, args, accepts)

if __name__ == '__main__':
    unittest.main()

