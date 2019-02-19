"""catcollectr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
########
# CatCollectr/CatCollectr/urls.py
from django.urls import include, path
from django.contrib import admin
# from main_app import views # took this line out at step 7 even though directions not explicit, though sample code was

# The first argument is the relative path for the URL. 
# The second argument is the specific path to the view function 
# we want to associate with our route.

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('main_app.urls'))
]
