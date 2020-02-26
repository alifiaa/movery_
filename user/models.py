from django.db import models

# Create your models here.

class User(models.Model):
    id = models.IntegerField(default='', primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(default='')
    is_superuser = models.BooleanField(default='')
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default='')
    is_active = models.BooleanField(default='')
    date_joined = models.DateTimeField(default='')
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return self.id + '|' + self.username

    @staticmethod
    def get_name():
        return 'user'