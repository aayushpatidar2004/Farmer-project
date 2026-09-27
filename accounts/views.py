from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from crops.models import Crop
from diseases.models import Disease, Pesticide
from market.models import MarketPrice
from soil.models import SoilData
from .forms import FarmerRegistrationForm, ProfileUpdateForm
from .models import FarmerProfile


def admin_required(view_func):
    """Allow only users who are either admin-role profiles or Django admin users."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        try:
            profile = request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            profile = FarmerProfile.objects.create(user=request.user)

        is_admin_user = request.user.is_superuser or request.user.is_staff
        is_admin_profile = profile.role == 'admin'

        if not (is_admin_profile or is_admin_user):
            messages.error(request, 'Access denied. Only admin-role users can access this dashboard.')
            return HttpResponseForbidden('Access denied. Only admin-role users can access this dashboard.')

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def register_view(request):
    """Farmer registration — role is always set to 'farmer'."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}! Your account has been created.")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FarmerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Login with username and password."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'accounts:dashboard')
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout via POST to protect against CSRF logout attacks."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard_view(request):
    """Farmer dashboard with summary stats and quick actions."""
    user = request.user
    crops = Crop.objects.filter(farmer=user)

    total_crops = crops.count()
    active_crops = crops.filter(status='growing').count()
    planned_crops = crops.filter(status='planned').count()
    harvested_crops = crops.filter(status='harvested').count()
    ready_crops = crops.filter(status='ready').count()
    recent_crops = crops[:5]

    try:
        profile = user.farmer_profile
    except FarmerProfile.DoesNotExist:
        profile = FarmerProfile.objects.create(user=user)

    context = {
        'profile': profile,
        'total_crops': total_crops,
        'active_crops': active_crops,
        'planned_crops': planned_crops,
        'harvested_crops': harvested_crops,
        'ready_crops': ready_crops,
        'recent_crops': recent_crops,
    }
    return render(request, 'farmer/dashboard.html', context)


@login_required
@admin_required
def admin_dashboard_view(request):
    """Protected admin dashboard for users with role='admin'."""
    try:
        profile = request.user.farmer_profile
    except FarmerProfile.DoesNotExist:
        profile = FarmerProfile.objects.create(user=request.user)

    context = {
        'profile': profile,
        'farmer_count': User.objects.count(),
        'crop_count': Crop.objects.count(),
        'disease_count': Disease.objects.count(),
        'pesticide_count': Pesticide.objects.count(),
        'market_price_count': MarketPrice.objects.count(),
        'soil_record_count': SoilData.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def profile_view(request):
    """View farmer profile."""
    try:
        profile = request.user.farmer_profile
    except FarmerProfile.DoesNotExist:
        profile = FarmerProfile.objects.create(user=request.user)

    return render(request, 'farmer/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    """Edit profile form."""
    try:
        profile = request.user.farmer_profile
    except FarmerProfile.DoesNotExist:
        profile = FarmerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.user, request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(request.user, instance=profile)

    return render(request, 'farmer/edit_profile.html', {'form': form, 'profile': profile})
