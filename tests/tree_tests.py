# -*- coding: utf-8 -*-

'Тесты для модуля tree'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import tree, unittest

class FromLeavesTest(unittest.TestCase):
    'Тест для процедуры from_leaves'
    
    def test_positive(self):
        'Сложный положительный тест'
        
        input = {
            'a.b.c' : 5,
            'a.b.d' : 6,
            'd' : 'sdf',
        }
        
        output = {
            'a' : {
                'b' : {
                    'c' : 5,
                    'd' : 6,
                },
            },
            'd' : 'sdf',
        }
        
        self.assertEqual(tree.from_leaves(input), output)
    
class RecursiveMapTest(unittest.TestCase):
    'Рекурсивный map'
    
    def test_positive(self):
        'Положительный тест'
        
        def f(*args):
            return args
        
        tree1 = {
            'a' : 'a1',
            'b' : {
                'c' : 'c1',
                'single' : 'single1',
            },
            'different_types' : {
                'k' : 1,
            },
        }
        
        tree2 = {
            'a' : 'a2',
            'b' : {
                'c' : 'c2',
            },
            'additional' : 'additional2',
            'different_types' : 'different_types2',
        }
    
        output = {
            'a' : ('a1', 'a2'),
            'b' : {
                'c' : ('c1', 'c2'),
                'single' : ('single1', None),
            },
            'different_types' : {
                'k' : (1, None),
            },
        }
    
        self.assertEqual(tree.recursive_map(f, tree1, tree2), output)
    
if __name__ == '__main__':
    unittest.main()


