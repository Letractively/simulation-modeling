# -*- coding: utf-8 -*-

'Тесты для модуля queue.py'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests) + '/core')

import queue, unittest

class queueTest(unittest.TestCase):
  def testNewQueueShouldBeEmpty(self):
    'Вновь создаваемая очередь пуста'
    self.assertEqual(queue.Queue(), [])
  
  def testIfNewItemIsAdded(self):
    'add() добавляет элементы'
    q = queue.Queue()
    q.add(5)
    self.assertEqual(q, [5])
    q.add(6)
    self.assertEqual(q, [5, 6])
  
  def testIfItemIsRemoved(self):
    q = queue.Queue()
    q.add(5)
    i = q.next()
    self.assertEqual(i, 5)
    self.assertEqual(q, [])
  
  def testOrder(self):
    q = queue.Queue()
    q.add(5)
    q.add(6)
    q.add(7)
    self.assertEqual(q.next(), 7)
    self.assertEqual(q.timeout(), 5)

if __name__ == '__main__':
  unittest.main()
