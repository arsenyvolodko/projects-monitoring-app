from django.contrib import admin
from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path("", views.all_members, name='all_members'),
    path('<int:member_id>/', views.specific_member, name='specific_member'),
    path('add_new_member/', views.add_new_member, name='add_new_member'),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member')
]
