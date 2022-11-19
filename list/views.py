from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from list.models import Item, List


def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html')


def list_new(request):
    '''новый список'''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST.get('item_text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = 'Сначала введите текст'
        return render(request, 'home.html', {'error': error})
    return redirect(f'/list/{list_.id}/')


def view_list(request, id):
    '''просмотр конкретного списка'''
    list_ = List.objects.get(id=id)
    return render(request, 'list.html', {'list':list_})


def add_item(request, id):
    '''добавить элемент списка'''
    list_ = List.objects.get(id=id)
    Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/list/{id}/')
