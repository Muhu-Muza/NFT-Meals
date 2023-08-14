from django.contrib import admin
from .models import User, FoodItem, LunchOrder


admin.site.register(User)
admin.site.register(FoodItem)
admin.site.register(LunchOrder)
