from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# home_page = None


def home_page(request):
    # return HttpResponse('<html><title>待办事项</title></html>')
    # if request.method =='POST':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request, 'home.html', {'new_item_text': request.POST['item_text']})
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text')})
