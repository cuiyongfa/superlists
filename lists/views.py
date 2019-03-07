from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.http import HttpResponse

# Create your views here.
# home_page = None


def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the_only_one_list_url')

    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':

        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect('/lists/%d/' %(list_.id,))
        except ValidationError:
            error = '输入不能为空'
    return render(request, 'view_list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = '输入不能为空'
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/%d/' % (list_.id,))
