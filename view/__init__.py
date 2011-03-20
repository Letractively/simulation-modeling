# -*- coding: utf-8 -*-

# Импорт и настройка Jinja2
from jinja2 import Environment, PackageLoader
templates = Environment(loader=PackageLoader('view', 'templates'))

from settings import app

def permalink(host, query):
    'Ссылка' # Функция не работает, найти - почему
    from cgi import escape

    return escape('%s?%s' % (
        host,
        '&'.join('='.join(pair) for pair in query.items())
    ), quote = True)

def index(names):
    'Главная страница'
    template = templates.get_template('index.html')
    return template.render(app = app, models = names)

def help(name, title):
    'Страница справки'
    template = templates.get_template('help.html')
    return template.render(app = app, name = name, title = title)

def model(name, title, input = {}, output = {}, query = {}):
    'Страница модели'
    template = templates.get_template(name + '.html')
    return template.render(app = app, name = name, title = title, input = input, output = output)

