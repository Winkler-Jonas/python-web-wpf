from django.shortcuts import render, HttpResponse
from .forms import Newsletter, Contact
# Create your views here.


def index(request):
    if request.method == 'POST':
        newsletter_form: Newsletter = Newsletter(request.POST)
        print(newsletter_form)
    if request.method == 'GET':
        template_name: str = "zhehe_index/index_main.html"
        newsletter_form = Newsletter
        contact_form = Contact
        return render(request=request, template_name=template_name, status=200, context={'newsletter': newsletter_form,
                                                                                         'contact': contact_form})
