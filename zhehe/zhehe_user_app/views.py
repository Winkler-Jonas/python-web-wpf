import re
from pathlib import Path
from typing import Optional, Dict, List

from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import Newsletter, Contact, TextInput, DocumentSave
from .models import Contact_Info, Subscriber, Document, DocumentPage
from .tasks import convert_doc, save_doc, PandocException, FileNotFoundException, UnknownModel, ImgConvertError
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
    doc_save_form = DocumentSave()
    messages: List[str] = []
    images: QuerySet = DocumentPage.objects.none()
    if request.method == 'POST':
        text_area = TextInput(request.POST)
        doc_save_form = DocumentSave(request.POST)
        if text_area.is_valid() and request.POST.get('convert'):
            # collect data from form
            text: str = text_area.cleaned_data['text_area']
            input_format: str = text_area.cleaned_data['text_format']
            try:
                pdf_file: str = convert_doc(text=text, input_format=input_format, usr_id=str(request.user.id))
                images = DocumentPage.objects.filter(doc_fk=pdf_file).order_by('doc_page_no')
                messages.append('Dokument erfolgreich konvertiert')
            except (PandocException, ImgConvertError) as e:
                messages.append(e.msg)
            except UnknownModel as e:
                pass  # not supposed to be seen by user
        elif doc_save_form.is_valid() and request.POST.get('save'):
            doc_name: str = doc_save_form.cleaned_data['name']
            doc_info: str = doc_save_form.cleaned_data['info'] if doc_save_form.cleaned_data['info'] else ''
            try:
                pdf_file: str = save_doc(doc_name=doc_name, doc_info=doc_info, usr_id=str(request.user.id))
                images = DocumentPage.objects.filter(doc_fk=pdf_file).order_by('doc_page_no')
                file_saved = Document.objects.get(document_path=pdf_file)
                text_area = TextInput(initial={'text_area': file_saved.document_text,
                                               'text_format': file_saved.document_format})
                messages.append('Dokument erfolgreich gespeichert')
            except FileNotFoundException as e:
                messages.append(e.msg)
            except UnknownModel as e:
                pass    # not supposed to be seen by user
    return render(request=request, template_name=template_name, status=200, context={'text_form': text_area,
                                                                                     'messages': messages,
                                                                                     'images': images,
                                                                                     'doc_save': doc_save_form})


@verified_email_required
def download(request, document: str):
    """
    ``!important!`` This view is only available for users who validated their email address

    This view allows users to download their pdf documents.

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :param document: The document path to be downloaded
    :type document: str
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    if request.method == 'GET':
        if (pdf_file := Path(document)).exists():
            db_file = Document.objects.get(document_path=str(pdf_file))
            with pdf_file.open(mode='rb') as fd:
                response = HttpResponse(fd.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={db_file.document_name}.pdf'
                return response
    return redirect(reverse('zhehe:home'))


@verified_email_required()
def edit(request, document: str):
    """
    ``!important!`` This view is only available for users who validated their email address

    View basically renders the same output as ``new_doc`` however, the text-area and the images
    will be the from the start

    :param request: Django request Object
    :type request: django.core.handlers.wsgi.WSGIRequest
    :param document: The document path to be edited
    :type document: str
    :return: Django render object containing HttpResponse
    :rtype: django.http.response.HttpResponse
    """
    template_name: str = "zhehe_user_app/zhehe_home/new_doc.html"
    messages: List[str] = []
    text_area = TextInput()
    doc_save_form = DocumentSave()
    messages: List[str] = []
    images: QuerySet = DocumentPage.objects.none()
    if request.method == 'GET':
        if (pdf_file := Path(document)).exists():
            db_tuple = Document.objects.get(document_path=document)

            text_area = TextInput(initial={'text_area': db_tuple.document_text,
                                           'text_format': db_tuple.document_format})
            doc_save_form = DocumentSave(initial={'name': db_tuple.document_name,
                                                  'info': db_tuple.document_info})
            images: QuerySet = DocumentPage.objects.filter(doc_fk=document).order_by('doc_page_no')
        else:
            redirect_template: str = 'zhehe_user_app/zhehe_home/overview.html'
            messages.append('Leider konnte Ihr Dokument nicht geladen werden.'
                            'Bitte nehmen Sie Kontak mit uns auf')

            return render(request=request, template_name=redirect_template,
                          context={'documents': Document.objects.filter(document_owner=request.user.id),
                                   'messages': messages})
    elif request.method == 'POST':
        text_area = TextInput(request.POST)
        doc_save_form = DocumentSave(request.POST)
        if text_area.is_valid() and request.POST.get('convert'):
            # collect data from form
            text: str = text_area.cleaned_data['text_area']
            input_format: str = text_area.cleaned_data['text_format']
            try:
                pdf_file: str = convert_doc(text=text, input_format=input_format, usr_id=str(request.user.id))
                images = DocumentPage.objects.filter(doc_fk=pdf_file).order_by('doc_page_no')
                messages.append('Dokument erfolgreich konvertiert')
            except (PandocException, ImgConvertError) as e:
                messages.append(e.msg)
            except UnknownModel as e:
                pass  # not supposed to be seen by user
        elif doc_save_form.is_valid() and request.POST.get('save'):
            doc_name: str = doc_save_form.cleaned_data['name']
            doc_info: str = doc_save_form.cleaned_data['info'] if doc_save_form.cleaned_data['info'] else ''
            try:
                pdf_file: str = save_doc(doc_name=doc_name, doc_info=doc_info, usr_id=str(request.user.id))
                images = DocumentPage.objects.filter(doc_fk=pdf_file).order_by('doc_page_no')
                file_saved = Document.objects.get(document_path=pdf_file)
                text_area = TextInput(initial={'text_area': file_saved.document_text,
                                               'text_format': file_saved.document_format})
                messages.append('Dokument erfolgreich gespeichert')
            except FileNotFoundException as e:
                messages.append(e.msg)
            except UnknownModel as e:
                pass  # not supposed to be seen by user
    return render(request=request, template_name=template_name, status=200, context={'text_form': text_area,
                                                                                     'messages': messages,
                                                                                     'images': images,
                                                                                     'doc_save': doc_save_form})


def delete(request, document: str):
    if request.method == 'POST':
        if (pdf_file := Path(document)).exists():
            files_to_delete: List[Path] = [Path(re.sub(r'(?<=^/)media(?=/)', 'media_content', doc_path['doc_page_path'])) for doc_path in DocumentPage.objects.all().values('doc_page_path').filter(doc_fk_id=document)]
            DocumentPage.objects.filter(doc_fk=document).delete()
            Document.objects.get(document_path=document).delete()
            for file in files_to_delete + [pdf_file]:
                file.unlink()
    return redirect(reverse('zhehe:home'))
