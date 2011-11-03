# -*- coding: utf-8 -*-

'Simulation modeling' # Имя приложения

# GAE API и стандартные модули
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError

# Модули приложения
import models, tree, view
from models import validator, agregator

class Handler(webapp.RequestHandler):
    def handle_exception(self, exception, debug_mode):
        logging.error(exception)
        self.response.clear()
        self.response.set_status(500)
        self.response.out.write(view.internal_error())

class MainPage(Handler):
    'Список моделей'
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        # Список моделей
        names = {}
        for name in models.__all__:
            names[name] = getattr(__import__('models.' + name, fromlist = ['models']), name).__doc__
        
        self.response.out.write(view.index(names))

class Model(Handler):
    'Модель'
    
    def request(self, name):
        
        self.response.headers['Content-Type'] = 'text/html'
        
        # Загрузка модели
        model = getattr(__import__('models.' + name, fromlist=['models']), name)
        
        title = model.__doc__
        
        # Входной запрос
        query = self.request.POST or self.request.GET
        
        if not query: # Если запрос пуст - просто выводим пустую страницу модели.
            self.response.out.write(view.model(name, title))
        else: # Необходимо обработать запрос.
            # 1. Переводим его в дерево параметров и удаляем лишние, если есть.
            raw_args = tree.from_materialized_path(query)
            raw_args = validator.normalize(raw_args, model.accepts)
            
            # 2. Проверяем и очищаем параметры.
            if not raw_args: # Если после удаления лишнего ничего не осталось -
                self.response.out.write(view.model(name, title)) # выводим пустую страницу
            else: # Проверка параметров.
                try:
                    args = validator.validate(raw_args, model.accepts)
                except Exception, error: # Валидация обнаружила ошибку error
                    args = {}
                    output = {}
                    errors = error.message # Сохраняем текст ошибки
                else: # Валидация успешна. Запускаем агрегатор, передавая ему модель.
                    errors = {}
                    try:
                        output = agregator.agregator(model, args)
                    except DeadlineExceededError:
                        logging.error('Deadline exceeded error.')
                        self.response.clear()
                        self.response.set_status(500)
                        self.response.out.write(view.internal_error())
                        return
                
                # Составляем входные данные.
                input = tree.recursive_map(
                    lambda arg, error:
                        {'value' : arg, 'error' : error} if error else arg,
                    raw_args,
                    errors
                )
                
                # Выводим страницу
                self.response.out.write(
                    view.model(name, title, input, output, self.request.body)
                )
    
    get = post = request

class Help(Handler):
    'Справочная система'
    
    def get(self, name):
        self.response.headers['Content-Type'] = 'text/html'
        
        model = getattr(__import__('models.' + name, fromlist=['models']), name)
        title = model.__doc__
        
        self.response.out.write(view.help(name, title))

class UrlShortener(Handler):
    'Обёртка для goo.gl API'
    
    def get(self, model):
        'Сокращение URL'
        
        # Получение URL модели, который должен быть сокращён
        host = self.request.host_url
        args = self.request.query
        url = '%s/%s?%s' % (host, model, args)
        
        # Вызов goo.gl
        from google.appengine.api import urlfetch
        result = urlfetch.fetch(
            url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCmKtYt1GL8F-9XXnywAHs2JzgMhm0OHzU',
            method = urlfetch.POST,
            payload = u'{ "longUrl" : "%s" }' % url,
            headers = {
                'Content-Type' : 'application/json',
            }
        )
        if result.status_code == 200:
            response = result.content
        else:
            raise Exception(result.status_code)
        
        # Парсинг
        from django.utils import simplejson as json
        shortUrl = json.loads(response)['id']
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(view.shorten(shortUrl))

class NotFound(Handler):
    'Страница не найдена'
    
    def get(self, url):
        self.response.clear()
        self.response.set_status(404)
        logging.error('Page "%s" was not found.' % url)
        self.response.out.write(view.notfound())

# Определение списка страниц
model_list = '|'.join(models.__all__)
routes = [
    ('/', MainPage),
    ('^/url/(%s)/*' % model_list, UrlShortener),
    ('^/help/(%s)/*' % model_list, Help),
    ('^/(%s)/*' % model_list, Model),
    ('^/*$', MainPage),
    ('^(.*)$', NotFound),
]

# Запуск приложения
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

