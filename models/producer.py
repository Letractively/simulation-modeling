# -*- coding: utf-8 -*-

'Производственная фирма'

import distributions
from validator import *

@accepts(
    in_stream  = (float, positive),
    mu         = array(float),
    sigma      = (float, unsigned),
    price      = (float, unsigned),
    cost       = (float, unsigned),
    total_time = (float, positive)
)
def producer(in_stream, mu, sigma, price, cost, total_time):
    u'Производственная фирма'
    
    # Генераторы событий
    work = [distributions.normal(mean, mean * sigma) for mean in mu]
    
    # Технологическая цепочка
    chain = [[] for mean in mu]
    
    ENVIRONMENT = -1 # Новая заявка
    
    def event_stream():
        'Поток событий'
        timer = distributions.exponential(in_stream)
        
        # Время появления следующей заявки
        next_order = next(timer)
        
        while True:
            time, source = next_order, ENVIRONMENT
            
            for link, queue in enumerate(chain):
                if queue and queue[0] < time:
                    time, source = queue[0], link
            
            if source == ENVIRONMENT:
                next_order += next(timer)
            
            # Если закончилось время, выходим
            if time >= total_time:
                return
            
            # Иначе возвращаем результат
            yield (time, source)
    
    def process(time, source):
        'Переход заявки в следующее звено технологической цепи'
        
        # Обработка канала-источника
        if source > ENVIRONMENT:
            chain[source].pop(0)
            if chain[source]:
                duration = next(work[source])
                chain[source][0] = time + duration
        
        # Обработка канала-приёмника
        dest = source + 1
        if dest < len(chain):
            chain[dest].append(time)
            if len(chain[dest]) == 1:
                duration = next(work[dest])
                chain[dest][0] += duration
        else:
            orders['processed'] += 1
    
    orders = {'processed' : 0}
    
    events = event_stream()
    # Основной цикл
    for event in events:
        process(*event)
    
    # Статистика заявок
    orders['rejected'] = sum(map(len, chain))
    orders['total']    = sum(orders.values())
    
    return {
        'factor' : round((max(mu) - min(mu)) / (sum(mu) / len(mu)), 3),
        'profit' : round(orders['processed'] * price - cost, 2),
        'orders' : orders,
    }



