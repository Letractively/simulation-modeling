# -*- coding: utf-8 -*-

'Основной файл - обработчик запросов'

# GAE API и стандартные библиотеки
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os, cgi

# Подключение шаблонов
template.register_template_library('templatetags.tags')

# Константы
settings = {
    'app' : {
        'name' : 'Simulation Modeling', # Полное имя приложения
        'short' : 'SM',                     # Краткая аббревиатура
    },
}

# Модули приложения
import models
from models import validator

def args_tree(args):
    'Превращение списка аргументов в дерево'
    
    tree = {}
    for arg, value in args.items():
        path = arg.split('.')
        
        layer = tree
        for token in path[:-1]:
            if token not in layer or type(layer[token]) != dict:
                layer[token] = {}
            layer = layer[token]
    
        if len(value) == 1:
            value = value[0]
        layer[path[-1]] = value
    
    return tree

class MainPage(webapp.RequestHandler):
    'Список моделей'
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        # Список моделей
        settings['models'] = {}
        for name in models.__all__:
            settings['models'][name] = getattr(__import__('models.' + name, fromlist = ['models']), name).__doc__
        
        self.response.out.write(template.render('templates/index.html', settings))

class Model(webapp.RequestHandler):
    'Модель'
    
    def request(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        # Имя модели. FIXME некрасиво, на путях с аргументами не сработает.
        name = self.request.path.split('/')[-1]
        
        # Загрузка модели
        model = getattr(__import__('models.' + name, fromlist = ['models']), name)
        title = model.__doc__
        
        template_file = 'templates/%s.html' % name
        template_parameters = { 'app' : settings['app'], 'title' : title }
        if self.request.postvars:
            # Аргументы моделирования
            args = args_tree(self.request.postvars)
            
            # Нормализация аргументов (удаление лишних)
            args = validator.normalize(args, model.accepts)
            
            # Валидация аргументов
            if args:
              try:
                  parameters = validator.validate(args, model.accepts)
              except Exception, error:
                  errors = error.message
                  template_parameters['errors'] = errors
              else:
                template_parameters['output'] = model(**parameters)
            
            #self.response.out.write(cgi.escape(str(self.request.postvars)))
            template_parameters['input'] = args

        self.response.out.write(template.render(template_file, template_parameters))
    
    get = post = request

# Определение списка моделей
routes = [('/', MainPage)] + [('/' + model, Model) for model in models.__all__]

# Запуск приложения
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
