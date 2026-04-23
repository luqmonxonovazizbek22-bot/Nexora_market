from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.models import ModelForm
from app.models import Contact, User


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro‘yxatdan o‘tgan")
        return email


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField()