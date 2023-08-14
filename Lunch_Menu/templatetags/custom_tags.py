from django import template

register = template.Library()

@register.filter
def is_selected(food_item, user_orders):
    return user_orders.filter(food_items=food_item).exists()