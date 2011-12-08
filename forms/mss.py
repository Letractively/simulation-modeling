# -*- coding: utf-8 -*-

from wtforms import Form, IntegerField, FloatField
from wtforms.validators import Required, Optional
from validators import *
import translations

good = [unsigned, reasonable]
excellent = [positive, reasonable]

IntegerField._translations = FloatField._translations = translations.Translations()

class ModelForm(Form):
    channels_count = IntegerField(u'Число каналов', excellent)
    total_time = FloatField(u'Продолжительность', excellent)
    times = IntegerField(u'Число итераций', excellent)
    
    in_stream = FloatField(u'Поступает, в час', excellent)
    out_stream = FloatField(u'Обслуживается, в час', excellent)
    cost = FloatField(u'Средний доход', excellent)
    
    queue_size = IntegerField(u'Макс. размер', [unsigned, reasonable, Optional()])
    queue_time = FloatField(u'Макс. срок ожидания', [unsigned, reasonable, Optional()])
    
    fault_stream = FloatField(u'Наработка на отказ', [positive, reasonable, Optional()])
    repair_stream = FloatField(u'Время ремонта', [unsigned, reasonable, required_if('fault_stream')])
    repair_cost = FloatField(u'Стоимость ремонта', [unsigned, reasonable, required_if('fault_stream')])
    destructive = FloatField(u'Вероятность аварии', [probability, required_if('fault_stream')])



