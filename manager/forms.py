# Django Import
from django import forms
from ckeditor.widgets import CKEditorWidget

# PySocial Import
from core import cursor


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


class GroupForm(forms.Form):
    group_name = forms.CharField(label='Group Name', max_length=100)

    def __init__(self, *args, **kwargs):
        views_name = kwargs.pop('views_name')

        super(GroupForm, self).__init__(*args, **kwargs)

        self.fields['views'] = forms.MultipleChoiceField(
            label='Check permission from core',
            choices=[(x, x) for x in views_name],
            required=False
        )


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=15, required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        required=False
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        required=False
    )
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        groups = cursor.acl_group.find({}, {'group_name': 1})
        groups_list = []

        for doc in groups:
            groups_list.append((doc['group_name'], doc['group_name']))

        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['groups_name'] = forms.ChoiceField(
            label='Choose your Group',
            required=True,
            choices=groups_list
        )
