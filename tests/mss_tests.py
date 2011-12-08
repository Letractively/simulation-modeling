# -*- coding: utf-8 -*-

'Тесты для модели системы массового обслуживания'

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import unittest
from models import mss
from models import distributions
from models.validator import const_generator

Infinity = float('inf')

class MssTest(unittest.TestCase):
    input = {
        'channels_count': 4,
        'total_time': 64,
        'in_stream': distributions.exponential(1.0/25),
        'out_stream': distributions.exponential(1.0/10),
        'cost': 150,
        'queue_size': 999,
        'queue_time': 0.25,
        'fault_stream': const_generator(Infinity)(0),
        'repair_stream': const_generator(Infinity)(0),
        'destructive': 0,
    }

    def test_positive(self):
        mss.mss(**self.input)
        
    def test_infinite_queue_time(self):
        b = self.input['queue_time']
        self.input['queue_time'] = Infinity
        mss.mss(**self.input)
        self.input['queue_time'] = b
        
    def test_infinite_queue_size(self):
        b = self.input['queue_size']
        self.input['queue_size'] = Infinity
        mss.mss(**self.input)
        self.input['queue_size'] = b

    def test_borders(self):
        input = self.input
        borders = (0.000 + 0.0001, 1000 + 0.0000)
        guard = False
        
        # Цикл по элементам списка input
        for variable, value in input.items():
            if type(value) == float:
                for input[variable] in borders + (value, ):
                    print input
                    mss.mss(**input)
            
            elif type(value) == int:
                for input[variable] in (50, 1) + (value, ):
                    print input
                    mss.mss(**input)
            
            elif type(value) == dict:
                pass
            
            elif value.__name__ == 'exponential':
                for a in borders + (10, ):
                    input[variable] = distributions.exponential(a)
                    print input
                    mss.mss(**input)
                
                input[variable] = value
        

if __name__ == '__main__':
    unittest.main()








