from datetime import datetime, timedelta
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Goal
from taxonomy.models import Category, Unit


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class GoalForm(forms.ModelForm):
    from taxonomy.models import Category, Unit

    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control modern-form-control",
            "placeholder": "Goal Title",
        })
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "class": "form-control modern-form-control",
            "placeholder": "Describe your goal...",
            "rows": 3,
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            "class": "form-select modern-form-control",
        })
    )
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.none(),
        required=True,
        widget=forms.Select(attrs={
            "class": "form-select modern-form-control",
        })
    )
    target_value = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={
            "class": "form-control modern-form-control",
            "placeholder": "Target value",
            "min": "0",
            "step": "0.1",
        })
    )
    deadline = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control modern-form-control",
            "min": date.today().strftime("%Y-%m-%d"),
            "max": (date.today() + timedelta(days=730)).strftime("%Y-%m-%d"),
        })
    )
    is_public = forms.BooleanField(
        required=False,
        label="Public",
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input modern-checkbox",
            "style": "accent-color: var(--primary-600); width: 1.5em; height: 1.5em;",
        })
    )

    class Meta:
        model = Goal
        fields = ["title", "description", "category", "unit", "target_value", "deadline", "is_public"]
        labels = {
            "is_public": "Public",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["unit"].queryset = Unit.objects.none()
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                category = Category.objects.get(pk=category_id)
                self.fields["unit"].queryset = category.units.all()
            except (ValueError, Category.DoesNotExist):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields["unit"].queryset = self.instance.category.units.all()

    def clean_deadline(self):
        """Validate that deadline is not too far in the future (max 2 years)."""
        deadline = self.cleaned_data.get('deadline')
        if deadline:
            max_deadline = date.today() + timedelta(days=730)  # 2 years
            if deadline > max_deadline:
                raise ValidationError(
                    f"Deadline cannot be more than 2 years from today. "
                    f"Maximum deadline: {max_deadline.strftime('%Y-%m-%d')}"
                )
            if deadline < date.today():
                raise ValidationError("Deadline cannot be in the past.")
        return deadline


class GoalEditForm(GoalForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].disabled = True
        self.fields["unit"].disabled = True
