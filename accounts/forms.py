from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser


# =========================
# User registration form
# =========================
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone_number",
            "address",
            "profile_picture",
            "preferred_payment_method",
            "role",
            "item_type",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "preferred_payment_method": forms.Select(attrs={"class": "form-select"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "item_type": forms.Select(attrs={"class": "form-select"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


# =========================
# User login form (FIXED)
# =========================
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            # 🔍 Allow login with email
            if "@" in username:
                try:
                    user_obj = CustomUser.objects.get(email=username)
                    username = user_obj.username
                except CustomUser.DoesNotExist:
                    pass

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError("Invalid username/email or password")

            if not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")

        return self.cleaned_data


# =========================
# Profile settings form
# =========================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "profile_picture",
            "preferred_payment_method",
            "role",
            "item_type",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "preferred_payment_method": forms.Select(attrs={"class": "form-select"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "item_type": forms.Select(attrs={"class": "form-select"}),
        }