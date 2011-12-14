# -*- coding: utf-8 -*-

'Торговая точка'

from random import random
from math import sqrt
from distributions import normal, limited_normal

def kiosk(revenue_mean, damage_mean, damage_probability, sigma, revenue_min, revenue_max, times=1):
    
	# Потоки выручки
    revenue_streams = []
    for shop in revenue_mean:
        revenue_streams.append([])
        for mean in shop:
            revenue_streams[-1].append(limited_normal(mean, sigma * mean, mean * (1 + revenue_min * sigma), mean * (1 + revenue_max * sigma)))
    
    # Потоки случайных убытков
    damage_streams = tuple(normal(mean, sigma * mean) for mean in damage_mean)
    
    # А что если эти поток отрицательный результат дадут?
    
    # Сумматор прибыли по магазинам
    revenue_total = [0] * len(revenue_mean)
    
    # Сумматор квадратов прибыли
    revenue_squares = [0] * len(revenue_mean)
    
    # И раз, ещё раз, и ещё times, times раз...
    for _ in range(times):
        for shop, row in enumerate(revenue_streams):
            # Полная выручка
            revenue = sum(stream.next() for stream in row)
            
            # Случайный убыток
            if random() < damage_probability[shop]:
                damage = damage_streams[shop].next()
                revenue -= damage
            
            revenue_total[shop]   += revenue
            revenue_squares[shop] += revenue * revenue
    
    # Считаем среднее значение
    income_mean = tuple(s / times for s in revenue_total)
    
    # Считаем среднеквадратическое отклонение
    income_sigma = tuple(sqrt((M - times * M2) / (times - 1)) for M, M2 in zip(revenue_total, revenue_squares))
    
    # Квантиль
    K = 1.645
    max_guaranteed_costs = tuple(mean - K * sigma for mean, sigma in zip(income_mean, income_sigma))
    
    
    
