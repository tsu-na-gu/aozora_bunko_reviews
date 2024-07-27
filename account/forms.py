from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import Profile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}))

    # def __init__(self, *args, **kwargs):
    #     super(CustomLoginForm, self).__init__(*args, **kwargs)


class CustomRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}))
    password2 = forms.CharField(label='パスワード確認', widget=forms.PasswordInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-gray-300 p-2 rounded w-full'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("2つのパスワードが一致しません。")
        return cd['password2']

