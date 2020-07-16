from typing import Optional, Dict

from django.db.models import QuerySet
from django.shortcuts import render

from .forms import Newsletter, Contact, TextInput, SignUp
from .models import Contact_Info, Subscriber, Document

import logging
logger = logging.getLogger(__name__)


def index(request):
    template_name: str = 'zhehe_user_app/zhehe_index/skeleton.html'
    newsletter_form = Newsletter
    contact_form = Contact
    signup_form = SignUp()
    if request.method == 'POST':
        logger.error('At least we are in the post method')
        signup_form = signup_form = SignUp(request.POST)
        if signup_form.is_valid():
            logger.error('Hello from Newsletter form')
            logger.error(signup_form.cleaned_data)
        else:
            logger.error(signup_form.errors)
        if form := Newsletter(request.POST).is_valid():
            logger.error('Hello from Newsletter form')
        elif form := Contact(request.POST).is_valid():
            logger.error('Hello from contact form')

    return render(request=request, template_name=template_name, status=200, context={'newsletter': newsletter_form})


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


def signup(request):
    template_name: str = 'zhehe_user_app/zhehe_index/forms/signup.html'

    signup_form = SignUp()
    if request.method is 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
        else:
            logger.error(form.errors)
    return render(request=request, template_name=template_name, context={'contact': signup_form})


def new_doc(request):
    template_name: str = "zhehe_user_app/zhehe_convert/convert_main.html"
    text_area = TextInput

    return render(request=request, template_name=template_name, status=200, context={'form': text_area})


def download(request):
    pass
