from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    template_name: str = ""
    return HttpResponse('<h1>Some other Text</h1>')
    # return render(request=request, template_name=template_name, status=200)
