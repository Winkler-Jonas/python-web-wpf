from typing import Dict, Optional

from django.shortcuts import render, HttpResponse
from django.db.models.query import QuerySet
from .forms import TextInput
from .models import Document

# Create your views here.


def overview(request):
    template_name: str = 'zhehe_convert/overview.html'
    context_dict: Dict[str, Optional[QuerySet]] = {'documents': None}

    try:
        context_dict['documents'] = Document.objects.all()
    except Document.DoesNotExist:
        pass    # Ignore

    print(request.GET)

    return render(request=request, template_name=template_name, context=context_dict)


def new_doc(request):
    template_name: str = "zhehe_convert/convert_main.html"
    text_area = TextInput

    return render(request=request, template_name=template_name, status=200, context={'form': text_area})


def download(request):
    pass
