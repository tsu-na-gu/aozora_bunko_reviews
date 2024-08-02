from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.models import User

from user_account.models import Profile


class CustomLoginForm(LoginForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}), label='パスワード')


class CustomSignupForm(SignupForm):
    password2 = forms.CharField(label='パスワード確認', widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("2つのパスワードが一致しません。")
        else:
            user.save()
            return user

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'password2')


