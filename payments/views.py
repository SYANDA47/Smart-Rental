from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
import json

from .models import Payment
from rentals.models import Rental
# ✅ Import the correct function from mpesa app
from mpesa.views import initiate_stk_push


@login_required
def payment_list(request):
    """Show only payments belonging to the logged-in user, with search support"""
    query = request.GET.get("q")
    payments = Payment.objects.filter(renter=request.user).order_by('-date')

    if query:
        payments = payments.filter(
            Q(item__title__icontains=query) |
            Q(method__icontains=query) |
            Q(status__icontains=query)
        )

    return render(request, "payments/payment_list.html", {
        "payments": payments,
        "query": query,
    })


@login_required
def payment_detail(request, payment_id):
    """View details of a single payment"""
    payment = get_object_or_404(Payment, pk=payment_id, renter=request.user)
    return render(request, "payments/payment_detail.html", {"payment": payment})


@login_required
def checkout(request, rental_id):
    """Step 1: Choose payment method"""
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)

    methods = [
        ("paypal", "PayPal"),
        ("card", "Bank Card"),
        ("mpesa", "M-Pesa"),
    ]

    if request.method == "POST":
        method = request.POST.get("method")
        return redirect("payment_method_step", rental_id=rental.id, method=method)

    return render(request, "payments/checkout.html", {"rental": rental, "methods": methods})


@login_required
def payment_method_step(request, rental_id, method):
    """Step 2: Show method-specific form and process payment"""
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)

    if request.method == "POST":
        # ✅ Ensure rental.item exists
        if not rental.item:
            messages.error(request, "This rental has no linked item.")
            return redirect("checkout", rental_id=rental.id)

        if method == "paypal":
            paypal_email = request.POST.get("paypal_email")
            Payment.objects.create(
                rental=rental,
                renter=request.user,
                item=rental.item,
                amount=rental.total_price,
                method="paypal",
                status="completed"
            )

        elif method == "card":
            card_number = request.POST.get("card_number")
            expiry = request.POST.get("expiry")
            cvv = request.POST.get("cvv")
            Payment.objects.create(
                rental=rental,
                renter=request.user,
                item=rental.item,
                amount=rental.total_price,
                method="card",
                status="completed"
            )

        elif method == "mpesa":
            phone_number = request.POST.get("phone_number")
            response = initiate_stk_push(phone_number, int(rental.total_price))
            checkout_id = response.get("CheckoutRequestID")

            Payment.objects.create(
                rental=rental,
                renter=request.user,
                item=rental.item,
                amount=rental.total_price,
                method="mpesa",
                status="pending",
                transaction_id=checkout_id
            )

        else:
            messages.error(request, "Unsupported payment method.")
            return redirect("checkout", rental_id=rental.id)

        rental.status = "active"
        rental.save()

        messages.success(request, f"Payment initiated for {rental.item.title}.")
        return redirect("payment_success", rental_id=rental.id)

    if method in ["paypal", "card", "mpesa"]:
        template_name = f"payments/{method}_form.html"
        return render(request, template_name, {"rental": rental})
    else:
        return redirect("payment_success", rental_id=rental.id)


@login_required
def payment_success(request, rental_id):
    """Step 3: Show success confirmation after payment"""
    rental = get_object_or_404(Rental, pk=rental_id, renter=request.user)
    payments = Payment.objects.filter(rental=rental, renter=request.user)

    if not payments.exists():
        messages.error(request, "No payment record found for this rental.")
        return redirect("payment_list")

    return render(request, "payments/success.html", {
        "rental": rental,
        "payments": payments,
        "latest_payment": payments.first()
    })


@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa STK Push callback from Safaricom"""
    data = json.loads(request.body.decode("utf-8"))
    checkout_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    result_code = data["Body"]["stkCallback"]["ResultCode"]

    payment = Payment.objects.filter(transaction_id=checkout_id).first()
    if payment:
        if result_code == 0:
            payment.status = "completed"
        else:
            payment.status = "failed"
        payment.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback received successfully"})
