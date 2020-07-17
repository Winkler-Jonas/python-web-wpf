from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms import bootstrap, layout
from allauth.account.forms import SignupForm

CONCERNS: tuple = (('', 'Wählen Sie ein Anliegen'),
                   ('VV', 'Verbesserungsvorschlag'),
                   ('B', 'Beschwerde'),
                   ('AA', 'Andere Anliegen'))


class Newsletter(forms.Form):
    """
    Custom designed newsletter form for bootstrap 4 viewport
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """
        Add layout to form attributes
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline justify-content-center'
        self.helper.layout = Layout(

            Div('name', css_class='form-group justify-content-center'),
            Div('email', css_class='form-group justify-content-center'),
            bootstrap.FormActions(
                layout.Submit('submit', 'Abonnieren!', css_class='btn btn-primary'))
        )


class Contact(forms.Form):
    """
    Custom designed contact form for bootstrap 4 viewport
    """
    concern = forms.ChoiceField(choices=CONCERNS,
                                label='Anliegen',
                                widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Vorname',
                                                         'class': 'form-control'}),
                           label='Vorname',
                           error_messages={'required': 'Bitte geben Sie Ihren Vornamen ein'})
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nachname',
                                                            'class': 'form-control'}),
                              label='Nachname',
                              error_messages={'required': 'Bitte geben Sie Ihren Nachnamen ein'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control'}),
                             label='E-Mail',
                             error_messages={'required': 'Bitte geben Sie eine gültige Email ein'})
    note = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ihre Nachricht..',
                                                        'rows': 8,
                                                        'class': 'form-control'}),
                           label='Ihre Nachricht',
                           error_messages={'required': 'Bitte geben Sie eine Nachricht ein'})
    newsletter = forms.BooleanField(label='Ich möchte regelmäßig Updates über Zhehe erhalten.',
                                    required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                    help_text={'required': 'Check-Box'})


class SignIn(forms.Form):
    """
    Custom designed sign-in form for bootstrap 4 viewport
    """
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             label='',
                             error_messages={'required': 'Bitte Ihre User-Mail angeben'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label='',
                               error_messages={'required': 'Bitte geben Sie Ihr Passwort ein'})


class TextInput(forms.Form):
    """
    Custom designed TxtInput form for bootstrap 4 viewport
    """
    text_area = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Geben Sie hier Ihren Text ein ...'}))

    # email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        """
        Add layout to form attributes
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.fields['text_area'].label = ''
        self.helper.layout = Layout(
            Field('text_area', rows=30, css_class='form-control textarea h-100'),
        )


class SignUp(forms.Form):
    """
    Custom designed UserSignUp form for bootstrap 4 viewport
    """
    usr_name = forms.CharField(label='Benutzername',
                               widget=forms.TextInput(attrs={'placeholder': 'Benutzername',
                                                             'class': 'form-control'}))
    name = forms.CharField(label='Vorname',
                           widget=forms.TextInput(attrs={'placeholder': 'Vorname',
                                                         'class': 'form-control'}),
                           error_messages={'required': 'Bitte geben Sie Ihren Vornamen ein'})
    surname = forms.CharField(label='Nachname',
                              widget=forms.TextInput(attrs={'placeholder': 'Nachname',
                                                            'class': 'form-control'}),
                              error_messages={'required': 'Bitte geben Sie Ihren Nachnamen ein'})
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control'}),
                             label='E-Mail',
                             error_messages={'required': 'Bitte geben Sie eine gültige Email ein'})
    password = forms.CharField(label='Passwort',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Passwort',
                                                                 'class': 'form-control'}))
    newsletter = forms.BooleanField(label='Ich möchte regelmäßig Updates über Zhehe erhalten.',
                                    required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                    help_text={'required': 'Check-Box'})
