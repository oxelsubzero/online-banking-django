from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path("",IndexView.as_view(),name="index"),
    path("carte",CarteView.as_view(),name="carte"),
    path("transfert",TransfertView.as_view(),name="send"),
    path("conseiller",AutreView.as_view(),name="autre"),
    path("rib",RibView.as_view(),name="rib"),
    path("beneficiaire",BeneficiaireRegisterView.as_view(),name="beneficiaire"),
    path("VirementInst",VirementInst.as_view(),name="VirementInst"),
    path("VirementInterne",VirementInterneView.as_view(),name="VirementInterne"),
    path("verification_code",ValidationCodeView.as_view(),name="verification_code"),
    path("settings",SettingsView.as_view(),name='settings'),
    path("sucess",SucessView.as_view(),name="sucess"),
    path('verification_code2',ValidationCode2View.as_view(),name="verification_code2"),
    path('account/<str:account_type>/', Account_details.as_view(), name='account_details'),
]
