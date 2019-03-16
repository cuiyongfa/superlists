from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm
from django.http import HttpResponse

# Create your views here.
# home_page = None


def home_page(request):

    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
    if form.is_valid():
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    return render(request, 'view_list.html', {'list': list_, "form": form})


def new_list(request):
    # list_ = List.objects.create()
    # item = Item(text=request.POST['text'], list=list_)
    # try:
    #     item.full_clean()
    #     item.save()
    # except ValidationError:
    #     list_.delete()
    #     error = '输入不能为空'
    #     return render(request, 'home.html', {'error': error})
    # return redirect(list_)

    form = ItemForm(data=request.POST)  # ➊
    if form.is_valid():  # ➋
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})  # ➌
