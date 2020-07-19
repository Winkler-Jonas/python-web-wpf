from typing import Optional, Dict, List

from django.db.models import QuerySet
from django.shortcuts import render

from .forms import Newsletter, Contact, TextInput
from .models import Contact_Info, Subscriber, Document
from .tasks import store_as_pdf
from allauth.account.forms import LoginForm
from allauth.account.decorators import verified_email_required

import logging

logger = logging.getLogger(__name__)


def index(request):
    """
    This view provides the landing page for zhehe application

    Containing two forms:
        - Signin
        - Newsletter

    And several other information regarding the application.
    Also access to user registration etc.

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
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
    """
    ``!important!`` This view is only available for users who validated their email address

    Provides access to users profile / home where documents are stored
    Renders home template

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    template_name: str = 'zhehe_user_app/zhehe_home/overview.html'
    context_dict: Dict[str, Optional[QuerySet]] = {'documents': None}

    if request.user.is_authenticated:
        # If the user requesting is authenticated retrieve his documents
        try:
            context_dict['documents'] = Document.objects.filter(document_owner=request.user.id)
        except Document.DoesNotExist:
            pass  # Ignore
    return render(request=request, template_name=template_name, context=context_dict)


def contact(request):
    """
    This view renders the contact_form template and is used to store user-contact form
    information in database If user wants to receive regular updates Subscriber model
    needs to be updated as well

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    template_name: str = 'zhehe_user_app/zhehe_index/forms/contact_form.html'
    message_contact_success: str = 'Wir haben Ihre Nachricht erhalten und werden Sie baldmöglichst kontaktieren'
    message_subscriber: str = 'Vielen Dank! Wir werden Sie regelmäßig mit Updates über Zhehe versorgen'

    contact_form = Contact()
    messages: List[str] = []
    if request.method == 'POST':
        contact_form = Contact(request.POST)
        if contact_form.is_valid():
            Contact_Info(concern=contact_form.cleaned_data['concern'],
                         name=contact_form.cleaned_data['name'],
                         surname=contact_form.cleaned_data['surname'],
                         email=contact_form.cleaned_data['email'],
                         note=contact_form.cleaned_data['note']).save(force_insert=True)
            messages.append(message_contact_success)
            if contact_form.cleaned_data['newsletter']:
                Subscriber(name=f'{contact_form.cleaned_data["name"]} {contact_form.cleaned_data["surname"]}',
                           email=contact_form.cleaned_data["email"]).save(force_insert=True)
                messages.append(message_subscriber)
    return render(request=request, template_name=template_name, context={'contact': contact_form,
                                                                         'messages': messages})


@verified_email_required
def new_doc(request):
    """
    ``!important!`` This view is only available for users who validated their email address

    This view lets authenticated users create new pdf documents from text formats like (markdown, rst and others..)
    Provides access to TextInput form which let's users:
        - convert documents
        - store documents

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    template_name: str = "zhehe_user_app/zhehe_home/new_doc.html"
    text_area = TextInput()
    messages: List[str] = []
    if request.method == 'POST':
        text_area = TextInput(request.POST)
        if text_area.is_valid():

            if request.POST.get('convert'):
                try:
                    store_as_pdf(text_area.cleaned_data['text_area'],
                                 input_format=text_area.cleaned_data['text_format'],
                                 usr_id=str(request.user.id))
                except Exception as e:
                    logger.error(e)
            elif request.POST.get('save'):
                logger.error('the save button was clicked')
            print(text_area.cleaned_data)
            messages.append('Dokument erfolgreich konvertiert')
        else:
            print(text_area.errors)

    return render(request=request, template_name=template_name, status=200, context={'text_form': text_area,
                                                                                     'messages': messages})


@verified_email_required
def download(request):
    """
    ``!important!`` This view is only available for users who validated their email address

    This view allows users to download their pdf documents.

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    pass
