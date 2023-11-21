from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import auth, messages
from .models import UserDocument
from django.contrib.auth.hashers import make_password
from main.models import Account,   Rib
from main.iban import generate_random_iban, generate_random_account
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import  account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str


#registration
class Emailview(View) :
    
    def get(self,request) : 
        return render(request, "auth/email.html")
    def post(self,request) :
        User = get_user_model()
        try :
            email = request.POST['email']
            if User.objects.filter(email=str(email)).exists():
                return (request,"")
            else :
                request.session['email'] = email
                return redirect('userInfo')
        except : 
            return redirect('userInfo')
        
class UserInformationView(View) :

    def get(self,request):
        return render(request,'auth/UserInformation.html')
    
    def post(self,request):
        name = request.POST.get('name')
        prenoms = request.POST.get('prenoms')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        
        request.session['name'] = name
        request.session['prenoms'] = prenoms
        request.session['age'] = age
        request.session['phone'] = phone
        request.session['country'] = country

        return redirect('birth')
    
class BirthView(View):
    def get(self,request):
        return render(request,"auth/birth.html")
    def post(self,request):
        return redirect('adresse')

class AdresseView(View) :
    def get(self,request):
        return render(request,'auth/adresse.html')
    def post(self,request):
        logement = request.POST.get('logement')
        address = request.POST.get('address')

        request.session['logement'] = logement
        request.session['address'] = address

        return redirect('financial')
    
class FinancialView(View):
    def get(self,request):
        return render(request,'auth/financial.html')
    def post(self,request):
        fiscalResident = request.POST.get('res')
        type = request.POST.get('prin')

        request.session['fiscalResident'] = fiscalResident
        request.session['type'] = type

        return redirect('usage')
    
class UsageView(View) : 
    def get(self,request):
        return render(request,'auth/usage.html')
    def post(self,request):
        return redirect('profession')
    
class ProfesionView(View) : 
    def get(self,request):
        return render(request,'auth/profession.html')
    def post(self,request):
        profession = request.POST.get('profession')
        request.session[profession] = profession
        return redirect('revenu')
    
class RevenuView(View) : 
    def get(self,request):
        return render(request,'auth/revenu.html')
    def post(self,request):
        revenu = request.POST.get('revenu')
        request.session['revenu'] = revenu
        return redirect('password')
    



class CreationView(View):
    def get(self, request):
        return render(request, 'auth/password.html')

    def post(self, request):
        User = get_user_model()
        password = request.POST.get('password')
        email = request.session.get('email')
        name = request.session.get('name')
        prenoms = request.session.get('prenoms')
        age_str = request.session.get('age')
        age = int(age_str) if age_str else 0
        phone = request.session.get('phone')
        country = request.session.get('country')
        logement = request.session.get('logement')
        address = request.session.get('address')
        fiscalResident = request.session.get('fiscalResident')
        type = request.session.get('type')
        profession = request.session.get('profession')
        revenu = request.session.get('revenu')

        new_user = User.objects.create_user(username=email, email=email) #create a new user
        new_user.set_password(password)

        new_user.name = name
        new_user.prenoms = prenoms
        new_user.age = age
        new_user.phone = phone
        new_user.country = country
        new_user.logement = logement
        new_user.address = address
        new_user.fiscalResident = fiscalResident
        new_user.type = type
        new_user.profession = profession
        new_user.revenu = revenu
        new_user.is_active = True  # Set 'active' to True
            
        new_user.save()

        user = authenticate(request, username=email, password=password)
 
        login(request, user)
        new_user = user

                # Create the three types of accounts for the user
        Account.objects.create(
            account_type="courant",
            user=new_user,
            balance=0.0
        )
        Account.objects.create(
            account_type="credit",
            user=new_user,
            balance=0.0
        )
        Account.objects.create(
            user=new_user,
            account_type="epargne",
            balance=0.0
        )
        iban = generate_random_iban(country)
        Rib.objects.create(
                user=user,
                code_bank = "28732",
                code_guichet = "0040",
                account_number= generate_random_account(),
                iban=iban,
                bic_swift='CIBAFR2L'
            )

        user = authenticate(request, username=email, password=password)
 
        login(request, user)
        return redirect('verification')




    
class VerificationView(View):
    def get(self,request):
        return render(request,'auth/verification.html')
    def post(self,request):
        return redirect("upload")


class UploadView(View):
    def get(self,request):
        return render(request,"auth/upload.html")
    
    def post(self, request):
        document_type = request.POST.get('document_type')
        try :
            user_document = UserDocument.objects.get(user=request.user)
            if user_document :
                return redirect("selfie")
        except :
            if document_type == 'national_id_card':
                recto_image = request.FILES.get('national_id_card_recto')
  

                if recto_image:
                    user_document_recto = UserDocument(user=request.user, document_type='national_id_card_recto', image=recto_image)
                    user_document_recto.save()

            elif document_type == 'passport':
                passport_image = request.FILES.get('passport')

                if passport_image:
                    user_document_passport = UserDocument(user=request.user, document_type='passport', image=passport_image)
                    user_document_passport.save()

            return redirect("selfie")


class SelfieView(View):
    def get(self, request):
        return render(request, "auth/selfie.html")

    def post(self, request):
        user = request.user

        # Check if a row already exists for the user
        try:
            user_document = UserDocument.objects.get(user=user)
        except UserDocument.DoesNotExist:
            # Redirect the user to the document upload page if no row is found
            return redirect("upload")

        # Check if a selfie image is provided and update it
        selfie_image = request.FILES.get('passport')
        if selfie_image:
            user_document.selfie = selfie_image
            user_document.save()

        return redirect("end")
    


class EndView(View):
    def get(self,request):
        #request.user.is_active = False
        #request.user.save()
        return render(request,"auth/end.html")

    
#login

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember') 

        if email and password:
            user = authenticate(request, username=email, password=password)                    
            if user:
                if user.active:
                    if remember_me:
                        request.session.set_expiry(2592000)
                    login(request, user)
                    return redirect('index')
                else : 
                    return redirect('end')
            else :
                messages.error(request, 'Informations de connexion incorrectes')
                return render(request, 'auth/login.html')
        
        else :
            messages.error(request, 'Veuillez remplir tout les champs')
            return render(request, 'auth/login.html')

#logout
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Vous avez été deconnecté')
        return redirect('login')
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Vous avez été deconnecté')
        return redirect('login')
    


class ChangePasswordView(View):
    def post(self, request):
        current_password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        renew_password = request.POST.get('renewpassword')

        if current_password and new_password and renew_password:
            # Check if the new passwords match
            if new_password == renew_password:
                # Check the current password
                if request.user.check_password(current_password):
                    # Change the user's password
                    request.user.set_password(new_password)
                    request.user.save()

                    # Update the session to prevent the user from being logged out after a password change
                    update_session_auth_hash(request, request.user)

                    messages.success(request, 'Votre mot de passe a été modifié')  # Redirect to a success page or any other desired URL
                else:
                    messages.error(request, 'Mot de passe actuel incorrect')
            else:
                messages.error(request, 'Votre nouveau mot de passe ne correspond pas')
        else:
            messages.error(request, 'Veuillez remplir tous les champs correctement')

        return redirect("settings")

class ChangePasswordView2(View):
    def get(self,request):
        return render(request,"auth/changepassword2.html")
    def post(self, request):
        email = request.POST.get('email')
        user = get_user_model()
        # Check if a user with the provided email exists
        try:
            User = get_user_model()
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            # You might want to handle the case where the user doesn't exist
            messages.error(request, 'Aucun utilisateur ne correspond à cet email')
            return render(request,"auth/changepassword2.html")

        # Generate a password reset token and send an email to the user
        current_site = get_current_site(request)

        email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

        link = reverse('reset', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Réinitialiser votre mot de passe'
        activate_url = 'https://'+email_body['domain']+link

                                # Create the HTML for the button link
        button_html = f'<a href="{activate_url}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #ffffff; text-decoration: none; border-radius: 5px;">Réinitialisation</a>'


                # Email message with the button link
        email_message = (
            f"Bonjour {user.prenoms}, clique sur le bouton suivant pour changer ton mot de passe :\n"
            f"</br></br>"
            f"{button_html}"
        )


        email = EmailMessage(
            email_subject,
            email_message,
            'appleshopnow@outlook.com',
            [email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        messages.success(request, 'Le lien de reinitialisation a bien été envoyé, veuillez verifier vos mail(spam aussi)')
    
        return render(request,"auth/changepassword2.html")
    


class PasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            request.session['id'] = id

            if  account_activation_token.check_token(user, token):

                return render(request,'auth/passwordupdate.html')

        except Exception as ex:
            messages.error(request,"Le lien que vous avez suivi n'est pas valide")

            return redirect('changepassword2')



class PasswordUpdateView(View):

    def post(self, request):
        id = request.session.get('id')
        User = get_user_model()
        new_password = request.POST['newpassword']
        renew_password = request.POST['renewpassword']
        try:
   
            user = User.objects.get(pk=id)
            if new_password == renew_password:
                user.set_password(new_password)
                user.save()

                return redirect('login')  

            else:
                messages.error(request,'Les mots de passe ne correspondent pas.')
                return render(request, "auth/password_update.html")

        except Exception as ex:
            pass

        return redirect('changepassword2')
 