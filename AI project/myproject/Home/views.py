from django.shortcuts import render,redirect
from .forms import AddToCartForm
from .models import CartItem
from django.shortcuts import HttpResponse
from .database_operations import fetch_data_from_database
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm , LoginForm


def home(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # Get the current logged-in user
            user = request.user

            # Extract form data
            product_name = form.cleaned_data['product_name']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']

            # Create a new CartItem object with the user and save it to the database
            CartItem.objects.create(user=user, product_name=product_name, price=price, quantity=quantity)

            # Redirect to cart page or any other page
            return redirect('home')
    else:
        form = AddToCartForm()
    return render(request, 'index.html', {'form': form})

def my_view(request):
    # Your view logic here

    # Fetch data from SQLite database
    data = fetch_data_from_database()

    # Process data or return it in the response
    return HttpResponse(data)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})