Forms
*****

Setup
-----

Forms dienen der Kommunikation mit Webseiten. Herkömmlich werden diese in einfachem HTML Kontext deklariert und
designed. Dies führt jedoch oft zu Komplikationen bezüglich der Darstellung dieser Forms. Bootstrap stellt an dieser Stelle einen
sinnvollen Ausweg zur Verfügung, um diese Forms für alle Geräte und Browser wie gedacht darzustellen. Das Django-Framework
hingegen bietet in diesem Fall eigene Lösungen, um Forms zu implementieren, um übertragene Informationen im backend einfach zu
verarbeiten sind. Hier kommt das **crispy_forms** Package zum Einsatz. Dieses verbindet die Kompatibilität der Django
Forms und die Dahrstellungsüberlegenheit von Bootstrap.

**Crispy Forms** können sowohl unter Anacoonda als auch unter PIP installiert werden.

Anaconda :ref:`(vgl. Anaconda Inc. o. J.)<Literaturverzeichnis>`

.. code-block:: bash

    $ conda install -c conda-forge django-crispy-forms

PIP :ref:`(vgl. Python Software Foundation 2020)<Literaturverzeichnis>`

.. code-block:: bash

    $ pip install django-crispy-forms

Um das Package unter Django zu nutzen, muss es unter **settings.py** zu den Apps hinzugefügt werden.

.. code-block:: python

    INSTALLED_APPS = [
        'django.contrib.admin',
        'crispy_forms',
    ]

.. _Crispy-Forms-Laden:

Um die crispy forms nun auch in den Templates verwenden zu können, müssen diese wie static Files geladen werden.
``{% load crispy_forms_tags %}``

Forms erstellen
---------------

forms.py
^^^^^^^^

Django Forms sollten in den jeweiligen Applikation in der Datei **forms.py** erstellt werden.

.. code-block:: python

    # Django Form import
    from django import forms
    # Crispy Form Helper import
    from crispy_forms.helper import FormHelper
    # Crispy CSS Form Helper imports
    from crispy_forms.layout import Layout, Div
    # Crispy further CSS Form Helper imports
    from crispy_forms import bootstrap, layout

    # New Class defining the Form to use in Python-Django-Framework
    class Newsletter(forms.Form):
        """
        Custom designed newsletter form for bootstrap 4 viewport
        """
        # In this case we use two form-inputs.
        # The placeholder defines what will be displayed to the user prior to the users input
        name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

        # Initialize the form with Bootstrap classes
        def __init__(self, *args, **kwargs):
            """
            Add layout to form attributes
            """
            super().__init__(*args, **kwargs)
            # First create a FormHelper
            self.helper = FormHelper()
            # Define what Class the overall form shall inherit
            self.helper.form_class = 'form-inline justify-content-center'
            # Define Bootstrap design for children of the form
            self.helper.layout = Layout(
                # First we define the field name which in this case ought to be at the center of the page
                Div('name', css_class=['form-group', 'justify-content-center']),
                # Second we define the field email which is to the right of name
                Div('email', css_class=['form-group', 'justify-content-center']),
                # We define an BootstrapAction to receive a properly defined bootstrap button to submit the user input
                bootstrap.FormActions(
                    # First Argument ist the action to be taken when clicked
                    # Secondary the label to be displayed on the butten
                    # Third the Bootstrap Class to be inherited
                    layout.Submit('submit', 'Abonnieren!', css_class='btn btn-primary'))
            )

view.py
^^^^^^^

Nach Erstellung der Form, muss diese der Webseite zur Verfügung gestellt werden. Dies kann durch das **Context-Dictionary**
in der **views.py** druchgeführt werden. Hier ein Beispiel, wie dies druchgeführt werden kann.

.. code-block:: python

    def index(request):
        # Wenn das Formular ausgefüllt wurde, handelt es sich um einen POST request
        if request.method == 'POST':
            newsletter_form: Newsletter = Newsletter(request.POST)
            # Weitere Aktionen mit den gesammelten Daten druchführen
        # Wenn die normale Webseite mit dem Formular geladen wird
        elif request.method == 'GET':
            template_name: str = "zhehe_index/index_main.html"
            # Bereitstellen des Formulars
            form = Newsletter
            # Mithilfe des Context-Dictionaries in der render-funktion, kann die Form an das Template geschickt werden
            return render(request=request, template_name=template_name, status=200, context={'form': form})

template.html
^^^^^^^^^^^^^

Anschließend muss die Form nur noch in das Template eingebunden werden. Dies ist vergleichsweise einfach, da bereits alle
wichtigen Styles übergeben wurden. Um die **crispy_forms** in einem Template nutzen zu können, müssen diese zunächst
:ref:`geladen<Crispy-Forms-Laden>` werden.

.. code-block:: html

    {% block newsletter %}
        {% crispy form %}
    {% endblock %}

Diese Schreibweise genügt, um eine vollständige Form in HTML darzustellen, es werden keine weiteren Styles oder Ähnliches
benötigt. Diese sehr unkomplizierte Implementation ermöglicht es dem Entwickler eine erhebliche Zeitersparnis, da die Form
sehr einfach wiederverwendet werden kann und die Nutzerdaten sicher und einfach abgegriffen werden können.

Weiteres über **Crispy Forms** kann selbstverständlich in der `Dokumentation`_ nachgelesen werden.


.. _Dokumentation: https://django-crispy-forms.readthedocs.io/en/latest/