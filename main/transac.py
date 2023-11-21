import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_bank.settings")
django.setup()


# Import necessary modules and models
from django.contrib.auth import get_user_model
from main.models import Account, Transaction
import random
from decimal import Decimal
from django.utils import timezone

# Get or create a user
user, created = get_user_model().objects.get_or_create(username="toto@gmail.com")

# Get an account for the user (assuming you have an account for the user)
account = Account.objects.get(user=user, account_type="courant")

# Generate random transactions
transaction_types = ["Deposit", "Withdrawal", "Transfer"]
statuses = ["confirmé", "en cours", "rejeté"]
for _ in range(10):  # Generate 10 random transactions
    transaction_type = random.choice(transaction_types)
    amount = Decimal(random.uniform(10, 1000)).quantize(Decimal("0.01"))
    to = "Beneficiary's IBAN"
    status = random.choice(statuses)
    date = timezone.now() - timezone.timedelta(days=random.randint(1, 365))  # Random date within the last year

    # Create the transaction
    Transaction.objects.create(user=user,account_type=account,transaction_type=transaction_type,amount=amount,to=to,status=status,date=date)
