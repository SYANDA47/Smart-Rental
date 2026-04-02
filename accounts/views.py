from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomLoginForm, ProfileForm


# Register new user
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # ✅ Let the form handle password hashing
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            # Auto-login after registration
            login(request, user)

            # Redirect based on role
            if user.role == "owner":
                return redirect("owner_dashboard")
            else:
                return redirect("renter_dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


# Login existing user
def login_view(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if user is not None and user.is_active:
                login(request, user)

                # Redirect based on role
                if user.role == "owner":
                    return redirect("owner_dashboard")
                else:
                    return redirect("renter_dashboard")
            else:
                messages.error(request, "Account inactive or invalid.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, "accounts/login.html", {"form": form})


# Logout user
def logout_view(request):
    logout(request)
    return redirect("login")


# Dashboard (role-aware landing page)
@login_required
def dashboard(request):
    if request.user.role == "owner":
        return redirect("owner_dashboard")
    return redirect("renter_dashboard")


# Profile settings (edit user details)
@login_required
def profile_settings(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile_settings")
    else:
        form = ProfileForm(instance=user)

    return render(request, "accounts/profile_settings.html", {"form": form})