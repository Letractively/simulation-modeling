# -*- coding: utf-8 -*-

'Simulation modeling' # Имя приложения

# GAE API и стандартные модули
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Модули приложения
import models, tree, view
from models import validator, agregator

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
                    output = agregator.agregator(model, args)
                
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

class Help(webapp.RequestHandler):
    'Справочная система'
    
    def get(self, name):
        self.response.headers['Content-Type'] = 'text/html'
        
        model = getattr(__import__('models.' + name, fromlist=['models']), name)
        title = model.__doc__
        
        self.response.out.write(view.help(name, title))

class UrlShortener(webapp.RequestHandler):
    'Обёртка для goo.gl API'
    
    def get(self):
        'Сокращение URL'
        
        # Получение URL модели, который должен быть сокращён
        model = self.request.path.split('/')[-1]
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
        
        self.response.out.write(view.shorten(shortUrl))


# Определение списка страниц
routes = [
    ('/', MainPage),
    (r'^/url/', UrlShortener),
    (r'^/help/([^/]*)/*', Help),
    (r'^/([^/]+)', Model),
]

# Запуск приложения
application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

