from django import forms


class ForumForm(forms.Form):
    sort = forms.IntegerField(label='sort')
    description = forms.CharField(
        label='description',
        widget=forms.Textarea()
    )
    title = forms.CharField(label='title')
    title_en = forms.CharField(label='title en')
