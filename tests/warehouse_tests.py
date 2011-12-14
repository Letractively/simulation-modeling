# -*- coding: utf-8 -*-

'Модель склада'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import unittest
from models.warehouse import warehouse

class WarehouseTest(unittest.TestCase):
    def test_none_orders(self):
        'Отсутствуют и заказы, и поставки'
        input = {
            'lot_size': 100,
            'limit': 0,
            'amount': 10,
            'total_time': 10,
            'demand_mu': 0,
            'demand_sigma': 0,
            'supply_mu': 10,
            'supply_sigma': 0,
            'demand_price': 100,
            'supply_price': 0,
            'storage_price': 0,
            'fine': 0,
            'times': 1,
        }
        
        sample = {
            'units': {
                'sales': 0,
                'supplies': 0,
                'fines': 0,
                'storage': 10,
            },
            'balance': {
                'sales': 0,
                'supplies': 0,
                'fines': 0,
                'storage': 0,
                'profit': 0,
                'costs': 0,
            },
        }
        
        output = warehouse(**input)
        del(output['history'])
        
        self.assertEqual(output, sample)
    
    def test_some_orders(self):
        'Имеются заказы, но нет поставок'
        input = {
            'lot_size': 100,
            'limit': 100,
            'amount': 1000,
            'total_time': 224,
            'demand_mu': 100,
            'demand_sigma': 10,
            'supply_mu': 12.5,
            'supply_sigma': 1,
            'demand_price': 100,
            'supply_price': 2,
            'storage_price': 3,
            'fine': 1.5,
            'times': 1,
        }
        
        input = {
            'lot_size': 100,
            'limit': 0,
            'amount': 10,
            'total_time': 10,
            'demand_mu': 1,
            'demand_sigma': 0,
            'supply_mu': 10,
            'supply_sigma': 0,
            'demand_price': 100,
            'supply_price': 0,
            'storage_price': 0,
            'fine': 0,
            'times': 1,
        }
        
        sample = {
            'units': {
                'sales': 10,
                'supplies': 0,
                'fines': 0,
                'storage': 5.5,
            },
            'balance': {
                'sales': 1000,
                'supplies': 0,
                'fines': 0,
                'storage': 0,
                'profit': 1000,
                'costs': 0,
            },
        }
        
        output = warehouse(**input)
        del(output['history'])
        
        self.assertEqual(output, sample)

    def test_some_orders_and_supplies(self):
        'Имеются и заказы и поставки'
        input = {
            'lot_size': 10,
            'limit': 0,
            'amount': 10,
            'total_time': 10,
            'demand_mu': 1,
            'demand_sigma': 0,
            'supply_mu': 10,
            'supply_sigma': 0,
            'demand_price': 100,
            'supply_price': 0,
            'storage_price': 0,
            'fine': 0,
            'times': 1,
        }
        
        sample = {
            'units': {
                'sales': 10,
                'supplies': 0,
                'fines': 0,
                'storage': 5.5,
            },
            'balance': {
                'sales': 1000,
                'supplies': 0,
                'fines': 0,
                'storage': 0,
                'profit': 1000,
                'costs': 0,
            },
        }
        
        output = warehouse(**input)
        del(output['history'])
        
        self.assertEqual(output, sample)

    def test_no_starting_amount(self):
        'Начальный запас отсутствует'
        input = {
            'lot_size': 10,
            'limit': 0,
            'amount': 0,
            'total_time': 10,
            'demand_mu': 1,
            'demand_sigma': 0,
            'supply_mu': 5,
            'supply_sigma': 0,
            'demand_price': 100,
            'supply_price': 0,
            'storage_price': 0,
            'fine': 0,
            'times': 1,
        }
        
        sample = {
            'units': {
                'sales': 5,
                'supplies': 10,
                'fines': 5,
                'storage': 3,
            },
            'balance': {
                'sales': 500,
                'supplies': 0,
                'fines': 0,
                'storage': 0,
                'profit': 500,
                'costs': 0,
            },
        }
        
        output = warehouse(**input)
        del(output['history'])
        
        self.assertEqual(output, sample)

