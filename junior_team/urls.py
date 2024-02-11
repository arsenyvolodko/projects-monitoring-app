"""
URL configuration for junior_team project.

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
from django.contrib import admin
from django.urls import path, include
import main_page
from main_page import views

urlpatterns = [
    path('', main_page.views.home, name='home'),
    path("admin/", admin.site.urls),

    path('teams/', include('teams.urls')),

    path('projects/', include('projects.urls')),

    path('grants/', include('grants.urls')),

    path('members/', include('members.urls')),

    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
]
