from django.contrib.auth.models import User
from django.db import models

from userservices.sessionStatus import SessionStatus


class Basemodel(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Role(Basemodel):
    name = models.CharField(max_length=255)


class User(Basemodel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name


class Session(Basemodel):
    token = models.CharField(max_length=255)
    expiring_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_status = models.CharField(
        max_length=50,
        choices=[(status.value[0], status.value[1]) for status in SessionStatus],
        default=SessionStatus.ACTIVE.value[0]
    )
