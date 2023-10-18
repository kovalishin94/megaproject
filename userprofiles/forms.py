from django import forms
from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from .models import Userprofile
from django.contrib.auth.models import User


class UserUpdateForm(Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(
        attrs={'class': 'form-control'}), max_length=50)
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        count_digits = 0
        count_lower_case = 0
        count_upper_case = 0
        for i in password1:
            if i.isdigit():
                count_digits += 1
            if i.islower():
                count_lower_case += 1
            if i.isupper():
                count_upper_case += 1
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        if len(password1) < 8:
            raise ValidationError('Пароль должен быть не менее 8 символов')
        if not count_digits or not count_upper_case or not count_lower_case:
            raise ValidationError(
                'Пароль не соответсвтует требованиям безопасности')


class UserCreationForm(UserUpdateForm):
    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        for i in User.objects.values('username'):
            if username == i['username']:
                raise ValidationError('Пользователь с таким именем существует')


class PrivilegeChooseForm(ModelForm):
    class Meta:
        model = Userprofile
        fields = [
            'privileges'
        ]
        widgets = {
            'privileges': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
