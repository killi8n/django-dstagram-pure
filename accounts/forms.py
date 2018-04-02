from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("password not match...")
        if len(cd['password2']) < 3:
            raise forms.ValidationError("password is too short!")
        return cd['password2']

    def clean_username(self):
        cd = self.cleaned_data
        if len(cd['username']) < 4:
            raise forms.ValidationError("username is too short!")
        return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if len(cd['email']) < 0:
            raise forms.ValidationError("이메일을 입력하여 주세요.")
        if not "@" in cd['email']:
            raise forms.ValidationError("이메일주소만 사용하여주세요.")
        return cd['email']