from typing import Optional, Dict, List

from django.db.models import QuerySet
from django.shortcuts import render

from .forms import Newsletter, Contact, TextInput
from .models import Contact_Info, Subscriber, Document
from allauth.account.forms import LoginForm
from allauth.account.decorators import verified_email_required

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


@verified_email_required
def home(request):
    template_name: str = 'zhehe_user_app/zhehe_home/overview.html'
    context_dict: Dict[str, Optional[QuerySet]] = {'documents': None}

    if request.user.is_authenticated:
        """
        If the user requesting is authenticated retrieve his documents
        """
        try:
            context_dict['documents'] = Document.objects.filter(document_owner=request.user.id)
        except Document.DoesNotExist:
            pass  # Ignore
    return render(request=request, template_name=template_name, context=context_dict)


def contact(request):
    template_name: str = 'zhehe_user_app/zhehe_index/forms/contact_form.html'

    contact_form = Contact()
    if request.method == 'POST':
        contact_form = Contact(request.POST)
        if contact_form.is_valid():
            print(contact_form.cleaned_data)
        else:
            logger.error(contact_form.errors)
    return render(request=request, template_name=template_name, context={'contact': contact_form})


def new_doc(request):
    template_name: str = "zhehe_user_app/zhehe_home/new_doc.html"
    text_area = TextInput()
    messages: List[str] = []
    if request.method == 'POST':
        text_area = TextInput(request.POST)
        if text_area.is_valid():
            print(text_area.cleaned_data)
            messages.append('Dokument erfolgreich konvertiert')
        else:
            print(text_area.errors)

    return render(request=request, template_name=template_name, status=200, context={'text_form': text_area,
                                                                                     'messages': messages})


def download(request):
    pass
