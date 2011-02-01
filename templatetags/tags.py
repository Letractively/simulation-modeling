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
        input_tag = '<input class="%s" name="%s" id="%s" value="%s" />' % (input_class, self.variable, self.variable, value)
        
        # <div class="error"> and return result HTML
        if error:
            error_tag = '<div class="balloon" id="%s">%s</div>' % (self.variable + '.error', error.encode('utf-8'))
            return error_tag + input_tag.encode('utf-8')
        else:
            return input_tag.encode('utf-8')

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

def input(parser, token):
    'Поле ввода'
    bits = token.split_contents()
    variable = bits[1]
    if variable[0] == variable[-1] and variable[0] in ('"', "'"):
        return InputNode(str(variable[1:-1]))
    else:
        raise Exception('In input tag, you should enclose varname in quotes!')

def distribution(parser, token):
    'Поле ввода'
    bits = token.split_contents()
    (label, variable) = bits[1:]
    return DistributionNode(str(label[1:-1]), str(variable[1:-1]))

register = template.create_template_register()
register.tag(input)
register.tag(distribution)

