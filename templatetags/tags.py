# -*- coding: utf-8 -*-

'Теги для шаблонов'

# Импорты
from google.appengine.ext.webapp import template
from django import template as django_template
from cgi import escape

class InputNode(django_template.Node):
    'Поле ввода'
    def __init__(self, variable):
        self.variable = escape(variable)
    
    def render(self, context):
        variable = escape(self.variable) # Имя параметра
        
        # Значение
        try:
            value = escape(django_template.resolve_variable('input.' + self.variable, context))
        except:
            value = ''
        
        # Ошибка
        try:
            error = escape(unicode(django_template.resolve_variable('errors.' + self.variable, context)))
        except:
            error = None
        
        # <input>
        input_class = 'text' + (' error' if error else '')
        input_tag = '<input class="{0}" name="{1}" id="{1}" value="{2}" />'.format(input_class, variable, value)
        
        # <div class="error"> and return result HTML
        if error:
            error_tag = '<div class="balloon" id="{0}">{1}</div>'.format(variable + '.error', error.encode('utf-8'))
            return error_tag + input_tag
        else:
            return input_tag

def input(parser, token):
    'Поле ввода'
    bits = token.split_contents()
    variable = bits[1]
    if variable[0] == variable[-1] and variable[0] in ('"', "'"):
        return InputNode(str(variable[1:-1]))
    else:
        raise Exception('In input tag, you should enclose varname in quotes!')

register = template.create_template_register()
my_tag = register.tag(input)

