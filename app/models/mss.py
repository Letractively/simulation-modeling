# -*- coding: utf-8 -*-

'Система массового обслуживания'

import random, math, distributions
from models.validator import *

@accepts(
        channelsCount=(int, unsigned), # Количество каналов

        queue={     # Очередь
               'size': (int, unsigned), # Максимальный размер очереди
               'time': (float, unsigned), # Максимальное время ожидания в очереди
               },

        streams={   # Потоки
                 'in':  distribution(), # Входной поток заявок
                 'out': distribution(), # Выходной поток обслуживаний
                 },

        faults={    # Неисправности
                'problems': (float, positive), # Поток неисправностей
                'repairs':  (float, finite, positive), # Поток ремонтов
                'destructive': probability, # Доля аварий
                },

        totalTime=(float, positive), # Продолжительность моделирования
        )
def mss(channelsCount, queue, streams, faults, totalTime):
    u'Система массового обслуживания'

    # Потоки
    in_stream = streams['in']
    out_stream = streams['out']

    fault_stream = distributions.exponential(faults['problems'])
    repair_stream = distributions.exponential(faults['repairs'])

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
        free = [key for key, value in enumerate(orders) if value == Infinity and 1 <= key <= channelsCount]

        # Выбор случайного канала
        channel = random.choice(free)

        # Время обработки заявки
        orders[channel] = time + next(out_stream)

    @action(state=increment)
    def sit(time):
        'Отправка заявки в очередь'
        orders.append(time + queue['time'])

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
        orders.pop(channelsCount + 1)

    @action(state=decrement)
    def timeout(time):
        'Уход элемента из очереди по таймауту'
        orders.pop(channelsCount + 1)

    @action()
    def fault(time, destructive):
        'Неисправность'

        if not mss.state:
            return # Авария проходит без последствий, если нет заявок в обработке

        # Занятые каналы
        busy = [index for index, value in enumerate(orders) if 1 <= index <= channelsCount and value < Infinity]

        # Выбор канала, на котором происходит авария
        channel = random.choice(busy)

        # Заявка ожидает ремонта оборудования
        orders[channel] += next(repair_stream)

        if destructive: # Если случилась авария,
            orders[channel] += next(out_stream) # Заявка ещё и обрабатывается заново

        # События

    def onNew(time):
        'Появление новой заявки'

        if mss.state < channelsCount: # Если есть пустые каналы,
            accept(time) # то принимаем заявку;
        elif mss.state < channelsCount + queue['size']: # если их нет, но есть места в очереди -
            sit(time) # направляем её в очередь.
        else: # если же и очередь забита -
            sizeout(time) # отвергаем заявку.

    def onLeave(time, channel):
        'Канал channel освобождается заявкой'
        leave(time, channel) # Заявка уходит из канала
        if mss.state + 1 > channelsCount: # Если очередь непуста...
            stand(time) # то из очереди вызывается первая заявка
            accept(time) # и уходит на выполнение

    def onTimeout(time):
        'Уход заявки из очереди по таймауту'
        timeout(time)

    def onDispatch(*args):
        'Редирект на нужный обработчик события'
        onDispatch.route(*args)
        orders[0] = next(eventStream)

    def onFault(time):
        'Неисправность'
        fault(time, random.random() <= faults['destructive'])

    def inputCombinator():
        'Комбинация генераторов'

        # Время последней заявки и последней неисправности
        new, fault = next(in_stream), next(fault_stream)

        while True:
        # Время следующей заявки и следующей неисправности
            if new < fault:
                onDispatch.route = onNew
                yield new
                new += next(in_stream)
            else:
                onDispatch.route = onFault
                yield fault
                fault += next(fault_stream)

            # Бесконечность

    Infinity = float('Infinity')

    # Поток событий - заявок и аварий
    eventStream = inputCombinator()

    # Время последнего изменения состояния
    mss.prevTime = 0

    # Структура, хранящая местоположение заявок и операции над ними.
    orders = [next(eventStream)] + [Infinity] * channelsCount

    # Состояние
    mss.state = 0
    mss.states = []

    while True:
    # Тип и значение следующего события
        event = min(range(len(orders)), key=orders.__getitem__)
        time = orders[event]

        # Ограничение времени жизни модели
        if time > totalTime:
            break

        if event:
            if event <= channelsCount: # Завершена обработка заявки
                onLeave(time, event)
            else: # Заявка уходит из очереди по таймауту
                onTimeout(time)
        else: # Независимое событие (новая заявка или неисправность)
            onDispatch(time) # уходит на диспетчеризацию.

        # Время истекло, но в обработке и в очереди ещё могли остаться заявки.
    mss.actions['shutdown'] = mss.state

    # Качество работы СМО
    rejectedFields = (  # Заявки, отклонённые:
                        'timeout', # По таймауту
                        'sizeout', # По размеру очереди
                        'shutdown',         # По окончанию рабочего времени
    )

    # Количество заявок, отменённых по каждой из причин
    absolute = {}
    for field in rejectedFields:
        absolute[field] = mss.actions[field]

    # Все отменённые заявки
    absolute['reject'] = sum(absolute.values())

    # Принятые заявки и все заявки, прошедшие через систему
    absolute['accept'] = mss.actions['accept']
    absolute['total'] = absolute['reject'] + absolute['accept']

    # Значения в процентах
    relative = {}
    for key, value in absolute.items():
        if key != 'total':
            relative[key] = round(value / float(absolute['total']) * 100, 2)

        # Среднее количество занятых каналов
    km = 0
    for channel, time in enumerate(mss.states):
        km += channel * time if channel <= channelsCount else channelsCount * time
    km /= totalTime

    # Среднее время пребывания заявки
    import operator

    times = {}

    orderTime = sum(orders * time for orders, time in enumerate(mss.states))
    queueTime = sum(time * orders for orders, time in enumerate(mss.states[channelsCount:]))

    if absolute['total']: # В системе
        times['total'] = round(orderTime / absolute['total'], 3)

    if mss.actions['sit']: # В очереди
        times['queue'] = round(queueTime / mss.actions['sit'], 3)

    # Среднее количество заявок
    orders = {'work': round(km, 3)}
    orders['total'] = round(orderTime / totalTime, 3)
    orders['queue'] = round(queueTime / totalTime, 3)

    # Результаты работы
    states = tuple(round(duration / totalTime * 100, 3) for duration in mss.states)
    return {
        'quality': {
            'abs': absolute,
            'pc': relative,
        },
        'load': {
            'states': states,
            'longestState': max(states),
            'times': times,
            'orders': orders,
        },
        'faults': mss.actions['fault'],
    }

