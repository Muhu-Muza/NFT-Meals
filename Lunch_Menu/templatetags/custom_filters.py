from django import template
from datetime import datetime, time

register = template.Library()

@register.filter
def is_selected(food_item, user_orders):
    return food_item in user_orders


# @register.filter
# @register.filter
# def time_between(value, time_range):
#     try:
#         value = datetime.strptime(value, '%H:%M:%S').time()
#         start_time, end_time = [datetime.strptime(t, '%H:%M:%S').time() for t in time_range.split()]
#         return start_time <= value <= end_time
#     except ValueError:
#         return False

@register.filter
def time_between(value, time_range):
    try:
        start_time, end_time = time_range.split(" ")
        value = datetime.strptime(value, '%H:%M:%S').time()
        start_time = datetime.strptime(start_time, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time, '%H:%M:%S').time()
        return start_time <= value <= end_time
    except ValueError:
        return False