from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

# ==========================================
# User Registration Form
# ==========================================
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # ensure email is required

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap styling
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        # Add placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    # Check if email already exists
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Email already exists. Please choose another.")
        return email

    # Username uniqueness is already handled by UserCreationForm
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user




# ==========================================
# User Login Form
# ==========================================
class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


# ==========================================
# Profile Update Form
# ==========================================
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })


# ==========================================
# Password Change Form
# ==========================================
class StyledPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap class
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        # Add placeholders
        self.fields['old_password'].widget.attrs.update({
            'placeholder': 'Old Password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'placeholder': 'New Password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'placeholder': 'Confirm New Password'
        })