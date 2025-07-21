from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control

from .forms import UserLoginForm, UserRegistrationForm
from .models import Recipe, Feedback, UserRegistration
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Home Page
def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})

# User Login
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                # Authenticate against the UserRegistration model
                user_registration = UserRegistration.objects.get(email=email, password=password)

                # Create a temporary Django user for authentication
                user, created = User.objects.get_or_create(username=user_registration.email)

                # Manually authenticate and log in the user
                login(request, user)

                request.session['user_id'] = user_registration.id
                return redirect('user_dashboard')

            except UserRegistration.DoesNotExist:
                messages.error(request, "Invalid email or password!")
    else:
        form = UserLoginForm()

    return render(request, 'user_login.html', {'form': form})
# User Dashboard
@login_required(login_url='user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    search_query = request.GET.get('search', '')

    if search_query:
        recipes = Recipe.objects.filter(
            Q(recipe_name__icontains=search_query) |  # Search by Name
            Q(category__icontains=search_query) |  # Search by Category
            Q(ingredients__icontains=search_query) |  # Search by Ingredients
            Q(description__icontains=search_query)  # Search by Description
        )
    else:
        recipes = Recipe.objects.all()

    return render(request, 'user_dashboard.html', {'recipes': recipes})

@login_required(login_url='user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            next_url = request.POST.get('next') or 'admin_dashboard'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'admin_login.html')




# Admin Dashboard - Manage Recipes
@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to access this page.")
        return redirect('admin_login')
    recipes = Recipe.objects.all()
    return render(request, 'admin_dashboard.html', {'recipes': recipes})


# Add Recipe
@login_required(login_url='admin_login')
def add_recipe(request):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to access this page.")
        return redirect('admin_login')
    if request.method == "POST":
        recipe_name = request.POST['recipe_name']
        ingredients = request.POST['ingredients']
        description = request.POST['description']
        category = request.POST['category']
        image = request.FILES.get('image')
        ratings = request.POST.get('ratings', 0)
        how=request.POST.get('how',0)

        Recipe.objects.create(
            recipe_name=recipe_name,
            ingredients=ingredients,
            description=description,
            category=category,
            image=image,
            ratings=ratings,
            how_to_cook=how,
        )
        return redirect('admin_dashboard')
    return render(request, 'add_recipe.html')

# Update Recipe
@login_required(login_url='admin_login')
def update_recipe(request, recipe_id):
    if not request.user.is_superuser:
        messages.error(request, "You must be an admin to access this page.")
        return redirect('admin_login')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        recipe.recipe_name = request.POST['recipe_name']
        recipe.ingredients = request.POST['ingredients']
        recipe.description = request.POST['description']
        recipe.category = request.POST['category']
        recipe.image = request.FILES.get('image', recipe.image)
        recipe.ratings = request.POST.get('ratings', recipe.ratings)
        recipe.save()
        return redirect('admin_dashboard')
    return render(request, 'update_recipe.html', {'recipe': recipe})

# Delete Recipe
@login_required(login_url='admin_login')
def delete_recipe(request, recipe_id):
    if not request.user.is_superuser:
        return redirect('admin_login')
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.delete()
    return redirect('admin_dashboard')

def admin_logout(request):
    logout(request)  # Clears the session
    request.session.flush()  # Ensures session data is completely cleared
    return redirect('admin_login')

# Like Recipe
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.ratings += 1  # Increase rating
    recipe.save()
    return redirect('home')

# Logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('home')
