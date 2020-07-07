from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    template_name: str = "zhehe_index/index_main.html"
    #return HttpResponse('<h1>Done</h1>')
    return render(request=request, template_name=template_name, status=200)
