from django.shortcuts import render, HttpResponse

from .forms import TextInput

# Create your views here.


def index(request):
    template_name: str = "zhehe_convert/convert_main.html"
    text_area = TextInput

    return render(request=request, template_name=template_name, status=200, context={'form': text_area})
