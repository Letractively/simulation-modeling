# -*- coding: utf-8 -*-

'Тесты для модуля helpers.py'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))
sys.path.append(os.path.dirname(tests) + '/models')

import unittest
from lxml import etree

from interface import serialize_input
from accepts import positive, array
class InputSerializerTest(unittest.TestCase):
    'Тесты для interface.serialize_input'
    
    def test_empty(self):
        'Пустое дерево'
        self.assertEqual(etree.tounicode(serialize_input({}, {})), '<input/>')
    
    def test_plain(self):
        'Простые правила'
        input   = {'a' : '1', 'b' : '2.0'}
        accepts = {'a' : int, 'b' : float}
        xml     = '<input><a type="int">1</a><b type="float">2.0</b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts)), xml)
    
    def test_plain_with_lists(self):
        'Нет иерархии, правила в виде списков'
        input   = {'a' : '1', 'b' : '2.0'}
        accepts = {'a' : int, 'b' : (float, positive)}
        xml     = '<input><a type="int">1</a><b type="float positive">2.0</b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts)), xml)


    def test_positive(self):
        'Положительный тест'
        input   = {'a' : '1', 'b' : {'c' : '2.0', 'd' : ['1', '2', '3']}}
        accepts = {'a' : int, 'b' : {'c' : (float, positive), 'd' : array(int)}}
        xml     = '<input><a type="int">1</a><b type="group"><c type="float positive">2.0</c><d type="array"><item>1</item><item>2</item><item>3</item></d></b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts)), xml)
    
    def test_error(self):
        'Ошибка'
        input   = {'a' : '1', 'b' : '2,0'}
        accepts = {'a' : int, 'b' : float}
        errors  = {'b' : 'float'}
        xml     = '<input><a type="int">1</a><b type="float" error="float">2,0</b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts, errors = errors)), xml)

    def test_positive_error(self):
        'Положительный тест с ошибками'
        
        input   = {'a' : '1,', 'b' : {'c' : '-2.0', 'd' : ['1', '2', '3']}}
        accepts = {'a' : int, 'b' : {'c' : (float, positive), 'd' : array(int)}}
        errors  = {'a' : 'int', 'b.c' : 'positive'}
        
        xml     = '<input><a type="int" error="int">1,</a><b type="group"><c type="float positive" error="positive">-2.0</c><d type="array"><item>1</item><item>2</item><item>3</item></d></b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts, errors = errors)), xml)
      
    def test_empty_input(self):
        'Пустой input'
        
        input   = {}
        accepts = {'a' : int, 'b' : float}
        errors  = {'a' : 'absent', 'b' : 'absent'}
        
        xml     = '<input><a type="int" error="absent"/><b type="float" error="absent"/></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts, errors = errors)), xml)

    def test_empty_input_hierarchy(self):
        'Пустой input с иерархией'
        
        input   = {}
        accepts = {'a' : int, 'b' : {'c' : float, 'd' : float }}
        errors  = {'a' : 'absent', 'b.c' : 'absent', 'b.d' : 'absent'}
        
        xml     = '<input><a type="int" error="absent"/><b type="group"><c type="float" error="absent"/><d type="float" error="absent"/></b></input>'
        
        self.assertEqual(etree.tounicode(serialize_input(input, accepts, errors = errors)), xml)

'''
class serializeTest(unittest.TestCase):
  'Тест процедуры serialize'
  
  def testEmpty(self):
    'Пустое дерево'
    
  
  def testDictionary(self):
    'Словарь'
    self.assertEqual(etree.tounicode(view.serialize('tree', {'a' : 1, 'b' : 2})), '<tree><a>1</a><b>2</b></tree>')

  def testList(self):
    'Список'
    self.assertEqual(etree.tounicode(view.serialize('tree', (1, 2))), '<tree><item>1</item><item>2</item></tree>')
  
  def testPlain(self):
    'Скаляр'
    self.assertEqual(etree.tounicode(view.serialize('tree', 5.0)), '<tree>5.0</tree>')
  
  def testComplex(self):
    'Сложный положительный тест'
    self.assertEqual(
      etree.tounicode(
        view.serialize(
          'tree',
          {
            'statistics' : (
              5.0, 6, '8'
            ),
            'foo' : {
              'bar' : '',
            }
          }
        )
      ),
      u'<tree><statistics><item>5.0</item><item>6</item><item>8</item></statistics><foo><bar></bar></foo></tree>'
    )
'''

if __name__ == '__main__':
  unittest.main()

