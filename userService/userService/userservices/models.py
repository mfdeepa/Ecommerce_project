from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models
from userservices.sessionStatus import SessionStatus
from oauth2_provider.models import AbstractApplication
from django.db import models

from django.core.validators import RegexValidator


class Basemodel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Role(Basemodel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    phone_number = models.CharField(
        max_length=10,
        validators=[phone_validator],
        verbose_name="Customer Phone Number",
        null=True,
        blank=True,
    )

    roles = models.ManyToManyField(Role, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username if self.username else f"User-{self.id}"


class Session(Basemodel):
    token = models.CharField(max_length=255)
    expiring_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_status = models.CharField(
        max_length=50,
        choices=[(status.value[0], status.value[1]) for status in SessionStatus],
        default=SessionStatus.Active.value[0]
    )



