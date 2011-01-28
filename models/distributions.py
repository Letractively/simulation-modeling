# -*- coding: utf-8 -*-

'Генераторы случайных величин с различными распределениями'

import random, math

def normal(mu, sigma, **extra):
  '''Нормальное распределение.
  
  mu - математическое ожидание, а sigma - стандартное (среднеквадратическое)
  отклонение.
  
  Возвращает генератор бесконечной последовательности случайных чисел.
  '''
  
  while True:
    yield random.gauss(mu, sigma)

def limitedNormal(mu, sigma, minimum, maximum, **extra):
  '''Усечённое нормальное распределение.
  
  mu - математическое ожидание, sigma - стандартное (среднеквадратическое)
  отклонение, minimum и maximum - границы значения случайной величины.
  Возвращает генератор бесконечной последовательности случайных чисел.
  '''
  
  while True:
    x = random.gauss(mu, sigma)
    if minimum < x < maximum:
      yield x

def equal(a, b):
    'Равномерное распределение от a до b, a < b'

    if a > b:
        a, b = b, a

    scale = b - a
    while True:
        yield (a + random.random() * scale)


def exponential(mean):
  '''Экспоненциальное распределение.
  mean - среднее значение.'''

  while True:
    yield - math.log(random.random()) * float(mean)

