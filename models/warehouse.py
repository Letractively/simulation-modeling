# -*- coding: utf-8 -*-

'Склад'

import distributions
from models.validator import *

@accepts(
    demand     = normal_distribution(conditions = {'mu' : (rational, positive, finite), 'sigma' : (rational, finite, unsigned)}, postprocess = (positive, inverse)),
    supply     = normal_distribution(conditions = {'mu' : (rational, positive, finite), 'sigma' : (rational, finite, unsigned)}, postprocess = (positive,)),
    amount     = (integer, unsigned, finite),
    lot_size   = (integer, positive, finite),
    limit      = (integer, unsigned, finite),
    price      = {
        'demand' : (rational, unsigned, finite),
        'supply' : (rational, unsigned, finite),
        'fine' : (rational, unsigned, finite),
        'storage' : (rational, unsigned, finite),
    },
    total_time = (rational, positive, finite)
)
def warehouse(demand, supply, amount, lot_size, limit, price, total_time):
    u'Склад'
    
    # Статистика
    fines    = 0 # Количество выплат неустойки
    sales    = 0 # Количество проданных единиц продукции
    supplies = 0 # Количество полученных партий
    average  = 0 # Среднее количество продукции на складе
    
    # История
    history = {
        'amount' : [(0, amount)],
        'supply' : [],
    }
    
    # Событие за границами total_time времени никогда не произойдёт
    never = delivery = total_time + 1 # float('Infinity')
    
    time = 0 # Время модели
    for delta in demand:
        time += delta
        
        # Выход за границы. Завершаем работу.
        if time > total_time:
            break
        
        average += amount * delta
        
        # Приехал новый заказ
        if delivery <= time:
            history['amount'].append((delivery, amount))
            amount += lot_size # Принимаем его
            supplies += 1
            average += (time - delivery) * lot_size # Учитываем хранение партии
            history['amount'].append((delivery, amount))
            delivery = never
        
        # На складе есть продукция
        if amount:
            amount -= 1 # Продаём блочок
            sales  += 1
            history['amount'].append((time, amount))
        else:
            fines += 1 # Выплачиваем неустойку
            #history['amount'].append((time, amount))
        
        # Если нужно - заказываем новую партию
        if amount <= limit and delivery == never:
            delivery = time + supply.next()
    
    # Обрабатываем запоздавший заказ, если он есть
    if delivery < total_time:
        history['amount'].append((delivery, amount))
        amount += lot_size
        supplies += 1
        average += (total_time - delivery) * lot_size
        history['amount'].append((delivery, amount))
        delivery = never
    
    # Переработка истории для вывода графика
    history['graph'] = {
        'x' : map(lambda x : round(x[0],2), history['amount']),
        'y' : map(lambda x : x[1], history['amount']),
        'limit'  : limit,
    }
    
    history['graph']['max'] = {
        'x' : max(history['graph']['x']),
        'y' : max(history['graph']['y']),
    }
    
    # Итоговая статистика
    return {
        'units' : {
            'supply'  : supplies,
            'sales'   : sales,
            'fine'    : fines,
            'storage' : average / total_time,
        },
        'balance' : {
            'supply'  : supplies * lot_size * price['supply'],
            'sales'   : sales    * price['demand'],
            'fine'    : fines    * price['fine'],
            'storage' : average  * price['storage'],
        },
        'history' : history,
    }

