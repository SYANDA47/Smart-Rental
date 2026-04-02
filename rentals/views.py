from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta

from .models import RentalItem, Rental
from .forms import RentalItemForm, RentalForm

# --- ITEM MANAGEMENT ---

def item_list(request):
    """Show all rental items (guest or logged-in user)."""
    items = RentalItem.objects.all().order_by("-created_at")
    return render(request, "rentals/item_list.html", {"items": items})


@login_required
def add_item(request):
    """Allow renters to add their own items for renting."""
    if request.method == "POST":
        form = RentalItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user   # ✅ tie item to logged-in renter
            # ✅ persist checkbox value into show_owner_name
            item.show_owner_name = form.cleaned_data.get("include_owner_name", False)
            item.save()
            messages.success(request, f"Item '{item.title}' has been listed for rent!")
            return redirect("item_list")
    else:
        form = RentalItemForm()
    return render(request, "rentals/add_item.html", {"form": form})


# --- RENTAL / BOOKING MANAGEMENT ---

@login_required
def rental_list(request):
    """Show rentals for the logged-in renter."""
    rentals = Rental.objects.filter(renter=request.user).order_by('-created_at')
    return render(request, "rentals/rental_list.html", {"rentals": rentals})


@login_required
def rental_detail(request, rental_id):
    """View details of a specific rental."""
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)
    return render(request, "rentals/rental_detail.html", {"rental": rental})


@login_required
def rental_create(request, item_id):
    """Normal rental flow using the RentalForm for dates."""
    item = get_object_or_404(RentalItem, pk=item_id)

    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.item = item
            rental.renter = request.user
            rental.save()  # ✅ triggers total_price calculation

            # ✅ Booking summary message
            messages.success(
                request,
                f"You reserved {item.title} for {rental.duration} days. "
                f"Daily Rate: Ksh {item.price_per_day}, Total: Ksh {rental.total_price}"
            )
            return redirect("checkout", rental_id=rental.id)
    else:
        form = RentalForm()

    return render(request, "rentals/rental_form.html", {"form": form, "item": item})


@login_required
def quick_rent(request, item_id):
    """Instant 1-day rental: skips the date form."""
    item = get_object_or_404(RentalItem, pk=item_id)

    start_date = date.today()
    end_date = start_date + timedelta(days=1)

    rental = Rental(
        renter=request.user,
        item=item,
        start_date=start_date,
        end_date=end_date,
        status="pending"
    )
    rental.save()  # ✅ triggers total_price calculation

    # ✅ Booking summary message
    messages.success(
        request,
        f"Quick rental started for {item.title} (1 day). "
        f"Daily Rate: Ksh {item.price_per_day}, Total: Ksh {rental.total_price}"
    )
    return redirect("checkout", rental_id=rental.id)


@login_required
def rental_cancel(request, rental_id):
    """Cancel a rental by deleting it completely."""
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)

    if rental.status in ["pending", "active"]:
        rental.delete()  # ✅ remove rental from DB
        messages.success(request, f"Rental for {rental.item.title} has been removed.")
    else:
        messages.warning(request, "This rental cannot be cancelled or is already completed.")

    return redirect("rental_list")
