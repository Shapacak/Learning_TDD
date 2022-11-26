from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from list.models import Item, List
from list.forms import ItemForm, ExistingListItemForm


def home_page(request):
    '''домашняя страница'''
    return render(request, 'home.html', {'form': ItemForm()})


def list_new(request):
    '''новый список'''
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})


def view_list(request, id):
    '''просмотр конкретного списка'''
    list_ = List.objects.get(id=id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

