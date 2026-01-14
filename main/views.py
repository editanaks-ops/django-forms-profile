from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, MessageForm, RegistrationForm  # ВАЖНО: одно имя формы регистрации
from .models import Message


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна. Вы вошли в систему.")
            return redirect("profile")
        else:
            messages.error(request, "Проверьте введённые данные.")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

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

                # безопасный редирект на next (если был)
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
    msgs = request.user.messages.order_by("-created_at")
    return render(request, "profile.html", {"messages_list": msgs})


def message_create_view(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            messages.success(request, "Сообщение отправлено.")
            return redirect("profile" if request.user.is_authenticated else "message")
        else:
            messages.error(request, "Проверьте сообщение.")
    else:
        form = MessageForm()

    return render(request, "message_form.html", {"form": form})







