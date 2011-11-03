# -*- coding: utf-8 -*-

'Тесты для модели склада'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import unittest
from models import warehouse
from models import distributions

class WarehouseTest(unittest.TestCase):
    'Тесты для модели'
    
    def test_infinite_amount(self):
        '''На складе лежит достаточно большое количество товара, чтобы не было
        необходимости заказывать новые партии.'''
        
        result = warehouse.warehouse(
            demand = distributions.normal(1, 0),
            supply = distributions.normal(1, 0),
            amount = 100,
            lot_size = 10,
            limit = 0,
            price = {
                'supply'  : 9999,
                'storage' : 1,
                'fine'    : 9999,
            },
            total_time = 100
        )
        
        sample = {
            'units' : {
                'supply'  : 0,
                'fine'    : 0,
                'storage' : sum(range(101)) / 100.0,
            },
            
            'balance' : {
                'supply'  : 0,
                'storage' : sum(range(101)),
                'fine'    : 0,
                'costs' : sum(range(101)),
            },
        }
        
        self.assertEqual(result, sample)

    def test_single_delivery(self):
        '''Есть дефицит, но достаточно одной партии, чтобы его покрыть'''
        
        result = warehouse.warehouse(
            demand = distributions.normal(1, 0),
            supply = distributions.normal(0, 0),
            amount = 1,
            lot_size = 5,
            limit = 0,
            price = {
                'supply'  : 1,
                'storage' : 1,
                'fine'    : 9999,
            },
            total_time = 3,
            
        )
        
        
        sample = {
            'units' : {
                'supply'  : 1,
                'fine'    : 0,
                'storage' : 10 / 3.0,
            },
            
            'balance' : {
                'supply'  : 5,
                'storage' : 10,
                'fine'    : 0,
                'costs' : 15,
            },
        }
        
        self.assertEqual(result, sample)

    def test_no_supply(self):
        'Отсутствующие поставки'
        
        result = warehouse.warehouse(
            demand = distributions.normal(1, 0),
            supply = distributions.normal(999999999999999999, 0),
            amount = 0,
            lot_size = 0,
            limit = 0,
            price = {
                'supply'  : 9999,
                'storage' : 1,
                'fine'    : 1,
            },
            total_time = 100
        )
        
        
        sample = {
            'units' : {
                'supply'  : 0,
                'fine'    : 100,
                'storage' : 0,
            },
            
            'balance' : {
                'supply'  : 0,
                'storage' : 0,
                'fine'    : 100,
                'costs' : 100,
            },
        }
        
        self.assertEqual(result, sample)

    def test_no_supply_with_amount(self):
        'Отсутствующие поставки с начальным запасом'
        
        result = warehouse.warehouse(
            demand = distributions.normal(999999999999999999, 0),
            supply = distributions.normal(999999999999999999, 0),
            amount = 100,
            lot_size = 0,
            limit = 0,
            price = {
                'supply'  : 9999,
                'storage' : 1,
                'fine'    : 1,
            },
            total_time = 100
        )
        
        
        sample = {
            'units' : {
                'supply'  : 0,
                'fine'    : 0,
                'storage' : 100,
            },
            
            'balance' : {
                'supply'  : 0,
                'storage' : 10000,
                'fine'    : 0,
                'costs' : 10000,
            },
        }
        
        self.assertEqual(result, sample)
        
    def test_borders(self):
        'Тестирование граничных значений'
        
        input = {
            'demand': distributions.normal(100, 10),
            'supply': distributions.normal(12.5, 1),
            'amount': 1000,
            'lot_size': 100,
            'limit': 100,
            'price': {
                'supply'  : 2,
                'storage' : 3,
                'fine'    : 1.5,
            },
            'total_time': 224,
        }
        
        borders = (0.000 + 0.0001, 1000 + 0.0000)
        guard = False
        
        # Цикл по элементам списка input
        for variable, value in input.items():
            if type(value) in (float, int):
                for input[variable] in borders + (value, ):
                    warehouse.warehouse(**input)
            
            elif type(value) == dict:
                pass
            
            elif value.__name__ == 'normal':
                for a in borders + (10, ):
                    for b in borders + (10, ):
                        input[variable] = distributions.normal(a, b)
                        warehouse.warehouse(**input)
                
                input[variable] = value
                
                

if __name__ == '__main__':
    unittest.main()

