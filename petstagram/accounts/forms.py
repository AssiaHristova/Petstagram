from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from core.forms import BootstrapFormMixin
from petstagram.accounts.models import Profile

UserModel = get_user_model()


class LoginForm(forms.Form):
    user = None
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class LoginForm2(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email',]


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image',]
