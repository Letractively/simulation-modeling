# -*- coding: utf-8 -*-

'Тесты для модуля schedule.py'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests) + '/core')

import schedule, unittest

s = schedule.Schedule()
e1, e2, e3 = (1, 'hm'), (2, 'hi!'), (3, 'bye!')

class scheduleTest(unittest.TestCase):
  def testAddOrder(self):
    'Порядок добавления'
    s.add(*e2)
    s.add(*e1)
    s.add(*e3)
    
    self.assertEqual(s.schedule, [e1, e2, e3])
  
  def testRemoveOrder(self):
    'Порядок удаления'
    self.assertEqual(s.next(), e1)
    self.assertEqual(s.next(), e2)
    self.assertEqual(s.next(), e3)    

if __name__ == '__main__':
    unittest.main()
