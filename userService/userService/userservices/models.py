from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.db import models

from userservices.sessionStatus import SessionStatus


class Basemodel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Role(Basemodel):
    name = models.CharField(max_length=255)


class User(AbstractUser):
    # name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    roles = models.ManyToManyField(Role, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # New related name for groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # New related name for permissions
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
