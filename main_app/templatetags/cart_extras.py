from django import template

register = template.Library()

@register.filter
def sum_total(orders):
    return sum([item.total_price() for item in orders])
