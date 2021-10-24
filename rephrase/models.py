from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=30, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=20, null=False)
    last_name = models.CharField(verbose_name="last name", max_length=20, null=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


