Django Allauth
**************

Beschreibung
------------

CSSing Forms
------------

Einem `Medium Artikel`_ verfasst von Gavin Wiener zu folgen ist es möglich, den allauth-formen CSS-Klassen hinzuzufügen.

.. _Medium Artikel: https://medium.com/@gavinwiener/modifying-django-allauth-forms-6eb19e77ef56

.. code-block:: python

    class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'red-border'
        })

Nach vielen Versuchen und Tests konnte ich dieses Verhalten nicht bestätigen. Es war mir nicht möglich, auf diese Art
den Formen CSS-Klassen hinzuzufügen. Weshalb ich mich für eine etwas unsaubere jedoch funktionierende Front-End-Variante
entschieden habe.

.. code-block:: javascript

    $(function () {
        // Add form-control css-classes to input
        $('#id_email').addClass('form-control');
        $('#id_password1').addClass('form-control');
        $('#id_password2').addClass('form-control');
        $('#id_password').addClass('form-control');
        $('#id_login').addClass('form-control');
        $('#id_oldpassword').addClass('form-control');
    });

Durch diese Javascriptfunktion ist es möglich, nachträglich CSS-Classen zu den Formen hinzuzufügen. Und so auch weiterhin
Bootstrap für das Stylen dieser zu verwenden. Die Funktion sucht lediglich nach der ID des HTML Elements, welche für
eindeutig ist und fügt dessen Element die Klasse ``form-control`` hinzu. Dies ist eine Bootstrap CSS-Klasse, um Formen
zu stylen.

Verfication Email
-----------------

Die Informationen zu Googles SMTP-Einstellungen können `hier nachgelesen`_ werden.

.. _hier nachgelesen: https://support.google.com/mail/answer/7126229?p=BadCredentials&visit_id=637307618550623949-3936989994&rd=2&authuser=4

In der ``settings.py`` sollte die Einrichtung der E-Mail-Adresse dann wie folgt aufgebaut werden.

.. code-block:: python
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'google-konto@gmail.com'
    EMAIL_HOST_PASSWORD = 'password'
    EMAIL_USE_TLS = True

Des Weiteren muss unter Verwendung dieser Einstellung im Google-Konto eine Einstellung vorgenommen werden, damit
Google das Versenden der Validierungsmail nicht verhindert und den Log-in durch Django ermöglicht. `Weniger sichere Apps gestatten`_

.. _Weniger sichere Apps gestatten: https://myaccount.google.com/lesssecureapps

Manchmal kann es `durch Captchas`_ ebenfalls zu Problemen mit dem Google-Konto kommen. Hier muss man gleichermaßen Einstellungen
im Konto vornehmen.

.. _durch Captchas: https://accounts.google.com/DisplayUnlockCaptcha