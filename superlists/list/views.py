from django.shortcuts import render, redirect
from django.http import HttpResponse
from list.models import Item



def home_page(request):
    if request.method == 'POST':
        item = Item()
        item.text = request.POST.get('item_text')
        item.save()
        return redirect('/')
    else:
        items = Item.objects.all()
        return render(request, 'home.html', {'items':items})
