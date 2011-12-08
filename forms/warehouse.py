# -*- coding: utf-8 -*-

from wtforms import Form, IntegerField, FloatField
from wtforms.validators import Required, Optional
from validators import *
import translations

good = [unsigned, reasonable]
excellent = [positive, reasonable]

IntegerField._translations = FloatField._translations = translations.Translations()

class ModelForm(Form):
    lot_size = IntegerField(u'Размер партии', excellent)
    limit = IntegerField(u'Минимальный запас', good)
    amount = IntegerField(u'Начальный запас', good)
    
    total_time = FloatField(u'Продолжительность', excellent)
    times = IntegerField(u'Число итераций', excellent)
    
    demand_mu = FloatField(u'В среднем', excellent)
    demand_sigma = FloatField(u'Отклонение', good)
    
    supply_mu = FloatField(u'В среднем', excellent)
    supply_sigma = FloatField(u'Отклонение', good)
    
    demand_price = FloatField(u'Цена изделия', good)
    supply_price = FloatField(u'Цена поставки', good)
    storage_price = FloatField(u'Цена хранения', good)
    fine = FloatField(u'Штраф за недостачу', good)




