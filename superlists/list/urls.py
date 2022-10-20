from django.urls import path
from . import views

urlpatterns = [
    path('new', views.list_new),
    path('<int:id>/', views.view_list),
    path('<int:id>/add_item', views.add_item),
]