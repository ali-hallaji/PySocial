# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import CaptchaField


class RegisterUsersForm(forms.Form):

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': "input",
                'type': "text",
                'placeholder': 'نام کاربری',
                'autocomplete': 'off',
                'value': ""
            }
        )
    )

    email = forms.EmailField(
        label='ایمیل:',
        widget=forms.EmailInput(
            attrs={'placeholder': 'name@yourdomain.com', 'tabindex': '7'})
    )

    password1 = forms.CharField(
        min_length=8,
        label='گذرواژه:',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'حداقل 8 کاراکتر', 'tabindex': '8'})
    )

    password2 = forms.CharField(
        min_length=8,
        label='تکرار گذرواژه:',
        widget=forms.PasswordInput(attrs={'tabindex': '9'})
    )
    captcha = CaptchaField()

    def clean(self):
        cleaned_data = super(RegisterUsersForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            self.add_error(
                'password1',
                'رمز عبورهای وارد شده، یکسان نمی باشد.'
            )
