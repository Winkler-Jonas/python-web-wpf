from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field

CONCERNS: tuple = (('', 'Wählen Sie ein Anliegen'),
                   ('VV', 'Verbesserungsvorschlag'),
                   ('B', 'Beschwerde'),
                   ('AA', 'Andere Anliegen'))

FORMATS: tuple = (('md', 'Markdown'),
                  ('rst', 'RestructuredText'))


class Newsletter(forms.Form):
    """
    Custom designed newsletter form for bootstrap 4 viewport
    """
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                         'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                            'class': 'form-control'}),
                             error_messages={'required': 'Bitte geben Sie eine gültige Email-Adresse ein'})


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


class TextInput(forms.Form):
    """
    Custom designed TxtInput form for bootstrap 4 viewport
    """
    text_format = forms.ChoiceField(choices=FORMATS,
                                    label='Format',
                                    widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    text_area = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Geben Sie hier Ihren Text ein ...',
                                                             'class': 'form-control textarea'}))
