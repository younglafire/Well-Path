from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Category, Unit, Goal

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
        fields = ("username", "email", "password1", "password2")

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "description", "category", "unit", "target_value", "deadline", "is_public"]
        labels = {
            "is_public": "Public",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ban đầu Unit rỗng
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