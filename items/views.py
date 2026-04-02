from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Item, Wishlist, Review
from rentals.models import Rental   # ✅ import Rental from rentals app


def item_list(request):
    """Show available items with search + wishlist support"""
    query = request.GET.get("q")
    items = Item.objects.filter(is_available=True).order_by('-id')

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('item_id', flat=True)

    return render(request, 'items/item_list.html', {
        'items': items,
        'query': query,
        'wishlist_items': wishlist_items,
    })


def item_detail(request, pk):
    """View details of a single available item + reviews"""
    item = get_object_or_404(Item, pk=pk, is_available=True)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, item=item).exists()

    reviews = item.reviews.select_related('user').order_by('-created_at')

    return render(request, 'items/item_detail.html', {
        'item': item,
        'in_wishlist': in_wishlist,
        'reviews': reviews,
    })


@login_required
def add_to_wishlist(request, item_id):
    """Add an item to the user's wishlist"""
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.get_or_create(user=request.user, item=item)
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, item_id):
    """Remove an item from the user's wishlist"""
    item = get_object_or_404(Item, id=item_id)
    Wishlist.objects.filter(user=request.user, item=item).delete()
    return redirect('wishlist')


@login_required
def wishlist(request):
    """Show all items in the user's wishlist"""
    favorites = Wishlist.objects.filter(user=request.user).select_related('item')
    return render(request, 'items/wishlist.html', {'favorites': favorites})


@login_required
def add_review(request, pk):
    """Add or update a star-only review for an item"""
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        Review.objects.update_or_create(
            item=item,
            user=request.user,
            defaults={"rating": rating}
        )
    return redirect("item_detail", pk=item.pk)


# --- Rentals ---
@login_required
def extend_rental(request, rental_id):
    """Extend a rental by 1 day"""
    rental = get_object_or_404(Rental, id=rental_id, renter=request.user, status="active")
    rental.extend(days=1)  # uses model method
    return redirect("item_detail", pk=rental.item.pk)


@login_required
def cancel_rental(request, rental_id):
    """Cancel a rental"""
    rental = get_object_or_404(Rental, id=rental_id, renter=request.user, status="active")
    rental.cancel()  # uses model method
    return redirect("item_detail", pk=rental.item.pk)
