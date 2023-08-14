from django.contrib.auth import views as auth_views
from django.urls import path

from Lunch_Menu import views


urlpatterns = [

    path('', views.login, name='login'),
    path('selection/', views.selection, name='selection'),
    path('login/', views.login, name='login'),
#     path('add_user/', views.add_user, name='add_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('orders/', views.orders, name='orders'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('users/', views.users, name='users'),
    path('book/', views.book, name='book'),  
    path('menu/', views.menu_manage, name='menu'), 
    path('selection/edit', views.edit_selection, name='edit_selection'), 
    path('delete_food_item/', views.delete_food_item, name='delete_food_item'),
    path('reports/',views.reports, name='reports'),
    path('menu_edit/', views.menu_edit, name='menu_edit'),
    path('toggle_food_item/', views.toggle_food_item, name='toggle_food_item'),
    path('check_food_item_exists/', views.check_food_item_exists, name='check_food_item_exists'),

    # reset password routes
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form_.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done_.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm_.html",post_reset_login=True,  # Auto-login after password reset
         post_reset_login_backend='django.contrib.auth.backends.ModelBackend'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete_.html"),
         name="password_reset_complete"),
]
