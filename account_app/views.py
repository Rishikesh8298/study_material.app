from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from module.password_validator import is_valid_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password


def signup(request):
    """Create an account."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Your password does not be matched")
            return render(
                request,
                "account/signup.html",
            )
        if len(password) < 8:
            messages.error(request, "Your password must be 8 character")
            return render(
                request,
                "account/signup.html",
            )
            # Password Validation
        if not is_valid_password(password):
            messages.error(request, "Your password is not strong.")
            return render(
                request,
                "account/signup.html",
            )

        if (
                len(User.objects.filter(username=name)) == 0
                and len(User.objects.filter(email=email)) == 0
        ):
            User.objects.create_user(username=name, email=email, password=password)
            messages.success(
                request, "Successfully registered.Please login with your username."
            )
            return render(
                request,
                "account/signup.html",
            )
        else:
            messages.error(request, "Already an User")
            return render(
                request,
                "account/signup.html",
            )
    return render(
        request,
        "account/signup.html",
    )


def signin(request):
    """Check User credential for using learning status"""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        log = authenticate(username=username, password=password)
        if log is not None:
            login(request, log)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
    return render(
        request,
        "account/login.html",
    )


@login_required(login_url="/")
def user_logout(request):
    """Logout the active user and redirect to home page"""
    request.session.flush()
    logout(request)
    return redirect("home")


@login_required(login_url="/")
def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        if not check_password(old_password, user.password):
            messages.error(request, "Current password is incorrect.")
            return render(request, "account/change_password.html")

        if not new_password:
            messages.error(request, "New password cannot be empty.")
            return render(request, "account/change_password.html")

        if len(new_password) < 8:
            messages.error(request, "New password must be at least 8 characters long.")
            return render(request, "account/change_password.html")

        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match.")
            return render(request, "account/change_password.html")

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Your password has been changed successfully.")
        return render(request, "account/change_password.html")

    return render(request, "account/change_password.html")
