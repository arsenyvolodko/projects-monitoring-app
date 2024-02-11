from django.contrib import admin
from django.urls import path

import grants
from . import views

app_name = 'grant'

urlpatterns = [
    path("", views.all_grants, name='all_grants'),
    path('addnewgrant/', views.add_new_grant, name='add_new_grant'),
    path('grant/<int:grant_id>', views.specific_grant, name='specific_grant'),
    path('grant/<int:grant_id>/edit_grant', views.edit_grant, name='edit_grant'),
    path('grant/<int:grant_id>/delete_grant', views.delete_grant, name='delete_grant'),
    path('grant/<int:project_id>/edit_sponsored_money/<int:grant_id>', views.edit_sponsored_money_in_grants, name='edit_sponsored_money_in_grants'),
    path('grant/<int:project_id>/delete_sponsored_money/<int:grant_id>', views.delete_sponsored_money_in_grants, name='delete_sponsored_money_in_grants'),
    path('grant/<int:grant_id>/add_sponsored_money', views.add_sponsored_money, name='add_sponsored_money'),


]
