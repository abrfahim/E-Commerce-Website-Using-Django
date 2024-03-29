from django import template
import math
register = template.Library()

@register.simple_tag
def call_sellprice(price, discount):
    if discount is None or discount is 0:
        return price
    sellprice = price
    sellprice = price - (price * discount/100)
    return math.floor(int(sellprice))

@register.simple_tag
def progress_bar(total_quantity, availablity):
    progress_bar = availablity
    progress_bar = availablity * (100/total_quantity)
    return math.floor(progress_bar)
    