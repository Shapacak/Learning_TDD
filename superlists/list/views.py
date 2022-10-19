from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import Item


def home_page(request):
    return render(request, 'home.html')


def list_new(request):
    Item.objects.create(text=request.POST.get('item_text'))
    return redirect('imba_list/')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items':items})
