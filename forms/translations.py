# -*- coding: utf-8 -*-

translations = {
    'Not a valid float value': u'Пожалуйста, введите число.',
    'Not a valid integer value': u'Пожалуйста, введите целое число.',
}

class Translations(object):
    def gettext(self, string):
        return translations[string]

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular

        return plural
