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
from django.db.models import Count





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

        if user.is_authenticated:
            # Get recommended products for the user
            recommended_products = get_recommended_products(user)

            # Format the recommended products for the JSON response
            products_data = [{'name': product.product_name, 'rating': product.rating} for product in recommended_products]

            response_data = {
                'response': 'Recommended Products:',
                'products': products_data
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'User not authenticated.'}, status=401)  # Unauthorized
    return JsonResponse({'error': 'Invalid request'}, status=400) 

def get_recommended_products(user):
    # Get all users who have rated at least one product
    rated_users = Rating.objects.exclude(user=user).values('user').annotate(num_ratings=Count('id'))
    
    # Calculate user-user similarity based on ratings
    similarity_scores = {}
    user_ratings = Rating.objects.filter(user=user)  # Fetch user's ratings
    for rated_user in rated_users:
        other_user = rated_user['user']
        other_user_ratings = Rating.objects.filter(user=other_user)
        
        # Calculate similarity score using a simple metric like Jaccard similarity
        common_ratings = set(user_ratings.values_list('product_name', flat=True))
        other_common_ratings = set(other_user_ratings.values_list('product_name', flat=True))
        
        similarity = len(common_ratings.intersection(other_common_ratings)) / len(common_ratings.union(other_common_ratings))
        similarity_scores[other_user] = similarity
    
    # Sort users by similarity score in descending order
    similar_users = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Get top similar users and their rated products
    top_similar_users = [user_id for user_id, _ in similar_users[:3]]  # Adjust the number of similar users as needed
    recommended_products = Rating.objects.filter(user__in=top_similar_users).order_by('-rating')[:5]  # Get top rated products from similar users
    
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

