# -*- coding: utf-8 -*-

'Simulation modeling' # Имя приложения

# GAE API и стандартные модули
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Модули приложения
import models, tree, view
from models import validator

class MainPage(webapp.RequestHandler):
    'Список моделей'
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        # Список моделей
        names = {}
        for name in models.__all__:
            names[name] = getattr(__import__('models.' + name, fromlist = ['models']), name).__doc__
        
        self.response.out.write(view.index(names))

class Model(webapp.RequestHandler):
    'Модель'
    
    def request(self):
        self.response.headers['Content-Type'] = 'text/html'

        # Имя модели
        name = self.request.path.split('/')[-1]
        
        # Загрузка модели
        model = getattr(__import__('models.' + name, fromlist = ['models']), name)
        title = model.__doc__
        
        # Входные параметры
        parameters = self.request.POST or self.request.GET
        if parameters:
            # Аргументы моделирования
            args = tree.from_materialized_path(parameters)
            
            # Нормализация аргументов (удаление лишних)
            args = validator.normalize(args, model.accepts)
            
            # Валидация аргументов
            errors = {}
            if args:
              try:
                  parameters = validator.validate(args, model.accepts)
              except Exception, error:
                  errors = error.message
                  output = {}
              else:
                  output = model(**parameters)
            
            # Входные параметры
            input = tree.recursive_map(lambda arg, error: {'value' : arg, 'error' : error} if error else arg, args, errors)
            
            self.response.out.write(view.model(name, title, input, output))
        else:
            self.response.out.write(view.model(name, title))
    
    get = post = request

# Определение списка моделей
routes = [('/', MainPage)] + [('/' + model, Model) for model in models.__all__]

# Запуск приложения
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

