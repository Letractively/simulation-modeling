# -*- coding: utf-8 -*-
'Склад'

import distributions, tree
from models.aggregator import aggregate, max_guaranteed_costs

@aggregate(max_guaranteed_costs)
def warehouse(lot_size, limit, amount, total_time, demand_mu, demand_sigma, supply_mu, supply_sigma, demand_price, supply_price, storage_price, fine, times=1):
    u'Склад'
    
    # Потоки
    stream = distributions.filter(lambda x: x > 0, distributions.normal)
    
    demand = distributions.inverse(stream(demand_mu, demand_sigma))
    supply = stream(supply_mu, supply_sigma)
    
    # Цены
    price = {
        'supplies': supply_price,
        'sales': demand_price,
        'storage': storage_price,
        'fines': fine,
    }
    
    # Статистика
    fines    = 0 # Количество выплат неустойки
    sales    = 0 # Количество проданных единиц продукции
    supplies = 0 # Количество полученных партий
    storage  = 0 # Среднее количество продукции на складе
    
    # Лог
    history = [(0, amount)]
    
    # Событие за границами total_time никогда не произойдёт
    delivery = never = total_time + 1

    time = 0 # Время модели
    for delta in demand:
        time += delta
        
        # Выход за границы. Завершаем работу.
        if time > total_time:
            time -= delta
            break
        
        storage += amount * delta
        
        # Приехал новый заказ
        if delivery <= time:
            history.append((delivery, amount))
            amount += lot_size # Принимаем его
            supplies += 1
            storage += (time - delivery) * lot_size # Учитываем хранение партии
            history.append((delivery, amount))
            delivery = never
        
        # На складе есть продукция
        if amount: # Продаём одну единицу
            amount -= 1
            sales  += 1
            if not amount:
                history.append((time, amount))
        else: # Продукции нет
            fines  += 1 # Выплачиваем неустойку
        
        # Если нужно - заказываем новую партию
        if amount <= limit and delivery == never:
            delivery = time + supply.next()
    
    # Учитываем в storage хранение товара после последней покупки
    storage += (total_time - time) * amount
    
    # Обрабатываем запоздавший заказ, если он есть
    if delivery < total_time:
        history.append((delivery, amount))
        amount += lot_size
        supplies += 1
        history.append((delivery, amount))
        
        storage += (total_time - delivery) * lot_size
        delivery = never
    
    history.append((total_time, amount))
    
    # Окончательная статистика
    
    units = {
        'sales': sales,
        'supplies': supplies * lot_size,
        'fines': fines,
        'storage': storage / total_time,
    }
    
    balance = {}
    for item, value in units.items():
        balance[item] = value * price[item]
    
    balance['storage'] *= total_time
    
    cost_fields = ['supplies', 'fines', 'storage']
    
    balance['costs'] = 0
    for field in cost_fields:
        balance['costs'] += balance[field]
    
    balance['profit'] = balance['sales'] - balance['costs']
    
    return {
        'units': units,
        'balance': balance,
        'history': history if times == 1 else [],
    }
    
    
