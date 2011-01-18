# -*- coding: utf-8 -*-

'Тесты для модуля imitator.py'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))
sys.path.append(os.path.dirname(tests) + '/models')

import unittest
from imitator import parse_args
class ArgsParserTest(unittest.TestCase):
        'Тесты для imitator.parse_args'
        
        def test_positive(self):
                'Положительный тест'
                self.assertEqual(
                        parse_args('a=1&b=2&b=3&c.a=1&c.b=2&c.b=3'),
                        {
                                'a' : '1',
                                'b' : ['2', '3'],
                                'c' : {
                                        'a' : '1',
                                        'b' : ['2', '3'],
                                },
                        }
                )
    
        def test_list(self):
                'Список значений'
                args = ['2', '3', 'sdf', 'вася', '!!!']
                query = '&'.join(('a=' + arg for arg in args))
                self.assertEqual(
                        parse_args(query),
                        {'a' : args}
                )
        
        def test_tree(self):
                'Правильность построения дерева'
                self.assertEqual(
                        parse_args('a=5&a.b=2&a.c.d=8'),
                        {
                                'a' : {
                                        'b' : '2',
                                        'c' : {
                                                'd' : '8',
                                        },
                                },
                        }
                )


from imitator import validate
from accepts  import *

class ValidatorTest(unittest.TestCase):
    'Тесты для функции imitator.validate'
    
    def test_positive(self):
        'Положительный тест'
        
        args = {'a' : '5', 'b' : {'c' : '8.365', 'd' : '-7.15'}}
        accepts = {'a' : int, 'b' : {'c' : (float, unsigned), 'd' : float}}
        
        self.assertEqual(validate(args, accepts), {'a' : 5, 'b' : {'c' : 8.365, 'd' : -7.15}})
    
    def test_no_dictionary(self):
        'Скалярное значение вместо словаря'
        
        args    = {'a' : '15'}
        accepts = {'a' : {'b' : int, 'c' : float}}
        
        self.assertRaises(Exception, validate, args, accepts)
        
        try:
            validate(args, accepts)
        except Exception, error:
            self.assertEqual(error.args, (('a.c', 'absent'), ('a.b', 'absent')))
    
    def test_absent(self):
        'Отсутствие обязательного параметра'
        
        args = {'a' : '5'}
        accepts = {'a' : int, 'b' : {'c' : (float, unsigned), 'd' : float}}
        
        self.assertRaises(Exception, validate, args, accepts)
        
        try:
            validate(args, accepts)
        except Exception, error:
            self.assertEqual(error.args, (('b', 'absent'), ('b.c', 'absent'), ('b.d', 'absent')))
    
    def test_invalid(self):
        'Неверное значение'
        
        args    = {'a' : 'hehe', 'b' : '-8.365'}
        accepts = {'a' : int, 'b' : (float, positive), 'c' : {'d' : float, 'e' : int}}
        
        self.assertRaises(Exception, validate, args, accepts)
        
        try:
            validate(args, accepts)
        except Exception, error:
            self.assertEqual(dict(error.args), {'a' : 'int', 'b' : 'positive', 'c' : 'absent', 'c.d' : 'absent', 'c.e' : 'absent'})
    
from imitator import normalize
class NormalizeTest(unittest.TestCase):
    'Тесты для процедуры imitator.normalize'
    
    def test_positive(self):
        'Положительный тест'
        
        args    = {'a' : '15', 'b' : '3.1415', 'c' : 'hehe', 'e' : {'f' : '8', 'g' : '3'}}
        accepts = {'a' : int, 'b' : float, 'e' : {'g' : int}}
        
        self.assertEqual(normalize(args, accepts), {'a' : '15', 'b' : '3.1415', 'e' : {'g' : '3'}})
    
    def test_no_dict(self):
        'Скаляр вместо словаря'
        
        args    = {'a' : '15'}
        accepts = {'a' : {'b' : int, 'c' : float}}
        
        self.assertEqual(normalize(args, accepts), {'a' : '15'})

if __name__ == '__main__':
    unittest.main()

#args = {'a' : '5'}
#accepts = {'a' : int, 'b' : {'c' : (float, unsigned), 'd' : float}}

#print validate(args, accepts)

