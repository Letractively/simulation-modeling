# -*- coding: utf-8 -*-

import producer_tests, tree_tests, validator_tests, warehouse_tests

# Модули
modules = (producer_tests, tree_tests, validator_tests, warehouse_tests)

for module in modules:
    for i in dir(module):
        test_class = getattr(module, i)
        if type(test_class) == type:
            for j in dir(test_class):
                test_function = getattr(test_class, j)
                if type(test_function).__name__ == 'instancemethod' and test_function.__name__.find('test_') == 0:
                    print test_function
                    print test_function.__doc__
                    print



