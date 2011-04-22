# -*- coding: utf-8 -*-

# Импорт и настройка Jinja2
from jinja2 import Environment, PackageLoader
templates = Environment(loader=PackageLoader('view', 'templates'), extensions = ['jinja2.ext.with_'])

from settings import app

def index(names):
    'Главная страница'
    template = templates.get_template('index.html')
    return template.render(app = app, models = names)

def help(name, title):
    'Страница справки'
    template = templates.get_template('help.html')
    return template.render(app = app, name = name, title = title)

def model(name, title, input = {}, output = {}, shorten = None):
    'Страница модели'
    template = templates.get_template(name + '.html')
    return template.render(app = app, name = name, title = title, input = input, output = output, shorten = '/url/%s?%s' % (name, shorten.replace('&', '&amp;')) if shorten else None)

def shorten(url):
    'Укорочение URL'
    
    template = templates.get_template('shorten.html')
    return template.render(url = url)

