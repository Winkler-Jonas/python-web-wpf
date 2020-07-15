from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms import bootstrap, layout


class Newsletter(forms.Form):
    """
    Custom designed newsletter form for bootstrap 4 viewport
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

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
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Vorname', 'label': 'Vorname'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nachname', 'label': 'Nachname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    note = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ihre Nachricht', 'rows': 3}))
    newsletter = forms.BooleanField(label='Newsletter abonnieren', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.fields['name'].label = 'Vorname'
        self.fields['surname'].label = 'Nachname'
        self.fields['email'].label = 'Ihre Kontakt Mail Adresse'
        self.fields['note'].label = 'Ihre Nachrich'

        self.helper.layout = Layout(
            Div('name', css_class='form-group'),
            Div('surname', css_class='form-group'),
            Div('email', css_class='form-group'),
            Div('note', css_class='form-group'),
            Div('newsletter', css_class='form-group'),
            bootstrap.FormActions(
                layout.Submit('submit', 'Senden', css_class='form-group btn btn-success btn-lg')
            )
        )


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
    name = forms.CharField(
        label='Vorname',
        label_suffix='',
        widget=forms.TextInput(attrs={'placeholder': 'Vorname'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nachname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Passwort'}))
    newsletter = forms.BooleanField(label='Newsletter abonnieren', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'

        self.fields['surname'].label = ''
        self.fields['email'].label = 'Ihre Kontakt Mail Adresse'
        self.fields['password'].label = 'Passwort'

        self.helper.layout = Layout(
            Div('name', css_class='form-group'),
            Div('surname', css_class='form-group'),
            Div('email', css_class='form-group'),
            Div('password', css_class='form-group'),
            Div('newsletter', css_class='form-group'),
            bootstrap.FormActions(
                layout.Submit('submit', 'Anmelden', css_class='form-group btn btn-primary btn-lg')
            )
        )

    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        if 'abc' not in name:
            raise forms.ValidationError('Blub')
        else:
            return name
