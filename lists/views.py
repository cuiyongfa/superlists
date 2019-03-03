from django.shortcuts import render, redirect
from lists.models import Item, List
from django.http import HttpResponse

# Create your views here.
# home_page = None


def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the_only_one_list_url')

    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'view_list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the_only_one_list_url/')
