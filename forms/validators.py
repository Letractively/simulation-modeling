# -*- coding: utf-8 -*-

from wtforms.validators import ValidationError, Required, Optional

required = Required(message=u'Пожалуйста, введите что-нибудь.')

def positive(form, field):
    if field.data <= 0:
        raise ValidationError(u'Пожалуйста, введите положительное число.')

def unsigned(form, field):
    if field.data < 0:
        raise ValidationError(u'Пожалуйста, введите неотрицательное число.')

def reasonable(form, field):
    if field.data > 1000:
        raise ValidationError(u'Помилуйте, зачем же так много?')

def probability(form, field):
    if not (0 <= field.data <= 1):
        raise ValidationError(u'Пожалуйста, укажите число между 0 и 1.')

def required_if(master_field_name, message=None):
    'Валидатор требует заполнения поля field, если непусто поле master_field.'
    
    if not message:
        message = u'Пожалуйста, введите что-нибудь.'
    
    def required_if(form, field):
        master_field = getattr(form, master_field_name)
        if master_field.data is None:
            Optional()(form, field)
    
    return required_if
