"""Creating forms for users to login"""
from django import forms
from django.contrib.auth.models import User
from .models import Profile
class LoginForm(forms.Form):
    """Creating the actual form field view"""
    username = forms.CharField(max_length=25, required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    """User registration model form"""
    password = forms.CharField(widget= forms.PasswordInput, label="Password")
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        """Already contained in form"""
        model = User
        fields = ("username", "first_name","email")

    def clean_password2(self):
        """Checking if passwords matches"""
        clean_data = self.cleaned_data
        if clean_data["password"]!=clean_data["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return clean_data["password2"]

class UserEditForm(forms.ModelForm):
    """User Edit form"""
    class Meta:
        """Already made data avaliable"""
        model = User
        fields = ("first_name", "last_name", "email")
class ProfileEditForm(forms.ModelForm):
    """User Profile edit form"""
    class Meta:
        """Already data made available"""
        model = Profile
        fields = ("date_of_birth","photo")
