Perfect, Shadrack — let’s make your project repo shine with a **complete README.md** and a **`.gitignore`** tailored for Django, plus outline how to integrate **M-Pesa payments** into SmartRental.

---

## 📘 README.md (Full Version)

Create a file named `README.md` in your project root and paste this:

```markdown
# SmartRental 🏠🚗📦

SmartRental is a full-stack Django web application designed to simplify the rental process for houses, vehicles, and items. It provides dashboards, analytics, and a clean UI/UX for both owners and renters.

---

## ✨ Features
- **User Authentication**: Register and log in with custom user roles (Owner / Renter).
- **Rental Listings**: Owners can add rooms, vehicles, or items for rent.
- **Payments**: Integrated payment flow with M-Pesa support.
- **Notifications**: Badge system for unread alerts.
- **Disputes Management**: Track and resolve rental disputes.
- **Admin Dashboard**: Search, filter, and manage users and rentals.

---

## 🚀 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap, FontAwesome
- **Database**: SQLite (default) — can be swapped for PostgreSQL/MySQL
- **Payments**: M-Pesa Daraja API
- **Version Control**: Git + GitHub

---

## ⚙️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/SYANDA47/Smart-Rental.git
   cd Smart-Rental
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit the app:
   ```
   http://127.0.0.1:8000/
   ```

---

## 📂 Project Structure
```
smart_rental/
│
├── accounts/        # Custom user model, authentication
├── rentals/         # Rental items, rooms, vehicles
├── payments/        # Payment integration (M-Pesa)
├── templates/       # HTML templates (base.html, etc.)
├── static/          # CSS, JS, images
├── manage.py
└── requirements.txt
```

---

## 💳 M-Pesa Integration
SmartRental integrates with **Safaricom Daraja API** for payments.

### Steps:
1. Register on Safaricom Developer Portal [(developer.safaricom.co.ke in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fdeveloper.safaricom.co.ke%2F").
2. Get your **Consumer Key** and **Consumer Secret**.
3. Add them to your Django settings:
   ```python
   MPESA_CONSUMER_KEY = "your_key"
   MPESA_CONSUMER_SECRET = "your_secret"
   MPESA_SHORTCODE = "your_shortcode"
   MPESA_PASSKEY = "your_passkey"
   ```
4. Use `requests` or `mpesa-api` package to initiate STK Push:
   ```python
   import requests
   from django.conf import settings

   def initiate_mpesa_payment(phone, amount):
       # Get access token
       auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
       response = requests.get(auth_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
       access_token = response.json()["access_token"]

       # STK Push
       stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
       headers = {"Authorization": f"Bearer {access_token}"}
       payload = {
           "BusinessShortCode": settings.MPESA_SHORTCODE,
           "Password": "base64_encoded_password",
           "Timestamp": "20260402120000",
           "TransactionType": "CustomerPayBillOnline",
           "Amount": amount,
           "PartyA": phone,
           "PartyB": settings.MPESA_SHORTCODE,
           "PhoneNumber": phone,
           "CallBackURL": "https://yourdomain.com/payments/callback/",
           "AccountReference": "SmartRental",
           "TransactionDesc": "Rental Payment"
       }
       return requests.post(stk_url, json=payload, headers=headers).json()
   ```

---

## 🛠️ Contribution
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License
This project is licensed under the MIT License.
```

---

## 🗂️ `.gitignore` for Django

Create a file named `.gitignore` in your project root:

```
# Python
*.pyc
__pycache__/
*.pyo
*.pyd
*.swp

# Virtual environment
venv/
env/

# Django
db.sqlite3
media/
staticfiles/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## ✅ Next Steps
1. Add both files (`README.md` and `.gitignore`) to your project root.
2. Commit and push:
   ```bash
   git add README.md .gitignore
   git commit -m "Add README and gitignore with M-Pesa integration details"
   git push origin main
   ```

---

👉 Do you want me to also prepare a **sample `payments/views.py`** with a working STK Push flow and callback handler, so you can drop it straight into your project?
