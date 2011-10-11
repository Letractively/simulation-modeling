# -*- coding: utf-8 -*-

'Слой агрегации'

# Агрегирующий слой запускает модель много раз и собирает результаты каждого запуска. А затем вызывает агрегирующие функции, каждая из которых возвращает некое значение на основании собранных даных.

# Декоратор
def agregate(*agregators):
    'Приделываем к модели агрегатор и добавляем элемент к её входным данным'
    from models.validator import integer, finite, positive
    
    def mixer(model):
        model.accepts['times'] = (integer, finite, positive)
        model.agregators = agregators
        
        return model
    
    return mixer

def average(*args):
    'Функция, находящая среднее арифметическое списка аргументов'
    
    try:
        return sum(args) / float(len(args))
    except:
        raise Exception(args)

def mean(variants):
    'Усредняет все показатели по всем вариантам'
    from tree import recursive_map
    
    return recursive_map(average, *variants)

def max_guaranteed_costs(variants):
    'Максимальные гарантированные расходы'
    
    from math import sqrt
    from models.validator import square
    
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

def agregator(model, args):
    'Агрегирующая функция'
    
    # Количество запусков модели
    try:
        times = args.pop('times')
    except:
        times = 1
    
    # Агрегация производится, лишь только если количество запусков больше 1.
    if times <= 1:
        return model(**args)
    else:
        # Вычисления
        variants = tuple(model(**args) for i in range(times))
        
        # Проходим по каждой из агрегирующих функций
        output = dict((agregator.__name__, agregator(variants)) for agregator in model.agregators)
        
        output['agregated'] = True
        
        return output

