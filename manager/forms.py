#! -*- coding:utf-8 -*-
from bson.objectid import ObjectId

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

    def __init__(self, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'


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

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'


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

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'


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

    def __init__(self, *args, **kwargs):
        super(BoxForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'


class ContentForm(forms.Form):
    description = forms.CharField(
        label='Description',
        widget=CKEditorWidget()
    )
    title = forms.CharField(label='Title')
    published = forms.BooleanField(label='Published', required=False)
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
                'box': 1,
                '_id': 1
            }
        )

        for doc in parent:
            text = "{0} | {1}".format(
                doc['box'],
                doc['parent_name'].encode('utf-8')
            )
            value = "{0}|{1}".format(
                doc['box'],
                doc['parent_name'].encode('utf-8')
            )
            parents.append((value, text))

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

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'

    def clean(self):
        if not self.cleaned_data.get('published', None):
            self.cleaned_data['published'] = False


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

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs['required'] = 'required'


class ForumForm(forms.Form):
    sort = forms.IntegerField(label='sort')
    description = forms.CharField(
        label='description',
        widget=forms.Textarea()
    )
    title = forms.CharField(label='title')
    title_en = forms.CharField(label='title en')

    def __init__(self, *args, **kwargs):
        boxs = [ObjectId('57060eed6007f0fb6eb95700'), "PySocial"]
        box = list(cursor.box.find({}, {'title': 1}))

        for doc in box:
            boxs.append((doc['title'], doc['title']))

        super(ForumForm, self).__init__(*args, **kwargs)
        self.fields['box'] = forms.ChoiceField(label='Box', choices=boxs)


class LessonForm(forms.Form):
    body = forms.CharField(
        label='Body',
        widget=CKEditorWidget()
    )
    published = forms.BooleanField(label='Published', initial=False)

    def __init__(self, *args, **kwargs):
        boxs = []
        box = list(cursor.box.find({}, {'title': 1}))

        for doc in box:
            boxs.append((doc['_id'], doc['title']))

        contents = []
        content = list(cursor.contents.find({}, {'title': 1, 'box_id': 1}))

        for doc in content:
            for item in boxs:
                if doc['box_id'] == item[0]:
                    contents.append(
                        (
                            doc['_id'],
                            (item[1] + " | " + doc['title'])
                        )
                    )

        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['box_id'] = forms.ChoiceField(
            label='Choose your Box',
            required=True,
            choices=boxs
        )
        self.fields['content_id'] = forms.ChoiceField(
            label='Choose your Content',
            required=True,
            choices=contents
        )
