from django import forms
from .models import CartItem
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User  # Import the User model


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product_name', 'price', 'quantity']
        
        
# Home/forms.py


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')