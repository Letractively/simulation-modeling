# -*- coding: utf-8 -*-

'Производственная фирма'

import distributions
from validator import *

U = (rational, unsigned, finite)
P = (rational, positive, finite)
@accepts(
    instream  = P,
    operations = array(*P),
    deviation  = P,
    income     = U,
    costs      = U,
    salary     = U,
    total_time = P,
)
def producer(instream, operations, deviation, income, costs, salary, total_time):
    u'Производственная фирма'
    
    # Генераторы событий
    work = [distributions.normal(mean, mean * deviation) for mean in operations]
    
    # Технологическая цепочка
    chain = [[] for mean in operations]
    
    ENVIRONMENT = -1 # Новая заявка
    
    # Статистика количества заявок
    statistics = [0] * len(operations)
    
    def event_stream():
        'Поток событий'
        timer = distributions.exponential(instream)
        
        # Время появления следующей заявки
        next_order = timer.next()
        
        while True:
            time, source = next_order, ENVIRONMENT
            
            for link, queue in enumerate(chain):
                if queue and queue[0] < time:
                    time, source = queue[0], link
            
            if source == ENVIRONMENT:
                next_order += timer.next()
            
            # Если закончилось время, выходим
            if time >= total_time:
                return
            
            # Иначе возвращаем результат
            yield (time, source)
    
    def process(time, source):
        'Переход заявки в следующее звено технологической цепи'
        
        # Предыдущее событие
        try:
            delta = time - process.previous_time
            process.previous_time = time
        except:
            delta = process.previous_time = time
        
        # Статистика
        for link, queue in enumerate(chain):
            statistics[link] += len(queue) * delta
        
        # Обработка канала-источника
        if source > ENVIRONMENT:
            chain[source].pop(0)
            if chain[source]:
                duration = work[source].next()
                chain[source][0] = time + duration
        
        # Обработка канала-приёмника
        dest = source + 1
        if dest < len(chain):
            chain[dest].append(time)
            if len(chain[dest]) == 1:
                duration = work[dest].next()
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
    
    # Прибыли и убытки
    balance = dict(
        (key, round(orders * income, 2))
        for key, orders in orders.items() if key != 'total'
    )
    balance['total'] = balance['processed'] - costs - salary * len(operations)
    
    # Статистика очередей
    queues = tuple(item / total_time for item in statistics)
    
    return {
        'factor' : round((max(operations) - min(operations)) / (sum(operations) / len(operations)), 3),
        'balance' : balance,
        'quality' : {
            'abs' : orders,
            'pc'  : dict(
                (key, round(value / float(orders['total']) * 100, 2)) for key, value in orders.items()
            ),
        },
        'queues' : queues,
        'max_queue' : max(queues),
    }


