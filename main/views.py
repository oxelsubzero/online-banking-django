from django.shortcuts import render,redirect
from django.views import View
from .models import Rib,Account,Transaction, Card, Beneficiaire,Conseiller, Notification
from django.http import JsonResponse
from .iban import generate_card
import random
from django.core.mail import send_mail
from decimal import Decimal
from . import county
from django.core.mail import EmailMessage


def notification(request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return notifications


class IndexView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        accounts = Account.objects.filter(user=request.user)
        
        notif = notification(request)
        context = {
            'accounts' : accounts,
           
            'user':request.user,
            'notifications':notif
        }
        return render(request,'main/index.html',context)

class CarteView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        user_cards = Card.objects.filter(user=request.user)
    
        context = {
            'user_cards': user_cards
        }

        return render(request, 'main/carte.html', context)
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        montant = request.POST.get("montant")
        card_nb = request.POST.get("card_nb") 

        if montant and card_nb:
            try:
                card = Card.objects.get(user=request.user,card_number=card_nb)
                account = Account.objects.get(user=request.user,account_type="courant")
                if account.balance >= int(montant) :
                    account.balance -= int(montant)
                    account.save()
                    card.solde += int(montant)
                    card.save()
            except (Card.DoesNotExist, Account.DoesNotExist):
                # Handle the case when the card or account doesn't exist
                # or doesn't belong to the current user
                pass  # You may want to add appropriate error handling here

            
        else :
            card = generate_card()
            Card.objects.create(
                user=request.user,
                card_number = card[0],
                cvv = card[1],
                expiration = "11 / 26",
            )

        return redirect("carte")

    
class RibView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        rib = Rib.objects.get(user=user)
        context = {
            'user':user,
            'rib': rib
        }
        return render(request,"main/rib.html",context)
    
class AutreView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        conseiller =Conseiller.objects.get(code=request.user.consiller_id)
        return render(request,"main/autre.html",{"conseiller":conseiller})
    
class TransfertView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        beneficiaire_list = Beneficiaire.objects.filter(user=request.user)
        account_list = Account.objects.filter(user=request.user)
        context = {
            "beneficiaire_list":beneficiaire_list,
            'account_list': account_list
        }
        return render(request,"main/transfert.html",context)
    
class BeneficiaireRegisterView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        intitule = request.POST.get('intitule')
        nom = request.POST.get('nom')
        bic = request.POST.get('bic')
        iban = request.POST.get('iban')

        if intitule and nom and bic and iban:
            beneficiaire = Beneficiaire(user=request.user, intitulé=intitule, nom=nom, bic=bic, iban=iban)
            beneficiaire.save()

            # You can customize the response message
            response_data = {'message': 'Bénéficiaire ajouté !'}
            return JsonResponse(response_data)

        response_data = {'message': 'Données invalides'}
        return JsonResponse(response_data, status=400)

class VirementInst(View) :
    def post(self,request) :
        if not request.user.is_authenticated:
            return redirect('login')
        # Get form data
        beneficiary_id = request.POST.get('beneficiaire')
        amount = float(request.POST.get('montant'))

        # Get the selected beneficiary
        beneficiary = Beneficiaire.objects.get(id=beneficiary_id)

        # Get the user's and beneficiary's accounts
        user_account = Account.objects.get(user=request.user,account_type="courant")

        try:
            if user_account.balance >= amount:
                verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
                request.session['verification_code_externe'] = verification_code
                request.session['beneficiaire'] = beneficiary.iban
                request.session['amount'] = amount
                email_body = f"Bonjour {request.user.prenoms}, veuillez entrer ce code pour valider votre transaction. Code : {verification_code}"
                email = EmailMessage(
                    "Code de confirmation",
                    email_body,
                    'appleshopnow@outlook.com',
                    [request.user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                return redirect('verification_code2')
            else:
                # Handle insufficient balance
                return render(request, "main/error.html", {"error": "Votre solde est insuffisant"})
            
        except ValueError:
            # Handle invalid montant (not a valid float)
            return render(request, "main/error.html", {"error": "Montant invalide"})



class VirementInterneView(View): 
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        source_account_type = request.POST.get('source')
        beneficiary_account_type = request.POST.get('beneficiaire')
        montant = request.POST.get('montant')

        # Validate the form data (you can add more validation as needed)
        if not source_account_type or not beneficiary_account_type or not montant:
            return render(request, 'main/error.html', {'error': 'Invalid form data'})

        # Fetch the selected accounts
        source_account = Account.objects.get(user=request.user, account_type=source_account_type)
        beneficiary_account = Account.objects.get(user=request.user, account_type=beneficiary_account_type)

        
        try:
            montant = float(montant)
            if source_account.balance >= montant:
                verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
                request.session['verification_code'] = verification_code
                request.session['source_account_type'] = source_account_type
                request.session['beneficiary_account_type'] = beneficiary_account_type
                request.session['montant'] = montant
                email_body = f"Bonjour {request.user.prenoms}, veuillez entrer ce code pour valider votre transaction. Code : {verification_code}"
                email = EmailMessage(
                    "Code de confirmation",
                    email_body,
                    'appleshopnow@outlook.com',
                    [request.user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)


                return redirect('verification_code')
            else:
                # Handle insufficient balance
                return render(request, "main/error.html", {"error": "Votre solde est insuffisant"})
        except ValueError:
            # Handle invalid montant (not a valid float)
            return render(request, "main/error.html", {"error": "Montant invalide"})
        

class ValidationCode2View(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, "main/verification_code2.html")
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        digit1 = request.POST.get("digit1")
        digit2 = request.POST.get("digit2")
        digit3 = request.POST.get("digit3")
        digit4 = request.POST.get("digit4")
        digit5 = request.POST.get("digit5")
        digit6 = request.POST.get("digit6")

        # Concatenate digits to form the verification code
        code = f"{digit1}{digit2}{digit3}{digit4}{digit5}{digit6}"
        if code:
            if code == request.session.get("verification_code_externe"):
                    user_account = Account.objects.get(user=request.user,account_type="courant")
                    user_account.balance -= Decimal(request.session.get("amount"))
                    Transaction.objects.create(
                    user=request.user,
                    account_type=user_account,
                    transaction_type='Virement à ',
                    amount=request.session.get("amount"),
                    to=request.session.get('beneficiaire'),
                    status='en cours'  # or another appropriate status

                    )
                    return render(request,"main/contacter_conseiller.html",{"error": "L’approbation de votre conseiller bancaire est nécessaire pour effectuer ce transfert."})

class ValidationCodeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, "main/verification_code.html")

    def post(self, request):
        # Retrieve individual digits from the form
        if not request.user.is_authenticated:
            return redirect('login')
        digit1 = request.POST.get("digit1")
        digit2 = request.POST.get("digit2")
        digit3 = request.POST.get("digit3")
        digit4 = request.POST.get("digit4")
        digit5 = request.POST.get("digit5")
        digit6 = request.POST.get("digit6")

        # Concatenate digits to form the verification code
        code = f"{digit1}{digit2}{digit3}{digit4}{digit5}{digit6}"
        if code:
            if code == request.session.get("verification_code"):
                source_account_type = request.session.get("source_account_type")
                beneficiary_account_type = request.session.get("beneficiary_account_type")
                montant = request.session.get("montant")

                # Fetch the corresponding accounts using the stored account types
                source_account = Account.objects.get(user=request.user, account_type=source_account_type)
                beneficiary_account = Account.objects.get(user=request.user, account_type=beneficiary_account_type)
                montant = Decimal(str(montant))

                if source_account_type == "credit":
                    Transaction.objects.create(
                        user=request.user,
                        account_type=source_account,
                        transaction_type='Transfert vers ',
                        amount=montant,
                        to=beneficiary_account.account_type,
                        status='en cours'
                    )
                    del request.session['verification_code']
                    del request.session['source_account_type']
                    del request.session['beneficiary_account_type']
                    del request.session['montant']
                    return render(request,"main/contacter_conseiller.html",{"error": "Votre transaction n’a pas aboutir veuillez contacter votre conseiller client pour résoudre le problème"})
                    
                else :
                    source_account.balance -= montant
                    beneficiary_account.balance += montant
                    source_account.save()
                    beneficiary_account.save()

                    Transaction.objects.create(
                        user=request.user,
                        account_type=source_account,
                        transaction_type='Transert vers ',
                        amount=montant,
                        to=beneficiary_account.account_type,
                        status='confirmé'
                    )

                    # Clear the session variables
                    del request.session['verification_code']
                    del request.session['source_account_type']
                    del request.session['beneficiary_account_type']
                    del request.session['montant']

                    return redirect("sucess")
            else:
                return render(request, "main/error.html", {"error": "Code invalide"})
                
        else:
            return render(request, "main/error.html", {"error": "Vous n'avez pas entrez de code"})
        
class SettingsView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        country_name = county.id_to_country(request.user.country)
        return render(request,"main/profil.html",{'user':request.user,'pays':country_name})
        
    
class SucessView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request,'main/success_page.html')
    


class Account_details(View):
    def get(self, request, account_type):
        if not request.user.is_authenticated:
            return redirect('login')
        solde = Account.objects.get(user=request.user, account_type=account_type).balance
        account_list = Account.objects.filter(user=request.user).exclude(account_type=account_type)
        transactions = Transaction.objects.filter(user=request.user,account_type=Account.objects.get(user=request.user, account_type=account_type))
        print(transactions)
        context = {
            "account_type":account_type,
            'account_list': account_list,
            'transactions' : transactions,
            'solde':solde
        }


        return render(request, 'main/account_details.html',context)
    

