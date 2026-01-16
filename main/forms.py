from django import forms
from django.contrib.auth.models import User

from .models import Message, Profile


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)
    phone_number = forms.CharField(label="Телефон", required=False)
    bio = forms.CharField(label="О себе", required=False, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if not email:
            raise forms.ValidationError("Email обязателен.")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают.")
        if p1 and len(p1) < 8:
            self.add_error("password1", "Пароль должен быть минимум 8 символов.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get("phone_number", ""),
                bio=self.cleaned_data.get("bio", ""),
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("name", "email", "text")
        widgets = {"text": forms.Textarea(attrs={"rows": 5})}

    def clean_text(self):
        text = (self.cleaned_data.get("text") or "").strip()
        if len(text) < 10:
            raise forms.ValidationError("Сообщение слишком короткое (минимум 10 символов).")
        if len(text) > 2000:
            raise forms.ValidationError("Сообщение слишком длинное (максимум 2000 символов).")
        return text
