from django import forms
from .models import CartItem,Rating
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

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
        }