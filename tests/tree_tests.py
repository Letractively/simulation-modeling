# -*- coding: utf-8 -*-

'Тесты для модуля tree'

import os, sys, operator
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import tree, unittest

class FromMaterializedPathTest(unittest.TestCase):
    'Стуктура входных данных'
    
    def test_positive(self):
        'Исходные данные корректны'
        
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
        
        self.assertEqual(tree.from_materialized_path(input), output)
    
    def test_skipped_branches(self):
        'Присутствуют пропуски ветвей'
        
        input = {
            'a.x' : 5,
            'b.y.z' : 6,
        }
        
        output = {
            'a': {
                'x': 5,
            },
            'b': {
                'y': {
                    'z': 6,
                },
            },
        }
        
        self.assertEqual(tree.from_materialized_path(input), output)
    
    def test_contradiction(self):
        'Наличие дочерних ветвей у узла, имеющего значение'
        
        input = {
            'a.x' : 5,
            'a.x.y' : 6,
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)
        
    def test_empty_branch_root(self):
        'Пустой узел в корне'
        
        input = {
            '.a': 5,
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)
        
    def test_empty_branch_middle(self):
        'Пустой узел в середине'
        
        input = {
            'a..b': 5,
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)
    
    
    def test_empty_branch_end(self):
        'Пустой узел в конце'
        
        input = {
            'a.b.': 5,
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)
        
    def test_empty_branches(self):
        'Ряд пустых узлов'
        
        input = {
            'a...b': 5,
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)

    def test_empty_input(self):
        'Пустой вход'
        
        self.assertEqual(tree.from_materialized_path({}), {})
        
    def test_empty_row(self):
        'Пустая входная строка'
        
        input = {
            '': '',
        }
        
        self.assertRaises(ValueError, tree.from_materialized_path, input)

class RecursiveMapTest(unittest.TestCase):
    'Рекурсивный map'
    
    def test_positive(self):
        'Простейший положительный тест'
        
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
        'Несовпадающие по структуре деревья'
        
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

if __name__ == '__main__':
    unittest.main()


