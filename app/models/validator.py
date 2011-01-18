# -*- coding: utf-8 -*-

'Декораторы моделей и прочие вспомогательные процедуры пакета models'

import distributions

Infinity = float('Infinity')
NaN      = float('NaN')


def accepts(**p):
  '''Список параметров, которые принимает модель, записывается в её атрибут accepts;
  значения параметров по умолчанию - в атрибут defaults'''
  def mixer(f):
    # Подмешиваем в функцию её предусловия
    f.accepts = p
    
    return f

  return mixer

# Предикаты

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
    x = float(x)
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

def array(value_type):
    'Массив значений типа value_type'
    
    def array(values):
        return list(map(value_type, values))
    
    return array

def distribution(conditions = {'mean' : (float, finite), 'from' : (float, finite), 'to' : (float, finite)}):
    def distribution(field):
        'Распределение'

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
            return distributions.exponential(values['mean'])
        elif t == 'equal':
            values = validate(field, piece(conditions, ('from', 'to')))
            return distributions.equal(*values.values())
        else:
            return distributions.normal(float(field['mean']))

    return distribution

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

def stream_filter(stream, conditions, limit = 100):
    'Фильтрация потока по условиям'

    pass