from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.


WORDS = {
    'редиска': 'редиска',
    'директор': 'директор',
    'глубине': 'глубине',
    'поразили': 'поразили',
    'убитое': 'убитое',
    'напомним': 'напомним',
    'чепухи': 'чепухи',
    'простуды': 'простуды'
}

WOR = ['редиска', 'чепухи']


@register.filter()
def censor(value):
   a = value
 #  for word in list(WORDS.keys()):
   for word in WOR:
      if word in a:
         a = a.replace(word, f'{word[:1]}{len(word[1:])*"*"}')
         #a = a.replace(word, f'{word[:1]}*****{word[-1:-2:-1]}')
      if word.capitalize() in a:
         a = a.replace(word.capitalize(), f'{word[:1].capitalize()}*****{word[-1:-2:-1].capitalize()}')

   return a
