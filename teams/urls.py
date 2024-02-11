from django.contrib import admin
from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path("", views.all_teams, name='all_teams'),
    path('<int:team_id>/', views.specific_team, name='specific_team'),
    path('add_new_team/', views.add_new_team, name='add_new_team'),
    path('edit_team/<int:team_id>/', views.edit_team, name='edit_team'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
]
