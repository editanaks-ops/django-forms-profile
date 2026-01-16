from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegistrationForm, MessageForm
from .models import Profile, Message


def home_view(request):
    # Если уже авторизован — сразу профиль
    if request.user.is_authenticated:
        return redirect("profile")
    return redirect("login")


def register_view(request):
    # Если уже авторизован — не надо регистрироваться
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # если Profile не создан (на всякий случай) — создаём
            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "phone_number": form.cleaned_data.get("phone_number", ""),
                    "bio": form.cleaned_data.get("bio", ""),
                },
            )

            login(request, user)
            messages.success(request, "Регистрация успешна. Вы вошли в систему.")
            return redirect("profile")
        else:
            messages.error(request, "Проверьте введённые данные.")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    # берем next из GET или POST
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    # если уже залогинен — сразу в профиль
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Вы вошли в систему.")

                # редиректим только если next безопасный
                if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)

                return redirect("profile")

            messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Проверьте введённые данные.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "next": next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("login")


@login_required
def profile_view(request):
    # профиль должен быть — но на всякий случай
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # сообщения пользователя (если модель Message связана с user)
    messages_list = Message.objects.filter(user=request.user).order_by("-id")

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "messages_list": messages_list,
        },
    )


@login_required
def message_create_view(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.save()
            messages.success(request, "Сообщение отправлено.")
            return redirect("profile")
        else:
            messages.error(request, "Проверьте введённые данные.")
    else:
        form = MessageForm()

    return render(request, "message_form.html", {"form": form})







