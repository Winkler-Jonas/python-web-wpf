from typing import Optional, Dict

from django.db.models import QuerySet
from django.shortcuts import render

from .forms import Newsletter, Contact, TextInput
from .models import Contact_Info, Subscriber, Document

import logging
logger = logging.getLogger(__name__)


def index(request):
    template_name: str = 'zhehe_user_app/zhehe_index/index_main.html'
    newsletter_form = Newsletter
    contact_form = Contact
    if request.method == 'POST':
        logger.error('At least we are in the post method')
        xy = Newsletter(request.POST)
        if xy.is_valid():
            logger.error('Hello from Newsletter form')
        else:
            logger.error(xy.errors)
        if form := Newsletter(request.POST).is_valid():
            logger.error('Hello from Newsletter form')
        elif form := Contact(request.POST).is_valid():
            logger.error('Hello from contact form')

    return render(request=request, template_name=template_name, status=200, context={'newsletter': newsletter_form,
                                                                                     'contact': contact_form})


def overview(request):
    template_name: str = 'zhehe_user_app/zhehe_convert/overview.html'
    context_dict: Dict[str, Optional[QuerySet]] = {'documents': None}

    try:
        context_dict['documents'] = Document.objects.all()
    except Document.DoesNotExist:
        pass    # Ignore

    print(request.GET)

    return render(request=request, template_name=template_name, context=context_dict)


def new_doc(request):
    template_name: str = "zhehe_user_app/zhehe_convert/convert_main.html"
    text_area = TextInput

    return render(request=request, template_name=template_name, status=200, context={'form': text_area})


def download(request):
    pass
