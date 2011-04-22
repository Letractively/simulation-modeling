# -*- coding: utf-8 -*-

'Декораторы моделей и прочие вспомогательные процедуры пакета models'

import distributions

Infinity = float('Infinity')
NaN      = float('NaN')

def accepts(**p):
    'Список параметров, которые принимает модель, записывается в её атрибут accepts'

    def mixer(model):
        'Подмешиваем в функцию её предусловия'
        model.accepts = p

        return model

    return mixer

# Предикаты

def non_empty(x):
  'Непустое значение'
  if x:
    return x
  else:
    raise ValueError(u'Пожалуйста, введите что-нибудь.')

def integer(x):
    'Целое число'
    try:
        return int(x)
    except:
        raise ValueError(u'Пожалуйста, введите целое число.')


def rational(x):
    'Число'
    try:
        return float(x)
    except:
        raise ValueError(u'Пожалуйста, введите число.')


def unsigned(x):
    'Число x не отрицательно'
    
    if x >= 0:
      return x
    else:
      raise ValueError(u'Пожалуйста, введите неотрицательное число.')


def positive(x):
    'Число x положительно'
    
    if x > 0:
      return x
    else:
      raise ValueError(u'Пожалуйста, введите положительное число.')


def probability(x):
    'Вероятность'
    if 0 <= x <= 1:
        return x
    else:
        raise ValueError(u'Пожалуйста, введите число из интервала [0, 1].')


def finite(x):
    'Конечность аргумента'

    if x in (Infinity, -Infinity, NaN):
        raise ValueError(u'Пожалуйста, введите конечную величину.')
    else:
        return x

def array(*conditions, **key_conditions):
    'Массив значений, имеющих указанные типы'
    
    def first(x):
        'Первый элемент списка'
        return x[0]
    
    def second(x):
        'Второй элемент списка'
        return x[1]
    
    # Честно - сам не знаю, что это и зачем
    if key_conditions:
        conditions = key_conditions
    
    def array(input):
        # Правила
        rules = dict((key, conditions) for key in input.keys())
        
        # Очищенная ветка дерева
        output = validate(input, rules)
        
        # Возвращаем обе ветки, преобразованные к форме отсортированного по ключам списка
        return map(second, sorted(output.items(), key=first))
    
    return array


def normal_distribution(conditions = {'mu' : (rational, finite), 'sigma' : (rational, finite, unsigned)}, postprocess = tuple()):
    'Нормальное распределение'
    
    def normal_distribution(field):
        values = validate(field, conditions)
        
        def normal_distribution(mu, sigma):
            stream = distributions.normal(mu, sigma)
        
            while True:
                value = stream.next() # Получение значения
                
                # И его обработка
                try:
                    for function in postprocess:
                        value = function(value)
                except:
                    continue # Следующее значение
                
                yield value
        
        return normal_distribution(values['mu'], values['sigma'])
    
    return normal_distribution
        

def inverse(x):
    'Обратная величина'
    return 1.0 / x

'''def distribution(conditions = {'mean' : (rational, finite), 'from' : (rational, finite), 'to' : (rational, finite)}, type = None, reverse = False):
    def distribution(field):
        'Распределение'
        
        def rotate(values):
            for variable, value in values.items():
                values[variable] = 1 / float(value)
        
        # Определим тип распределения
        types = ('exponential', 'equal', 'normal') # Допустимые типы
        try:
            t = field['type']
        except: # Тип не указан
            t = types[0]
        else:
            if not (t in types):
                raise ValueError(u'Распределение %s неизвестно.' % t)

        if t == 'exponential':
            values = validate(field, piece(conditions, ('mean', )))
            if reverse:
                rotate(values)
            return distributions.exponential(values['mean'])
        elif t == 'equal':
            values = validate(field, piece(conditions, ('from', 'to')))
            if reverse:
                rotate(values)
            return distributions.equal(*values.values())
        else:
            values = validate(field, piece(conditions, ('mean', )))
            if reverse:
                rotate(values)
            return distributions.normal(float(field['mean']))

    return distribution
'''

# Инструмент валидации

def normalize(args, accepts):
    'Удаление излишних аргументов'

    if type(args) != dict:
        return args

    for arg, value in args.items():
        if arg not in accepts:
            args.pop(arg)
        else:
            if type(accepts[arg]) == dict:
                normalize(value, accepts[arg])

    return args

def validate(node, conditions):
    'Проверка узла входных данных node по условиям preconditions'
    node_type = type(conditions)

    # Ветвь
    if node_type == dict:
        parameters = {} # Очищенные параметры
        errors = {} # Ошибки
        for child, condition in conditions.items():
            try: # Получение значения аргумента
                value = node[child] # Значение узла
            except:
                value = None
                errors[child] = 'absent'

            try: # Валидация
                parameters[child] = validate(value, conditions[child])
            except Exception, error:
                errors[child] = error.message

        if errors:
            raise Exception(errors)
        else:
            return parameters

    # Узел со списком правил
    elif node_type in (tuple, list):
        if node is not None:
            for condition in conditions:
                try:
                    node = condition(node)
                except Exception, error:
                    raise Exception(error.message)
            return node

    # Узел с одним правилом
    else:
        if node is not None:
            try:
                return conditions(node)
            except Exception, error:
                raise Exception(error.message)

square = lambda x: x * x

def piece(dictionary, keys):
    'Slicing для словарей'
    return dict((key, dictionary[key]) for key in keys if key in dictionary)
