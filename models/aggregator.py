# -*- coding: utf-8 -*-

'Слой агрегации'

# Агрегирующий слой запускает модель много раз и собирает результаты каждого запуска. А затем вызывает агрегирующие функции, каждая из которых возвращает некое значение на основании собранных даных.

from tree import recursive_map

# Декоратор
def aggregate(*aggregators):
    'Приделываем к модели агрегаторы'
    def mixer(model):
        model.aggregators = aggregators
        
        return model
    
    return mixer

def average(*args):
    'Функция, находящая среднее арифметическое списка аргументов'
    
    try:
        return sum(args) / float(len(args))
    except:
        raise Exception(args)

def max_guaranteed_costs(variants):
    'Максимальные гарантированные расходы'
    
    from math import sqrt
    square = lambda x: x * x

    X = tuple(variant['balance']['costs'] for variant in variants)
    M = average(*X)
    s = sqrt(average(*(square(x - M) for x in X)))

    # Квантиль уровня гарантии
    K = 1.28

    # Теперь найдём максимальные гарантированные расходы.
    return M + K * s

def min_guaranteed_profit(variants):
    'Максимальные гарантированные расходы'
    
    from math import sqrt
    from models.validator import square
    
    X = tuple(variant['balance']['total'] for variant in variants)
    M = average(*X)
    s = sqrt(average(*(square(x - M) for x in X)))

    # Квантиль уровня гарантии
    K = 1.28

    # Теперь найдём максимальные гарантированные расходы.
    return M - K * s

def aggregator(model, args):
    'Агрегирующая функция'
    
    times = args.get('times', 1)
    
    if times == 1:
        output = model(**args)
        variants = [output]
    else:
        # Многократный запуск модели
        variants = tuple(model(**args) for _ in range(times))
        
        # Усреднённое значение
        output = recursive_map(average, *variants)
    
    # Агрегатные значения
    for f in model.aggregators:
        output[f.__name__] = f(variants)
    
    return output

