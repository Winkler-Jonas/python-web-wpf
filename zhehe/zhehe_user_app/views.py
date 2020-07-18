from typing import Optional, Dict

from django.db.models import QuerySet
from django.shortcuts import render

from .forms import Newsletter, Contact, TextInput
from .models import Contact_Info, Subscriber, Document
from allauth.account.forms import LoginForm

import logging
logger = logging.getLogger(__name__)


def index(request):
    template_name: str = 'zhehe_user_app/zhehe_index/skeleton.html'
    newsletter_form = Newsletter()
    signin_form = LoginForm()
    if request.method == 'POST':
        newsletter_form = Newsletter(request.POST)
        if newsletter_form.is_valid():
            print(newsletter_form.cleaned_data)
        else:
            print(newsletter_form.errors)

    return render(request=request, template_name=template_name, status=200, context={'newsletter': newsletter_form,
                                                                                     'signin': signin_form})


def home(request):
    template_name: str = 'zhehe_user_app/zhehe_convert/overview.html'
    context_dict: Dict[str, Optional[QuerySet]] = {'documents': None}

    try:
        context_dict['documents'] = Document.objects.all()
    except Document.DoesNotExist:
        pass    # Ignore

    print(request.GET)

    return render(request=request, template_name=template_name, context=context_dict)


def contact(request):
    template_name: str = 'zhehe_user_app/zhehe_index/forms/contact_form.html'

    contact_form = Contact()
    if request.method == 'POST':
        logger.error(request.POST)
        logger.error('Hello from contact view')
        contact_form = Contact(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
        else:
            logger.error(contact_form.errors)
    return render(request=request, template_name=template_name, context={'contact': contact_form})


def new_doc(request):
    template_name: str = "zhehe_user_app/zhehe_convert/convert_main.html"
    text_area = TextInput

    return render(request=request, template_name=template_name, status=200, context={'form': text_area})


def download(request):
    pass
