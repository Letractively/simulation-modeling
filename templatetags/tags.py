# -*- coding: utf-8 -*-

'Теги для шаблонов'

# Импорты
from google.appengine.ext.webapp import template
from django import template as django_template
import cgi

escape = lambda value: cgi.escape(value, quote = True)
register = template.create_template_register()

def tag(name, value, attributes):
    'Сборка HTML-тега'
    
    attributes = u' ' + u' '.join(u'%s="%s"' % (key, value) for key, value in attributes.items())
    
    return (u'<%s%s>%s</%s>' % (name, attributes, value, name)).encode('utf-8')

class InputNode(django_template.Node):
    'Класс поля ввода <input>'
    
    def __init__(self, variable, name):
        'Компиляция'
        self.variable = escape(variable)
        self.name  = name
    
    def render(self, context):
        'Вывод'
        
        #return str(dir(django_template))
        
        def resolve(v):
            try:
                if v[0] == '"' and v[-1] == '"':
                    return escape(v[1:-1])
                else:
                    return django_template.resolve_variable(v, context)
            except:
                return u'nafig'
        
        # Извлечение значения
        value = resolve(self.variable)

        if hasattr(self.name, '__iter__'):
            name = ''.join(map(unicode, map(resolve, self.name)))
        else:
            name = resolve(self.name)
        
        # Атрибуты тега
        attributes = {
            'id'    : name, 'name' : name,
            'class' : 'text',    'type' : 'text',
        }
        
        # Есть ли ошибка?
        try:
            error = value['error']
        except:
            error = None
        else:
            attributes['class'] += ' error'
            value = value['value']
            error = tag('div', error, {'class' : 'balloon', 'id' : name + '.error'})
        
        attributes['value'] = value
        field = tag('input', '', attributes)
        
        if error:
            return error + field
        else:
            return field


class DistributionNode(django_template.Node):
    'Распределение'
    def __init__(self, label, variable):
        self.variable = escape(variable)
        self.label = escape(label)
    
    def render(self, context):
        # Available distributions
        distributions = {
            'exponential' : 'Экспонента',
            'normal' : 'Нормальный',
            'equal' : 'Равномерный',
        }
        
        # Bunch of <option> tags
        selected = ' selected="selected"'
        try:
            current = escape(unicode(django_template.resolve_variable('input.' + self.variable + '.type', context)))
        except:
            current = 'exponential'

        options = ''.join('<option value="%s"%s>%s</option>' % (name, selected if name == current else '', label) for name, label in distributions.items())
        
        # <select> tag
        select = '<select id="%s.type" name="%s.type" onchange="distribution_switch(this)">%s</select>' % (self.variable, self.variable, options)
        
        # <input> for central value
        input_central = InputNode(self.variable + '.mean').render(context)
        
        # <input>-s for range
        input_from = InputNode(self.variable + '.from').render(context)
        input_to   = InputNode(self.variable + '.to').render(context)
        
        # <tr> - subsection
        subsection = u'''<tr class="subsection">
                <th class="label">%s</th>
                <td>%s</td>
            </tr>'''.encode('utf-8') % (self.label, select)
        
        # Единица измерения
        unit = '<div class="unit">заявок</div>'
        
        # <tr> - central
        hide = ' style="display: none"'
        tr_central = u'''
            <tr id="%s.central"%s>
                <th class="label nested">Скорость, в час:</th>
                <td>%s%s</td>
            </tr>'''.encode('utf-8') % (self.variable, hide if current == 'equal' else '', input_central, unit)
        
        # <tr> - range
        style = hide if current != 'equal' else ''
        tr_range = u'''
            <tr id="%s.range-first"%s>
                <th class="label nested">Скорость, в час: от</th>
                <td>%s%s</td>
            </tr>
            <tr id="%s.range-last"%s>
                <th class="label nested">до</th>
                <td>%s%s</td>
            </tr>'''.encode('utf-8') % (self.variable, style, input_from, unit, self.variable, style, input_to, unit)
        
        return subsection + tr_central + tr_range

@register.tag
def input(parser, token):
    'Тег {% input variable "name" %}'
    
    try:
        tokens = token.split_contents()[1:]
        variable, name = tokens[0], tokens[1:]
    except:
        raise django_template.TemplateSyntaxError, "%r tag requires exactly two arguments, %s found" % (token.contents.split()[0], token.split_contents())
    
    return InputNode(variable, name)

@register.filter
def values_sort(value):
    'Всякая фигня - написать и забыть. Очень некрасивая штука, до невозможности некрасивая. Пакость.'
    def first(x):
        return x[0]
    
    def second(x):
        return x[1]
    
    return map(second, sorted(value.items(), key=first))

@register.tag
def distribution(parser, token):
    'Поле ввода'
    bits = token.split_contents()
    (label, variable) = bits[1:]
    return DistributionNode(str(label[1:-1]), str(variable[1:-1]))


