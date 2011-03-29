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
                'demand'    : 1,
                'storage' : 1,
                'fine'    : 9999,
            },
            total_time = 100
        )
        result.pop('history')
        
        sample = {
            'units' : {
                'supply'  : 0,
                'sales'   : 100,
                'fine'    : 0,
                'storage' : sum(range(101)) / 100.0,
            },
            
            'balance' : {
                'supply'  : 0,
                'storage' : sum(range(101)),
                'fine'    : 0,
                'sales' : 100,
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
                'demand'  : 1,
                'storage' : 1,
                'fine'    : 9999,
            },
            total_time = 3
        )
        result.pop('history')
        
        sample = {
            'units' : {
                'supply'  : 1,
                'sales'   : 3,
                'fine'    : 0,
                'storage' : 10 / 3.0,
            },
            
            'balance' : {
                'supply'  : 5,
                'storage' : 10,
                'fine'    : 0,
                'sales'   : 3,
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
                'demand'    : 1,
                'storage' : 1,
                'fine'    : 1,
            },
            total_time = 100
        )
        result.pop('history')
        
        sample = {
            'units' : {
                'supply'  : 0,
                'sales'   : 0,
                'fine'    : 100,
                'storage' : 0,
            },
            
            'balance' : {
                'supply'  : 0,
                'storage' : 0,
                'fine'    : 100,
                'sales' : 0,
            },
        }
        
        self.assertEqual(result, sample)

if __name__ == '__main__':
    unittest.main()

