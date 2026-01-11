import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



class IdentityType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class PersonalInformation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    identity_type = models.OneToOneField(
        IdentityType,
        on_delete=models.PROTECT,
        unique=False
    )
    identity_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} {self.lastname}"


# AbstractUser es la entidad generica padre que se encarga de crear un usuario y manejar su autenticación
class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
  
    personal_information = models.OneToOneField(
        PersonalInformation,
        on_delete=models.CASCADE,
        unique=True  
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.username
