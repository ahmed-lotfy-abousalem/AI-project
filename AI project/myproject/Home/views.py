from django.shortcuts import render,redirect
from .forms import AddToCartForm,RatingForm
from .models import CartItem,Rating
from django.shortcuts import HttpResponse
from .database_operations import fetch_data_from_database
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import SignupForm , LoginForm
from django.http import JsonResponse
from .models import Rating, CartItem,Product




def home(request):
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # Extract form data
            product_name = form.cleaned_data['product_name']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            rating = int(request.POST.get('rating', 0))  # Get the rating value from the POST data

            # Create a new CartItem object with the user, product details, and rating
            CartItem.objects.create(
                user=request.user,
                product_name=product_name,
                price=price,
                quantity=quantity
            )

            # Create a new Rating object and save it to the database
            Rating.objects.create(
                user=request.user,
                product_name=product_name,
                rating=rating
            )

            # Redirect to home page after adding to cart and rating
            return redirect('home')
    else:
        form = AddToCartForm()

    # Fetch all products from the database
    products = Product.objects.all()
    context = {'products': products, 'form': form}
    return render(request, 'index.html', context)


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        user = request.user  # Assuming user is authenticated

        # Implement collaborative filtering to recommend products
        recommended_products = get_recommended_products(user)

        return JsonResponse({'response': 'Recommended Products:', 'products': recommended_products})
    return JsonResponse({'error': 'Invalid request'})

def get_recommended_products(user):
    # Get user's ratings and cart items
    user_ratings = Rating.objects.filter(user=user)
    user_cart_items = CartItem.objects.filter(user=user)

    # Implement collaborative filtering logic to recommend products
    # This is a simplified example; you may need more sophisticated algorithms
    recommended_products = []
    for rating in user_ratings:
        if rating.rating >= 4:  # Assuming products rated 4 or above are recommended
            recommended_products.append(rating.product_name)
    
    # Add cart items to recommendations
    for cart_item in user_cart_items:
        if cart_item.product_name not in recommended_products:
            recommended_products.append(cart_item.product_name)

    return recommended_products
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

