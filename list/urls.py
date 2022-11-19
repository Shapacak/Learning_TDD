from django.urls import path
from . import views

urlpatterns = [
    path('new', views.list_new, name='new_list'),
    path('<int:id>/', views.view_list, name='view_list'),
]