"""Chinese_Emotion_Analysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Emotion_Manager.views import index, calculate_accuracy, dict_result, redirect_to_index

urlpatterns = [
    path('', redirect_to_index),
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('calculate/', calculate_accuracy, name='calculate'),
    path('dict/', dict_result)
]
