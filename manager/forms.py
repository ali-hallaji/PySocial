# Django Import
from django import forms
from ckeditor.widgets import CKEditorWidget


class HomeForm(forms.Form):
    body = forms.CharField(
        label='body',
        required=False,
        widget=CKEditorWidget()
    )
    news = forms.CharField(
        label='news',
        required=False,
        widget=CKEditorWidget()
    )
