from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    _list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=_list)
    return redirect('/lists/the-only-list-in-the-world/')
