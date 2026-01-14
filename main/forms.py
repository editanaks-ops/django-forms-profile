from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Message, Profile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    phone_number = forms.CharField(label="Телефон", required=False)
    bio = forms.CharField(
        label="О себе",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone_number", "bio")

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email обязателен.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            # ВАЖНО: поля Profile должны называться phone_number и bio
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "phone_number": self.cleaned_data.get("phone_number", ""),
                    "bio": self.cleaned_data.get("bio", ""),
                }
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("name", "email", "text")
        widgets = {
            "text": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_text(self):
        text = (self.cleaned_data.get("text") or "").strip()
        if len(text) < 10:
            raise forms.ValidationError("Сообщение слишком короткое (минимум 10 символов).")
        if len(text) > 2000:
            raise forms.ValidationError("Сообщение слишком длинное (максимум 2000 символов).")
        return text
