from django.urls import path
from . import views

urlpatterns = [
    path('new', views.list_new),
    path('<int:id>/', views.view_list),
]