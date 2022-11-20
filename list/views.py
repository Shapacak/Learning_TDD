from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from list.models import Item, List
from list.forms import ItemForm


def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html', {'form': ItemForm()})


def list_new(request):
    '''новый список'''
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST.get('id_text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = 'Сначала введите текст'
        return render(request, 'home.html', {'error': error})
    return redirect(list_)


def view_list(request, id):
    '''просмотр конкретного списка'''
    list_ = List.objects.get(id=id)
    error = ''
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['id_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = 'Сначала введите текст'
    return render(request, 'list.html', {'list': list_, 'error': error})

