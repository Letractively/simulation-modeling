# -*- coding: utf-8 -*-

'Несимметрическая функция map для деревьев'

import os, sys, operator, unittest
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import tree

class RecursiveMapTest(unittest.TestCase):
    'Рекурсивный map'
    
    def test_positive(self):
        'Структуры деревьев совпадают'
        
        trees = [
            {
                'a': 1,
                'b': {
                    'c': 2,
                },
            } for _ in range(5)
        ]
        
        self.assertEqual(
            tree.recursive_map(lambda *args: sum(args), *trees), 
            {
                'a': 5,
                'b': {
                    'c': 10,
                }
            }
        )
    
    def test_unmatching_trees(self):
        'Структуры деревьев не совпадают'
        
        tree1 = {
            'a': {
                'b': 5,
            },
            'c': 10,
        }
        
        tree2 = {
            'a': {
                'b': 5,
            },
        }
        
        output = {
            'a': {
                'b': (5, 5),
            },
            'c': (10, None),
        }
        
        self.assertEqual(tree.recursive_map(lambda *args: args, tree1, tree2), output)
        
        tree2['c'] = 10
        del tree1['c']
        del output['c']
        
        self.assertEqual(tree.recursive_map(lambda *args: args, tree1, tree2), output)




