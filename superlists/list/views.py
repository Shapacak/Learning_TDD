from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def list_new(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/list/{list_.id}/')


def view_list(request, id):
    list_ = List.objects.get(id=id)
    return render(request, 'list.html', {'list':list_})


def add_item(request, id):
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/list/{id}/')
