from django.db import models
from django.contrib.auth.models import AbstractUser

# Model for the User
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


# Model for Food Items
class FoodItem(models.Model):
    FOODTYPE_CHOICES = (
        ('food', 'Food'),
        ('sauces', 'Sauces'),
        ('drinks', 'Drinks'),
    )
    name = models.CharField(max_length=100)
    foodType = models.CharField(max_length=100, choices=FOODTYPE_CHOICES, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def is_selected(self, user_orders):
        return user_orders.filter(food_items=self).exists()


# Model for Lunch Orders
class LunchOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_items = models.ManyToManyField(FoodItem)
    order_date = models.DateField()
    is_ordered = models.BooleanField(default=False)
    time_of_order = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Order - {self.order_date}"

class MainFood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sauce(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Extra(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# from Lunch_Menu.models import FoodItem
# def create_food_items():
#     food_items = [
#         ('Matooke', 'food'),
#         ('Irish', 'food'),
#         ('Cassava', 'food'),
#         ('Mango', 'drinks'),
#         ('Passion', 'drinks'),
#         ('GNuts', 'sauces'),
#         ('Rice', 'food'),
#         ('Posho', 'food'),
#         ('Fish', 'sauces'),
#         ('Beef', 'sauces'),
#     ]

#     for name, food_type in food_items:
#         FoodItem.objects.create(name=name, foodType=food_type)

# # Call the function to create the food items
# create_food_items()

# from Lunch_Menu.models import FoodItem
# FoodItem.objects.all().delete()


# from Lunch_Menu.models import FoodItem

# # Retrieve the queryset of instances to delete
# foods_to_delete = FoodItem.objects.filter(name__in=["Pizza", "Burger", "Salad"])

# # Delete the instances
# foods_to_delete.delete()
