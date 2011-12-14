# -*- coding: utf-8 -*-

import inspect, unittest

__all__ = ['warehouse_tests', 'tree_tests']

# Модули
modules = dict((module, __import__(module)) for module in __all__)

# Классы
suites = dict((module, []) for module in modules.keys())

for module_name, module in modules.items():
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            suites[module_name].append(obj)

# Выполнение тестов

for module, cases in suites.items():
    print
    print
    print modules[module].__doc__
    print '-' * 70
    for case in cases:
        suite = unittest.TestLoader().loadTestsFromTestCase(case)
        unittest.TextTestRunner(verbosity=2).run(suite)





