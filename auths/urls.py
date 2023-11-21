from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('mail',Emailview.as_view(),name="mail"),
    path('login', LoginView.as_view(), name="login"),
    path('adresse',AdresseView.as_view(),name="adresse"),
    path('userinfo',UserInformationView.as_view(),name="userInfo"),
    path('fiancial',FinancialView.as_view(),name="financial"),
    path('usage',UsageView.as_view(),name="usage"),
    path('profession',ProfesionView.as_view(),name="profession"),
    path('revenu',RevenuView.as_view(),name="revenu"),
    path('birth',BirthView.as_view(),name="birth"),
    path('verification',VerificationView.as_view(),name="verification"),
    path("upload",UploadView.as_view(),name="upload"),
    path("password", CreationView.as_view(),name="password"),
    path("selfie",SelfieView.as_view(),name="selfie"),
    path("end",EndView.as_view(),name="end"),
    path("logout",LogoutView.as_view(),name="logout"),
    path('changepassword',ChangePasswordView.as_view(),name="changepassword"),
    path('changepassword2',ChangePasswordView2.as_view(),name="changepassword2"),
    path('reset/<uidb64>/<token>',PasswordResetConfirmView.as_view(),name="reset"),
    path("update",PasswordUpdateView.as_view(),name="update")
]
