# -*- coding: utf-8 -*-

'Модуль интерфейса'

from lxml import etree
import os

def serialize_input(values, errors = {}, node = None):
    '''Сериализация входных данных input в XML-дерево с корнем в элементе node
    с учётом ошибок errors'''

    # Если родительский элемент не указан, нужно его создать
    if node is None:
        node = etree.Element('input')

    t = type(values)
    # Текущий узел является группой узлов
    if t == dict:
        for child, value in values.items():
            try:
                error = errors[child]
            except:
                error = {}

            serialize_input(value, error, etree.SubElement(node, child))

    # Текущий узел является значением
    else:
        node.text = unicode(values)
        if errors:
            node.set('error', unicode(errors))

    return node

def serialize_output(results):
    'Подготовка вывода'

    def spider(variable, parent):
        if type(variable) == dict:
            for key, value in variable.items():
                spider(value, etree.SubElement(parent, key))    
        elif type(variable) in (tuple, list):
            for value in variable:
              spider(value, etree.SubElement(parent, 'item'))
        else:
            parent.text = unicode(variable)

        return parent

    return spider(results, etree.Element('output'))

def notfound(model):
    return 'NOT FOUND: ' + model

def view(root, model = None, accepts = {}, input = {}, output = {}, errors = {}, fatal = None, path = ''):
    'Основная процедура интерфейса. Генерирует содержимое страницы.'
    
    # Фатальная ошибка
    if fatal is not None:
      return 'FATAL: ' + str(fatal)
    
    tree = etree.Element('model')
    tree.set('title', model.__doc__)
    tree.set('sitename', u'Имитатор')
    tree.set('path', path)

    #return str(errors)
    input = serialize_input(input, errors = errors)
    #return etree.tostring(input)

    tree.append(input)
    
    if output:
      output = serialize_output(output)
      tree.append(output)
    
    xsl = etree.parse(root + '/templates/' + model.__name__ + '.xsl')
    transform = etree.XSLT(xsl)
    
    #return etree.tostring(tree)
    return etree.tostring(transform(tree))

def presenter(**basic_args):
    'Осуществляет карринг для более удобного вызова interface.view().'
    
    def viewer(**args):
        basic_args.update(args)
        
        return view(**basic_args)
    
    return viewer
