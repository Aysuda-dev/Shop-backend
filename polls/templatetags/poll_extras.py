from django import template
from jalali_date import date2jalali, datetime2jalali

register = template.Library()

@register.filter
def show_date(view):
    return date2jalali(view)

@register.filter
def show_time(view):
    return datetime2jalali(view).strftime('%H:%M')

@register.filter
def three_digit_currency(value:int):
    return '{:,}'.format(value) + 'ریال'

@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digit_currency(quantity * price)