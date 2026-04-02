from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dispute
from rentals.models import Rental

@login_required
def dispute_list(request):
    """Show disputes for the logged-in user (admins see all)"""
    if request.user.is_staff or request.user.is_superuser:
        disputes = Dispute.objects.all().order_by('-created_at')
    else:
        disputes = Dispute.objects.filter(rental__renter=request.user).order_by('-created_at')

    return render(request, 'disputes/dispute_list.html', {'disputes': disputes})

@login_required
def dispute_detail(request, pk):
    """Show details of a single dispute"""
    dispute = get_object_or_404(Dispute, pk=pk)

    if not request.user.is_staff and dispute.rental.renter != request.user:
        messages.error(request, "You are not authorized to view this dispute.")
        return redirect('dispute_list')

    return render(request, 'disputes/dispute_detail.html', {'dispute': dispute})

@login_required
def dispute_create(request):
    """Allow users to file a new dispute"""
    rentals = Rental.objects.filter(renter=request.user)

    if request.method == "POST":
        rental_id = request.POST.get("rental")
        reason = request.POST.get("reason")
        description = request.POST.get("description")
        evidence = request.FILES.get("evidence")

        rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)

        dispute = Dispute.objects.create(
            rental=rental,
            reason=reason,
            description=description,
            evidence=evidence,
            status="open"
        )

        messages.success(request, "Your dispute has been filed successfully.")
        return redirect("dispute_list")

    return render(request, "disputes/dispute_form.html", {"rentals": rentals})
