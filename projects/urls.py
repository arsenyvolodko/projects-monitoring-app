from django.contrib import admin
from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path("", views.all_projects, name='all_projects'),
    path('addnewproject/', views.add_new_project, name='add_new_project'),
    path('<int:project_id>/', views.specific_project, name='specific_project'),
    path('<int:project_id>/delete', views.delete_project, name='delete_project'),
    path('<int:project_id>/edit', views.edit_project, name='edit_project'),
    path('<int:project_id>/add_sponsored_money', views.add_sponsored_money, name='add_sponsored_money'),
    path('<int:project_id>/edit_sponsored_money/<int:grant_id>', views.edit_sponsored_money, name='edit_sponsored_money'),

    # path('<int:blog_id>/', views.detail, name='detail')
]
