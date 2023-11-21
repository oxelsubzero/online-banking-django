from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account_type} - {self.user}"

    def save(self, *args, **kwargs):
        original_balance = self.balance
        super().save(*args, **kwargs)

        if self.balance != original_balance:
            transaction_type = "Credit" if self.balance > original_balance else "Debit"
            amount = abs(self.balance - original_balance)
            Transaction.objects.create(
                user=self.user,
                account_type=self.account_type,
                transaction_type=transaction_type,
                amount=amount,
                to="Account",
                status="Success"
            )



class Rib(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    code_bank = models.CharField(max_length=10)
    code_guichet = models.CharField(max_length=10)
    account_number = models.CharField(max_length=20)
    iban = models.CharField(max_length=34)
    bic_swift = models.CharField(max_length=11)


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    account_type = models.ForeignKey(Account, on_delete=models.CASCADE) 
    transaction_type = models.CharField(max_length=20)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    to = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} on {self.date}"
    
    

class Card(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    cvv = models.CharField(max_length=4)
    expiration = models.CharField(max_length=8)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Beneficiaire(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    intitulé = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    bic = models.CharField(max_length=20)
    iban = models.CharField(max_length=20)


class Conseiller(models.Model):
    code = models.CharField(max_length=10,unique=True)
    nom = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    whatsapp = models.CharField(max_length=40)


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

