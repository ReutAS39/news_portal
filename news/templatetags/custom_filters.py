from django import template

class CensorException(Exception):
    pass

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

WORDS = ['редиска', 'чепухи', 'reebok', 'текст']

@register.filter()
def censor(value):
    try:
        if not isinstance(value, str):
            raise CensorException('Error')

        v = value
        for word in WORDS:
            if word in v:
                v = v.replace(word, f'{word[:1]}{len(word[1:])*"*"}')
            if word.capitalize() in v:
                v = v.replace(word.capitalize(), f'{word[:1].capitalize()}{len(word[1:])*"*"}')

        return v

    except CensorException as e:
        print(e)