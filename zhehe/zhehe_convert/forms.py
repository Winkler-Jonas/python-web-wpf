from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms import bootstrap, layout


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