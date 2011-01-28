# -*- coding: utf-8 -*-

'Обработчик HTTP-запросов'

import os, sys

def parse_args(args):
    'Превращение URL-запроса в дерево аргументов'
    from cgi import parse_qs
    args = parse_qs(args)
    
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

def process(environ):
    'Формирование содержимого страницы'
    
    # Путь к директории приложения в локальной файловой системе
    app_root = os.path.dirname(environ['SCRIPT_FILENAME'])
    sys.path.append(app_root)
    
    # Импорты
    import models, interface
    from models import validator
    
    # Аргументы модели
    if environ['REQUEST_METHOD'] == 'GET':
        args = parse_args(environ['QUERY_STRING'])
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except:
            request_body_size = 0
        
        request_body = environ['wsgi.input'].read(request_body_size)
        
        args = parse_args(request_body)
    
    # Имя модели
    path = tuple(chunk.lower() for chunk in environ['PATH_INFO'].split('/') if chunk)
    
    # Если путь не указан
    if not path:
        return interface.index()
    else:
        model_name = path[0]
    
    # Загрузка модели
    if model_name in models.__all__:
        model = getattr(__import__('models.' + model_name, fromlist = ['models']), model_name)
    else:
        return interface.notfound(model_name)

    # Нормализация аргументов (удаление лишних)
    args = validator.normalize(args, model.accepts)
    
    # Интерфейс
    view = interface.presenter(root = app_root, path = environ['SCRIPT_NAME'], model = model, accepts = model.accepts, input = args)
    
    # Аргументы пусты
    if not args:
        return view()
    
    try: # Валидация аргументов
        parameters = validator.validate(args, model.accepts)
    except Exception, errors: # Есть ошибки
        return view(errors = errors.message)
    else:
        try: # Запуск модели
            output = model(**parameters)
        except Exception, error: # Фатальная ошибка
            return view(fatal = error)
        else:
            return view(output = output)
    

def application(environ, start_response):
    'Выдача HTTP ответа'

    # Получаем содержание страницы
    output = process(environ)

    # HTTP response
    status = '200 OK'
    content_type = 'application/xhtml+xml'
    response_headers = [('Content-type', content_type),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

