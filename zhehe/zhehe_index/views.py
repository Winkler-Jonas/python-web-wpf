from django.shortcuts import render, HttpResponse
from .forms import Newsletter, Contact
from .models import Contact_Info, Subscriber
# Create your views here.

import logging
logger = logging.getLogger(__name__)


def index(request):
    template_name: str = 'zhehe_index/index_main.html'
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
