from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from crispy_forms import bootstrap, layout


class Newsletter(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline justify-content-center'
        self.helper.layout = Layout(

            Div('name', css_class=['form-group', 'justify-content-center']),
            Div('email', css_class=['form-group', 'justify-content-center']),
            bootstrap.FormActions(
                layout.Submit('submit', 'Abonnieren!', css_class='btn btn-primary'))
        )

