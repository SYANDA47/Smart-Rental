from django import forms
from .models import RentalItem, Rental


class RentalItemForm(forms.ModelForm):
    """Form for owners or guests to list or update their items."""
    include_owner_name = forms.BooleanField(
        required=False,
        label="Include owner's name",
        help_text="Check this box if you want your name shown with the item."
    )

    class Meta:
        model = RentalItem
        fields = [
            "title",
            "description",
            "price_per_day",
            "image",
            "available_from",
            "available_to",
            # ✅ we expose include_owner_name here, but map it manually in the view
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter item name"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe the item..."
            }),
            "price_per_day": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Daily rental price"
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "available_from": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "available_to": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
        }

    def save(self, commit=True, owner=None):
        """Custom save to map include_owner_name → show_owner_name."""
        instance = super().save(commit=False)
        instance.show_owner_name = self.cleaned_data.get("include_owner_name", False)
        if owner:
            instance.owner = owner
        if commit:
            instance.save()
        return instance


class RentalForm(forms.ModelForm):
    """Form for renters to book an item for specific dates."""
    class Meta:
        model = Rental
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("The end date cannot be before the start date.")
        return cleaned_data
