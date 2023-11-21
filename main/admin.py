from django.contrib import admin
from .models import Transaction, Card, Account,Conseiller

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'transaction_type', 'amount', 'date', 'to', 'status')
    list_filter = ('user', 'transaction_type', 'status')
    search_fields = ('user__username', 'to')
    list_editable = ('status',)  # Allow editing 'status' directly in the list view
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'cvv', 'expiration')
    list_filter = ('user','card_number')
    search_fields = ('user__username','card_number')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'balance')

@admin.register(Conseiller)
class ConseillerAdmin(admin.ModelAdmin):
    list_display = ('code','nom','email','whatsapp')
    search_fields = ('code', 'nom', 'email', 'whatsapp')


