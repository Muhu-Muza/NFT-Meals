"""
URL configuration for Lunch_Menu_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project_name/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Lunch_Menu.urls')), 
    # path('book/', include('Lunch_Menu.urls')), # Add your app's URL patterns here
    # You can add other project-level URL patterns here if needed
]

# Custom URL patterns for handling 404 and 500 errors
handler404 = 'Lunch_Menu.views.handle_404'  #page_not_found
handler500 = 'Lunch_Menu.views.handle_500'   #server_error
handler400 = 'Lunch_Menu.views.handle_400'   #bad_request
handler403 = 'Lunch_Menu.views.handle_403'   #permission_denied
