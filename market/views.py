from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q

from .models import MarketPrice
from .forms import MarketPriceForm


def is_admin(user):
    """Check if the user has admin role."""
    try:
        profile = getattr(user, 'farmer_profile', None)
    except Exception:
        profile = None
    return bool(user.is_staff or (profile is not None and profile.role == 'admin'))


@login_required
def market_list_view(request):
    """Market prices with search, crop filter, and sort."""
    prices = MarketPrice.objects.all()

    search_query = request.GET.get('q', '').strip()
    unit_filter = request.GET.get('unit', '').strip()
    sort_by = request.GET.get('sort', '-date')

    if search_query:
        prices = prices.filter(
            Q(crop_name__icontains=search_query) |
            Q(market_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if unit_filter:
        prices = prices.filter(unit=unit_filter)

    valid_sorts = ['crop_name', '-crop_name', 'price', '-price', 'date', '-date']
    if sort_by in valid_sorts:
        prices = prices.order_by(sort_by)

    context = {
        'prices': prices,
        'search_query': search_query,
        'unit_filter': unit_filter,
        'sort_by': sort_by,
        'unit_choices': MarketPrice.UNIT_CHOICES,
    }
    return render(request, 'market/list.html', context)


@login_required
@user_passes_test(is_admin)
def market_add_view(request):
    """Admin-only: add a new market price entry."""
    if request.method == 'POST':
        form = MarketPriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Market price entry added successfully.")
            return redirect('market:list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MarketPriceForm()

    return render(request, 'market/form.html', {'form': form, 'title': 'Add Market Price'})


@login_required
@user_passes_test(is_admin)
def market_edit_view(request, pk):
    """Admin-only: edit a market price entry."""
    price = get_object_or_404(MarketPrice, pk=pk)

    if request.method == 'POST':
        form = MarketPriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            messages.success(request, "Market price updated successfully.")
            return redirect('market:list')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = MarketPriceForm(instance=price)

    return render(request, 'market/form.html', {'form': form, 'price': price, 'title': 'Edit Market Price'})


@login_required
@user_passes_test(is_admin)
def market_delete_view(request, pk):
    """Admin-only: delete a market price entry (POST only)."""
    price = get_object_or_404(MarketPrice, pk=pk)

    if request.method == 'POST':
        price.delete()
        messages.success(request, "Market price entry deleted.")
        return redirect('market:list')

    return render(request, 'market/confirm_delete.html', {'price': price})
