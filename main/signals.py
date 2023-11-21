from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, Transaction

@receiver(post_save, sender=Account)
def create_transaction(sender, instance, created, **kwargs):
    if created:  # Vous pouvez ajuster cette condition selon vos besoins spécifiques
        # Créez une transaction correspondante lorsqu'un nouveau compte est créé
        Transaction.objects.create(
            user=instance.user,
            account_type=instance,
            transaction_type='Crédit',  # Ou un autre type de transaction selon vos besoins
            amount=instance.balance,   # Montant crédité sur le compte
            to='Compte crédité',
            status='confirmé'
        )
