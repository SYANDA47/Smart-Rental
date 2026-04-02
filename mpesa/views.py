import requests
import base64
import json
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Generate access token
def generate_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    response.raise_for_status()
    return response.json().get("access_token")

# Initiate STK Push (dynamic phone + amount)
def initiate_stk_push(phone_number, amount):
    access_token = generate_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # ✅ Ensure amount is int (avoid Decimal serialization error)
    amount = int(amount)

    # Encode password
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode("utf-8")
    ).decode("utf-8")

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,  # customer phone number
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,  # define in settings.py
        "AccountReference": "SmartRental",
        "TransactionDesc": "Rental Payment"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    # ✅ Handle possible errors gracefully
    try:
        return response.json()
    except Exception:
        return {"error": "Invalid response from Safaricom", "status_code": response.status_code}

# Handle Callback
@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body.decode("utf-8"))
    print("Callback Data:", json.dumps(data, indent=2))

    checkout_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    result_code = data["Body"]["stkCallback"]["ResultCode"]

    # ✅ Update Payment record if it exists
    from payments.models import Payment
    payment = Payment.objects.filter(transaction_id=checkout_id).first()
    if payment:
        if result_code == 0:
            payment.status = "completed"
            # Extract receipt number if available
            items = data["Body"]["stkCallback"].get("CallbackMetadata", {}).get("Item", [])
            receipt = next((i.get("Value") for i in items if i.get("Name") == "MpesaReceiptNumber"), None)
            if receipt:
                payment.transaction_id = receipt
        else:
            payment.status = "failed"
        payment.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback received successfully"})
