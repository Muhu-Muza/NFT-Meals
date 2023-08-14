from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.http import HttpResponse
from Lunch_Menu.models import LunchOrder
from .models import FoodItem
from .models import User
from django.utils import timezone
import datetime



# Create your views here.
# @login_required
# def book(request):
#     if request.method == 'POST':
#         selected_items = request.POST.get('food_item_selected', '')  # Get the comma-separated string
#         item_ids = [int(item_id) for item_id in selected_items.split(',') if item_id.isdigit()]  # Convert to a list of integers
#         user = request.user
#         order_date = date.today()

#         lunch_order = LunchOrder.objects.create(user=user, order_date=order_date)
#         for item_id in item_ids:
#             try:
#                 food_item = FoodItem.objects.get(id=item_id)
#                 lunch_order.food_items.add(food_item)
#             except FoodItem.DoesNotExist:
#                 pass  # Handle the case where the food item with the given ID does not exist

#         # Redirect to the selection page after saving the order
#         return redirect('Lunch_Menu:selection')

#     else:
#         food_items = FoodItem.objects.all()
#         # Check if the user has a lunch order
#         user_has_order = LunchOrder.objects.filter(user=request.user).exists()
#         context = {'segment': 'book', 'food_items': food_items, 'user_has_order': user_has_order}
#         return render(request, "book.html", context)

def book(request):
    now = timezone.now().strftime("%H:%M:%S")
    tomorrow = (timezone.now() + datetime.timedelta(days=1))
    
    # Get the day of the week for tomorrow
    day_of_week = tomorrow.strftime('%A')
    
    if request.method == 'POST':
        selected_items = request.POST.get('food_item_selected', '')
        item_ids = [int(item_id) for item_id in selected_items.split(',') if item_id.isdigit()]
        user = request.user
        order_date = date.today()
        time_of_order = timezone.now().time()

        lunch_order = LunchOrder.objects.create(user=user, order_date=order_date, time_of_order=time_of_order)
        for item_id in item_ids:
            try:
                food_item = FoodItem.objects.get(id=item_id)
                lunch_order.food_items.add(food_item)
            except FoodItem.DoesNotExist:
                pass  # Handle the case where the food item with the given ID does not exist

        # Redirect to the selection page after saving the order
        return redirect('selection')

    else:
        food_items = FoodItem.objects.filter(is_active=True)
        user_has_order = LunchOrder.objects.filter(user=request.user).exists()
        today = date.today()
        user_has_ordered_today = LunchOrder.objects.filter(user=request.user, order_date=today).exists()

        # Get the current date and time
        

        context = {
            'segment': 'book',
            'food_items': food_items,
            'user_has_order': user_has_order,
            'user_has_ordered_today': user_has_ordered_today,
            'now': now,
            'formatted_date': tomorrow.strftime('%d/%m/%Y'), 'day_of_week': day_of_week}
        
        return render(request, "book.html", context)




@login_required
# def selection(request):
#     user = request.user
#     today = date.today()
    
#     # Filter user orders based on the current date
#     user_orders = LunchOrder.objects.filter(user=user, order_date=today)
    
#     context = {'segment': 'selection', 'user_orders': user_orders}
#     return render(request, "selection.html", context)

def selection(request):
    user = request.user
    today = date.today()
    
    # Filter user orders based on the current date
    user_orders = LunchOrder.objects.filter(user=user, order_date=today)
    
    now = timezone.now().strftime("%H:%M:%S")  # Convert datetime object to string in "HH:MM:SS" format
    context = {'segment': 'selection', 'user_orders': user_orders, 'now': now}
    return render(request, "selection.html", context)


# def edit_selection(request):
#     # Get the current user's lunch orders
#     user_orders = LunchOrder.objects.filter(user=request.user)

#     # Get all food items
#     food_items = FoodItem.objects.all()

#     context = {'segment': 'edit_selection', 'food_items': food_items, 'user_orders': user_orders}
#     return render(request, "edit_selection.html", context)
@login_required
def edit_selection(request):
    # Get the current user's lunch orders
    user_orders = LunchOrder.objects.filter(user=request.user)

    # Get all food items
    food_items = FoodItem.objects.filter(is_active=True)

    context = {'segment': 'edit_selection', 'food_items': food_items, 'user_orders': user_orders}

    if request.method == 'POST':
        # Process the form submission and update the lunch order
        selected_food_items_str = request.POST.get('food_item_selected', '')
        selected_food_items = [int(item_id) for item_id in selected_food_items_str.split(',') if item_id.isdigit()]
        time_of_order = timezone.now().time()

        user_order = LunchOrder.objects.filter(user=request.user).first()

        if user_order:
            user_order.food_items.clear()  # Remove all previous food items from the order
            for item_id in selected_food_items:
                try:
                    food_item = FoodItem.objects.get(id=item_id)
                    user_order.food_items.add(food_item)  # Add selected food items to the order
                except FoodItem.DoesNotExist:
                    pass

            user_order.time_of_order = time_of_order  # Update the time_of_order field
            user_order.save()  # Save the changes to the user's order

            return redirect('selection')

    # Render the template when the method is not POST
    return render(request, "edit_selection.html", context)



@login_required
@user_passes_test(lambda user: user.is_superuser)
def users(request):
    if request.method == 'POST':
        # Check if the request is a POST request (form submission)
        user_id_to_delete = request.POST.get('userId', None)
        if user_id_to_delete:
            try:
                user = User.objects.get(pk=user_id_to_delete)
                # Delete the user from the database
                user.delete()
                # Redirect back to the same page after successful deletion
                return redirect('users')
            except User.DoesNotExist:
                return HttpResponse("User not found.", status=404)
    
    # If the request is not a POST request or user deletion is unsuccessful,
    # display the list of users as before.
    users = User.objects.all()
    context = {'segment': 'users', 'users': users}
    return render(request, "users.html", context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def user_orders(request):
    today = date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    # Get the day of the week for tomorrow
    day_of_week = tomorrow.strftime('%A')
    user_orders = LunchOrder.objects.filter(order_date=today)
    
    context = {'segment': 'user_orders', 'user_orders': user_orders, 'formatted_date': tomorrow.strftime('%d/%m/%Y'), 'day_of_week': day_of_week}
    return render(request, "user_orders.html", context)

# @login_required
# @user_passes_test(lambda user: user.is_superuser)
# def add_user(request):
#     context = {'segment': 'add user'}
#     return render(request, "register.html", context)



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            return redirect('book')  # Redirect after successful login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    context = {'segment': 'login'}
    return render(request, "login.html", context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'Username or Email already exists.')
            return redirect('register')

        # Create the new user object but don't save it yet
        user = User(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password)  # Hash the password before saving
        user.save()

        messages.success(request, 'Account created successfully! You can now log in.')
        auth_login(request, user)
        return redirect('book')  # Redirect to the login page

    context = {'segment': 'register'}
    return render(request, "register.html", context)



def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
@user_passes_test(lambda user: user.is_superuser)
def orders(request):
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    
    # Get the day of the week for tomorrow
    day_of_week = tomorrow.strftime('%A')

    food_items = FoodItem.objects.filter(foodType__in=['food', 'sauces', 'drinks'], is_active=True)
    
    todays_orders = LunchOrder.objects.filter(order_date=today)
    
    food_items = food_items.annotate(num_users=Count('lunchorder__user', filter=Q(lunchorder__in=todays_orders), distinct=True))
    
    context = {'segment': 'orders', 'food_items': food_items, 'formatted_date': tomorrow.strftime('%d/%m/%Y'), 'day_of_week': day_of_week}
    return render(request, "orders.html", context)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def menu_manage(request):
    # Get all food items
    food_items = FoodItem.objects.all()

    if request.method == 'POST':
        new_item_name = request.POST.get('newItem')
        new_item_type = request.POST.get('newItemType')
        if new_item_name and new_item_type in ['food', 'sauces', 'drinks']:
            FoodItem.objects.create(name=new_item_name, foodType=new_item_type)

    context = {'segment': 'menu_manage', 'food_items': food_items}
    return render(request, "menu_manage.html", context)

def delete_food_item(request):
    if request.method == 'POST':
        food_item_id = request.POST.get('foodItemId')
        if food_item_id:
            try:
                food_item = FoodItem.objects.get(pk=food_item_id)
                food_item.delete()
            except FoodItem.DoesNotExist:
                pass  # Handle error if food item does not exist

    return redirect('menu')


@xframe_options_exempt
@csrf_exempt
def api(request):
    if request.method == 'POST':
        # Get the selected items from the POST data
        selected_items = request.POST.getlist('selected_items[]')

        # Handle the selected items as needed (e.g., save to the database, perform calculations, etc.)

        # Return a response (in this example, we're returning a success message)
        return JsonResponse({'message': 'Data received successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def check_food_item_exists(request):
    if request.method == 'GET':
        item_name = request.GET.get('item_name', '')
        if FoodItem.objects.filter(name__iexact=item_name).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})



def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)

def handle_403(request, exception):
    return render(request, '403.html', status=403)

def handle_400(request, exception):
    return render(request, '400.html', status=400)

@login_required
def reports(request):    
    context = {'segment': 'reports'}
    return render(request, "reports.html", context)

@login_required
@user_passes_test(lambda user: user.is_superuser)
def menu_edit(request):
    food_items = FoodItem.objects.all()
    context = {
        'segment': 'menu_edit',
        'food_items': food_items,
    }
    
    return render(request, 'menu_edit.html', context)

@require_POST
@csrf_exempt  # Use this decorator for simplicity, consider using a proper CSRF setup
def toggle_food_item(request):
    food_item_id = request.POST.get('food_item_id')
    try:
        food_item = FoodItem.objects.get(pk=food_item_id)
        food_item.is_active = not food_item.is_active
        food_item.save()
        return JsonResponse({'status': 'success'})
    except FoodItem.DoesNotExist:
        return JsonResponse({'status': 'error'})