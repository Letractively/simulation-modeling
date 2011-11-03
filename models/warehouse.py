# -*- coding: utf-8 -*-
'Склад'

import distributions, tree
from models.validator import *
from models.agregator import *

RPF = (rational, positive, finite)
RUF = (rational, unsigned, finite)

IUF = (integer, unsigned, finite, maximum(100000))
IPF = (integer, positive, finite, maximum(100000), minimum(0.00001))

@aggregate(mean, max_guaranteed_costs)
@accepts(
    demand     = normal_distribution(conditions = {'mu' : RPF, 'sigma' : RUF}, postprocess = (positive, inverse)),
    supply     = normal_distribution(conditions = {'mu' : RPF, 'sigma' : RUF}, postprocess = (positive,)),
    amount     = IUF,
    lot_size   = IPF,
    limit      = IUF,
    price      = {
        'supply' : RUF,
        'fine' : RUF,
        'storage' : RUF,
    },
    total_time = RPF,
)
def warehouse(demand, supply, amount, lot_size, limit, price, total_time):
    u'Склад'
    
    # Статистика
    fines    = 0 # Количество выплат неустойки
    sales    = 0 # Количество проданных единиц продукции
    supplies = 0 # Количество полученных партий
    average  = 0 # Среднее количество продукции на складе
    
    # Событие за границами total_time никогда не произойдёт
    delivery = never = total_time + 1

    time = 0 # Время модели
    for delta in demand:
        time += delta
        
        # Выход за границы. Завершаем работу.
        if time > total_time:
            time -= delta
            break
        
        average += amount * delta
        
        # Приехал новый заказ
        if delivery <= time:
            amount += lot_size # Принимаем его
            supplies += 1
            average += (time - delivery) * lot_size # Учитываем хранение партии
            delivery = never
        
        # На складе есть продукция
        if amount: # Продаём одну единицу
            amount -= 1
            sales  += 1
        else: # Продукции нет
            fines  += 1 # Выплачиваем неустойку
        
        # Если нужно - заказываем новую партию
        if amount <= limit and delivery == never:
            delivery = time + supply.next()
    
    # Учитываем в average хранение товара после последней покупки
    average += (total_time - time) * amount
    
    # Обрабатываем запоздавший заказ, если он есть
    if delivery < total_time:
        amount += lot_size
        supplies += 1
        
        average += (total_time - delivery) * lot_size
        delivery = never
    
    # Итоговая статистика
    output = {
        'units' : {
            'supply'  : supplies,
            'fine'    : fines,
            'storage' : average / total_time,
        },
        'balance' : {
            'supply'  : supplies * lot_size * price['supply'],
            'fine'    : fines    * price['fine'],
            'storage' : average  * price['storage'],
        },
    }
    
    # Затраты
    output['balance']['costs'] = sum(output['balance'].values())
    
    return output




