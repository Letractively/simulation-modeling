# -*- coding: utf-8 -*-

'Тесты для модели производственной фирмы'

import os, sys, unittest
from copy import deepcopy
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

from models import producer, distributions

class ProducerTest(unittest.TestCase):
    def test_borders(self):
        'Тестирование граничных значений'
                
        input = {
            'instream': 0.28,
            'operations': [4.08],
            'deviation': 0.1,
            'income': 610,
            'costs': 120,
            'salary': 600,
            'total_time': 170,
        }
        
        borders = (0.000 + 0.0001, 1000 + 0.0000)
        guard = False
        
        # Цикл по элементам списка input
        for variable, value in input.items():
            if type(value) != list:
                for input[variable] in borders + (value, ):
                    if guard:
                        try:
                            producer.producer(**input)
                        except:
                            raise Exception(input)
                    else:
                        producer.producer(**input)
            
        
        

if __name__ == '__main__':
    unittest.main()

