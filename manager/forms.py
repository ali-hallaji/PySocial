# Django Import
from django import forms
from ckeditor.widgets import CKEditorWidget

# PySocial Import
from core import cursor


class HomeForm(forms.Form):
    title = forms.CharField(label='Title')
    body = forms.CharField(
        label='body',
        required=False,
        widget=CKEditorWidget()
    )
    kind = forms.CharField(
        label='Kind of Body',
    )
    icon = forms.CharField(label='icon', required=False)
    order = forms.IntegerField(label='order', required=False)


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

        self.fields['groups_name'] = forms.MultipleChoiceField(
            label='Choose your Group',
            required=True,
            choices=groups_list
        )


class BoxForm(forms.Form):
    title = forms.CharField(label='Title')
    title_fa = forms.CharField(label='Title Fa')
    order = forms.IntegerField(label='Box Order')
    description = forms.CharField(
        label='Description',
        required=False,
        widget=CKEditorWidget()
    )
    box_pic = forms.FileField(label='Box Image', required=False)


class ContentForm(forms.Form):
    description = forms.CharField(
        label='Description',
        widget=CKEditorWidget()
    )
    title = forms.CharField(label='Title')
    published = forms.BooleanField(label='Published')
    order = forms.IntegerField(label='Order')

    def __init__(self, *args, **kwargs):
        # Get box name
        boxs = []
        box = list(cursor.box.find({}, {'title': 1}))

        for doc in box:
            boxs.append((doc['_id'], doc['title']))

        # Get parent name
        parents = []
        parent = cursor.settings.find(
            {
                'settings_type': 'Parents'
            },
            {
                'parent_name': 1,
                '_id': 0
            }
        )

        for doc in parent:
            parents.append((doc['parent_name'], doc['parent_name']))

        super(ContentForm, self).__init__(*args, **kwargs)
        self.fields['box_id'] = forms.ChoiceField(
            label='Choose your Box',
            required=True,
            choices=boxs
        )

        self.fields['parent'] = forms.ChoiceField(
            label='Choose your parent name',
            required=True,
            choices=parents
        )


class ParentForm(forms.Form):
    parent_name = forms.CharField(label='Parent Name')
    description = forms.CharField(
        label='Description',
        required=False,
        widget=CKEditorWidget()
    )

    def __init__(self, *args, **kwargs):
        # Get box name
        boxs = []
        box = list(cursor.box.find({}, {'title': 1}))

        for doc in box:
            boxs.append((doc['title'], doc['title']))

        super(ParentForm, self).__init__(*args, **kwargs)
        self.fields['box'] = forms.ChoiceField(
            label='Choose your Box',
            required=True,
            choices=boxs
        )
