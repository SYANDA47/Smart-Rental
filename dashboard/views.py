from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from rentals.models import Rental
from payments.models import Payment
from disputes.models import Dispute


@login_required
def renter_dashboard(request):
    """Dashboard for renters: rentals, payments, stats, and monthly spending trend"""
    profile = request.user  # CustomUser instance

    # Rentals and payments for this renter
    rentals = Rental.objects.filter(renter=request.user).order_by('-start_date')
    payments = Payment.objects.filter(renter=request.user).order_by('-date')

    # Summary stats
    total_spent = payments.aggregate(total=Sum("amount"))["total"] or 0
    active_rentals = rentals.filter(status="active").count()
    pending_payments = payments.filter(status="pending").count()

    # Monthly spending trend
    monthly_data = (
        payments.annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(total=Sum("amount"))
                .order_by("month")
    )

    context = {
        "profile": profile,
        "rentals": rentals,
        "payments": payments,
        "total_spent": total_spent,
        "active_rentals": active_rentals,
        "pending_payments": pending_payments,
        "monthly_data": monthly_data,
        "item_type": profile.item_type,   # ✅ show what renter offers
    }
    return render(request, "dashboard/renter.html", context)


@login_required
def owner_dashboard(request):
    """Dashboard for owners: revenue, top items, disputes, and monthly revenue trend"""
    rentals = Rental.objects.all()
    payments = Payment.objects.all()

    # Revenue summary
    revenue = payments.filter(status="completed").aggregate(total=Sum("amount"))["total"] or 0

    # Top rented items (use title instead of name)
    top_items = (
        rentals.values("item__title")
               .annotate(total=Count("id"))
               .order_by("-total")[:5]
    )

    # Open disputes count
    disputes_count = Dispute.objects.filter(status="open").count()

    # Monthly revenue trend
    monthly_revenue = (
        payments.filter(status="completed")
                .annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(total=Sum("amount"))
                .order_by("month")
    )

    context = {
        "revenue": revenue,
        "top_items": top_items,
        "disputes": disputes_count,
        "monthly_revenue": monthly_revenue,
    }
    return render(request, "dashboard/owner.html", context)
