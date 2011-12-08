# -*- coding: utf-8 -*-

'Система массового обслуживания'

import random, math, distributions, tree
from models.aggregator import aggregate

@aggregate()
def mss(channels_count, in_stream, out_stream, cost, total_time, queue_size=None, queue_time=None, fault_stream=None, repair_stream=None, destructive=None, repair_cost=None, times=1):
    u'Система массового обслуживания'
    
    Infinity = float('inf')
    
    if queue_size is None:
        queue_size = Infinity
    
    if queue_time is None:
        queue_time = Infinity
    
    if fault_stream is None:
        fault_stream = Infinity
    
    if repair_stream is None:
        repair_stream = 0
    
    if destructive is None:
        destructive = 0
    
    if repair_cost is None:
        repair_cost = 0
    
    stream = distributions.filter(lambda x: x > 0, distributions.exponential)
    
    in_stream = stream(1.0 / in_stream)
    out_stream = stream(1.0 / out_stream)
    
    fault_stream = stream(fault_stream)
    repair_stream = stream(repair_stream)
    
    # Действия
    mss.actions = {}

    increment, decrement = 1, -1

    def action(state=0):
        def mix(f):
            key = f.__name__
            mss.actions[key] = 0

            def spice(*args):
                result = f(*args)

                mss.actions[key] += 1 # Статистика

                # Состояние
                duration = (args[0] - mss.prevTime)
                try:
                    mss.states[mss.state] += duration
                except:
                    mss.states.append(duration)

                mss.prevTime = args[0]
                mss.state += state

                return result

            return spice

        return mix

    @action(state=increment)
    def accept(time):
        'Принять заявку в обработку'

        # Поиск свободного канала
        free = [key for key, value in enumerate(orders) if value == Infinity and 1 <= key <= channels_count]

        # Выбор случайного канала
        channel = random.choice(free)

        # Время обработки заявки
        orders[channel] = time + out_stream.next()

    @action(state=increment)
    def sit(time):
        'Отправка заявки в очередь'
        orders.append(time + queue_time)

    @action()
    def sizeout(time):
        'Отклонение заявки по размеру очереди'

    @action(state=decrement)
    def leave(time, channel):
        'Окончание обслуживания заявки'
        orders[channel] = Infinity

    @action(state=decrement)
    def stand(time):
        'Удаление первого элемента из очереди'
        orders.pop(channels_count + 1)

    @action(state=decrement)
    def timeout(time):
        'Уход элемента из очереди по таймауту'
        orders.pop(channels_count + 1)

    @action()
    def fault(time, destructive):
        'Неисправность'

        if not mss.state:
            return # Авария проходит без последствий, если нет заявок в обработке

        # Занятые каналы
        busy = [index for index, value in enumerate(orders) if 1 <= index <= channels_count and value < Infinity]

        # Выбор канала, на котором происходит авария
        channel = random.choice(busy)

        # Заявка ожидает ремонта оборудования
        orders[channel] += repair_stream.next()

        if destructive: # Если случилась авария,
            orders[channel] += out_stream.next() # Заявка ещё и обрабатывается заново
            mss.actions['destructive_fault'] = mss.actions.get('destructive_fault', 0) + 1

    # События

    def onNew(time):
        'Появление новой заявки'

        if mss.state < channels_count: # Если есть пустые каналы,
            accept(time) # то принимаем заявку;
        elif mss.state < channels_count + queue_size: # если их нет, но есть места в очереди -
            sit(time) # направляем её в очередь.
        else: # если же и очередь забита -
            sizeout(time) # отвергаем заявку.

    def onLeave(time, channel):
        'Канал channel освобождается заявкой'
        leave(time, channel) # Заявка уходит из канала
        if mss.state + 1 > channels_count: # Если очередь непуста...
            stand(time) # то из очереди вызывается первая заявка
            accept(time) # и уходит на выполнение

    def onTimeout(time):
        'Уход заявки из очереди по таймауту'
        timeout(time)

    def onDispatch(*args):
        'Редирект на нужный обработчик события'
        onDispatch.route(*args)
        orders[0] = eventStream.next()

    def onFault(time):
        'Неисправность'
        fault(time, random.random() <= destructive)

    def inputCombinator():
        'Комбинация генераторов'

        # Время последней заявки и последней неисправности
        new, fault = in_stream.next(), fault_stream.next()

        while True:
        # Время следующей заявки и следующей неисправности
            if new < fault:
                onDispatch.route = onNew
                yield new
                new += in_stream.next()
            else:
                onDispatch.route = onFault
                yield fault
                fault += fault_stream.next()

            # Бесконечность

    Infinity = float('Infinity')

    # Поток событий - заявок и аварий
    eventStream = inputCombinator()

    # Время последнего изменения состояния
    mss.prevTime = 0

    # Структура, хранящая местоположение заявок и операции над ними.
    orders = [eventStream.next()] + [Infinity] * channels_count

    # Состояние
    mss.state = 0
    mss.states = []

    while True:
    # Тип и значение следующего события
        event = min(range(len(orders)), key=orders.__getitem__)
        time = orders[event]

        # Ограничение времени жизни модели
        if time > total_time:
            break

        if event:
            if event <= channels_count: # Завершена обработка заявки
                onLeave(time, event)
            else: # Заявка уходит из очереди по таймауту
                onTimeout(time)
        else: # Независимое событие (новая заявка или неисправность)
            onDispatch(time) # уходит на диспетчеризацию.

    # Время истекло, но в обработке и в очереди ещё могли остаться заявки.
    mss.actions['shutdown'] = mss.state

    # Сбор статистики.
    # Сначала собирается баланс доходов и расходов. Он имеет следующую
    # структуру:
    # - Все прошедшие через систему заявки
    #   - Принятые
    #   - Не принятые
    #       - По размеру очереди
    #       - По времени ожидания
    #       - По рабочему времени
    
    denied = dict((field, mss.actions[field]) for field in ('sizeout', 'timeout', 'shutdown'))
    denied['total'] = sum(denied.values())
    
    requests = {
        'denied': denied,
        'accepted': mss.actions['accept'],
        'total': mss.actions['accept'] + denied['total'],
    }
    
    # Теперь следующий шаг - статистика по балансу. Она имеет точно такую же
    # структуру, но добавляется пункт costs -- затраты на обслуживание системы,
    # заданные функцией от количества каналов.
    balance = tree.recursive_map(lambda x: x * cost, requests)
    
    balance['repairs'] = mss.actions['fault'] * repair_cost
    
    costs_function  = lambda n: 1 - 0.5 * n + 0.5 * n * n
    costs = costs_function(channels_count)
    
    balance['costs'] = costs
    balance['income'] = balance['accepted'] - costs - balance['repairs']
    
    balance['relative_income'] = requests['accepted'] - costs / cost
    
    # Теперь статистика по загрузке каналов и очереди -- распределение
    # вероятностей состояний системы. Для каждого из состояний указывается
    # вероятность пребывания системы в нём.
    workload = [time / total_time * 100 for time in mss.states]
    
    workload_mean = sum(n * p / total_time for n, p in enumerate(mss.states))
    
    output = {
        'requests': requests,
        'balance': balance,
        'workload': workload,
        'workload_mean': workload_mean,
        'workload_mean_probability': workload[int(round(workload_mean))],
    }
    
    if mss.actions['fault']:
        output['faults'] = {
            'total': mss.actions['fault'],
            'fatal': mss.actions.get('destructive_fault', 0),
        }
    
    return output

