from django import template

try:
    # Python 3.x
    from urllib.parse import quote_plus
except:
    # Python 2.x
    from urllib import quote_plus


register = template.Library()


@register.filter
def urlify(value):
    return(quote_plus(value))
