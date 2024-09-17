from django import forms
from .models import Product ,AppUser
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib.auth.models import User
import requests
from django.core.exceptions import ValidationError

class ProductDetail(forms.ModelForm):

    class Meta:
        model=Product
        fields=['name','desc','price','image','category','stock']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )



class SignUp(forms.ModelForm):  # Use ModelForm for model-based forms
    class Meta:
        model = AppUser
        fields = ['username', 'email', 'contact', 'address', 'password']
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Mobile Number'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Call the email verification API (Hunter.io or another provider)
        api_key = "d9f88867b0a997ef8e5b91a44b55b8ba2476e00f"  # Replace with your actual API key
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"

        try:
            response = requests.get(url)
            result = response.json()

            if result['data']['result'] != 'deliverable':
                raise ValidationError("Email ID not found. Please use a valid email address.")
        except requests.RequestException:
            raise ValidationError("Error verifying email. Please try again later.")

        return email        
      
