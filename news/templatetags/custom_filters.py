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

@register.filter()
def ru_plural(value, variants):
    variants = variants.split(',')
    value = abs(int(value))

    if value % 10 == 1 and value % 100 != 11:
        variant = 0

    elif value % 10 >= 2 and value % 10 <= 4 and \
            (value % 100 < 10 or value % 100 >= 20):
        variant = 1

    else:
        variant = 2

    return variants[variant]