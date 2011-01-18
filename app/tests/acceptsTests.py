# -*- coding: utf-8 -*-

'Тесты для модуля accepts.py'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests) + '/models')

import unittest

from accepts import array

f = array(float)
class ArrayTest(unittest.TestCase):
    'Тесты для accepts.array'
    
    def test_empty(self):
        'Пустой массив'
        self.assertEqual(f([]), [])
    
    def test_positive(self):
        'Положительный тест'
        self.assertEqual(f(['2.3', '4.5']), [2.3, 4.5])
    
    def test_non_list(self):
        'Входное значение не является списком'
        self.assertRaises(Exception, f, 3.3)
    
    def test_non_float(self):
        'Один из элементов списка не является числом'
        self.assertRaises(Exception, f, ['2,3', '4.5'])

if __name__ == '__main__':
  unittest.main()
