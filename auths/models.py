from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class UserDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    #for the passport or the recto face of id card
    image = models.ImageField(upload_to='user_documents/')
    #for only the verso face of id card
    image2 = models.ImageField(upload_to='user_documents/',blank=True, null=True)
    selfie = models.ImageField(upload_to='user_documents/', blank=True, null=True)  # Add the selfie field

    def __str__(self):
        return self.document_type
    

class CustomUser(AbstractUser):
    # Additional fields for your custom user model
    name = models.CharField(max_length=255)
    prenoms = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    logement = models.CharField(max_length=255)
    address = models.TextField()
    fiscal_resident = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    profession = models.CharField(max_length=255,null=True)
    revenu = models.CharField(max_length=20)
    consiller_id = models.CharField(max_length=20, null=True)
    profil_img = models.ImageField(upload_to='user_profil_img/', blank=True, null=True)
    active = models.BooleanField(default=False)

    @property
    def profile_image_url(self):
        if self.profil_img:
            return self.profil_img.url
        else:
            # Use the default profile image if the user's image is not set
            return settings.STATIC_URL + 'img/profil.png'


