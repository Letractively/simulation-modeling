# -*- coding: utf-8 -*-

# Импорт и настройка Jinja2
from jinja2 import Environment, PackageLoader
templates = Environment(loader=PackageLoader('view', 'templates'), extensions = ['jinja2.ext.with_'])

from GChartWrapper import Pie, Line, LineXY

from settings import app

def index(names):
    'Главная страница'
    template = templates.get_template('index.html')
    return template.render(app = app, models = names)

def help(name, title):
    'Страница справки'
    template = templates.get_template('help/%s.html' % name)
    return template.render(app = app, name = name, title = title)

def mss(*a, **kw):
    'Страница модели массового обслуживания'
    
    if 'output' in kw and kw['output']['requests']['total']:
        # Генерация диаграммы баланса заявок
        requests = kw['output']['requests']
        
        # Исходные данные
        data = []
        
        for key in ('timeout', 'sizeout', 'shutdown'):
            data.append(round(requests['denied'][key], 2))
        
        data.append(round(requests['accepted'], 2))
        
        # Цвета
        colors = ('FBFF53', '1560BD', 'FF4D6F', '008090')
        
        # Заголовки
        labels = [str(round(value / requests['total'] * 100, 2)) + '%' for value in data]
        
        # Размер
        sizes = [250, 160]
        
        kw['output']['requests_diagram'] = Pie(data).color(*colors).label(*labels).size(*sizes).scale(0, sum(data)).img(alt=u'Количество заявок')
        
        if kw['output']['balance']['accepted']:
            # Генерация диаграммы выручки
            balance = kw['output']['balance']
            data = [balance['income'], balance['repairs'], balance['costs']]
            colors = ['8F007E', '000000', '999999']
            labels = [str(round(value / balance['accepted'] * 100, 2)) + '%' for value in data]
            sizes[1] = 80
            
            kw['output']['income_diagram'] = Pie(data).color(*colors).label(*labels).size(*sizes).scale(0, sum(data)).img(alt=u'Распределение выручки')
    
        # Генерация диаграммы загрузки
        data = kw['output']['workload']
        sizes = [560, 180]
        
        diagram = Line(data).scale(0, round(max(data), 3)).size(sizes).color('1560BD')
        diagram['chm'] = 'B,008090,0,0,0|B,FF4D6F,0,%s:,0' % (kw['form'].data['channels_count'])
        
        diagram.axes.type('xxy')
        diagram.axes.label(1, '', 'Количество заявок в системе', '')
        
        y_labels_count = 4
        diagram.axes.label(2, *(str(round(max(data) / (y_labels_count - 1) * n, 2)) + '%' for n in range(y_labels_count)))
        
        diagram.axes.range(0, 0, len(data) - 1)
        
        kw['output']['workload_diagram'] = diagram.img(alt=u'Вероятностное распределение количества заявок в системе', style='margin-top: 18px')
    
    return model(*a, **kw)

def warehouse(*args, **kwargs):
    'Модель склада'
    
    if not kwargs.get('output', False):
        return model(*args, **kwargs)
    
    
    
    # Генерация диаграммы баланса
    if kwargs['output']['balance']['sales'] > 0 and kwargs['output']['balance']['profit'] > 0:
        balance = kwargs['output']['balance']

        data = [round(balance[field], 2) for field in ('supplies', 'storage', 'fines', 'profit')]
        colors = ('FBFF53', '1560BD', 'FF4D6F', '008090')
        labels = [str(round(value / balance['sales'] * 100, 2)) + '%' for value in data]
        sizes = [250, 160]

        kwargs['output']['balance_diagram'] = Pie(data).color(*colors).label(*labels).size(*sizes).scale(0, balance['sales']).img(alt=u'Диаграмма баланса')
    
    history = kwargs['output']['history']
    if history:
        # Генерация диаграммы истории
        
        # Абсциссы и ординаты
        x, y = zip(*history)
        
        sizes = [560, 180]
        diagram = LineXY([x, y]).size(sizes).scale(0, max(x), 0, max(y)).color('1560BD')
        diagram['chm'] = 'B,1560BD,0,:,0'
        
        diagram.axes.type('xxy')
        diagram.axes.range(0, 0, max(x))
        diagram.axes.range(2, 0, max(y))
        diagram.axes.label(1, '', 'Время, ч', '')
        
    
        kwargs['output']['history_diagram'] = diagram.img()
    
    return model(*args, **kwargs)

def model(name, title, form=None, output={}, query=''):
    'Страница модели'
    template = templates.get_template(name + '.html')
    
    # Ссылка
    shorten = '/url/%s?%s' % (name, query) if query else None
    
    return template.render(app=app, name=name, title=title, form=form, shorten=shorten, output=bool(output), **output)

def shorten(url):
    'Укорочение URL'
    
    template = templates.get_template('shorten.html')
    return template.render(url=url)

def notfound():
    'Страница не найдена'
    template = templates.get_template('notfound.html')
    return template.render(app=app, title=u'Страница не найдена')

def internal_error():
    'Внутренняя ошибка'
    template = templates.get_template('internal_error.html')
    return template.render(app=app, title=u'Внутренняя ошибка')

