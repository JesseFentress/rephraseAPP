from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rephraseAPP.settings import LANGUAGE_CHOICES

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, password=None):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First Name is required")
        if not last_name:
            raise ValueError("Last Name is required")
        user = self.model(self.normalize_email(email), username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(email=self.normalize_email(email), username=username, first_name=first_name, last_name=last_name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        return user


class User(AbstractBaseUser):
    user_id = models.AutoField(verbose_name='user id', unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True, null=False)
    email = models.EmailField(verbose_name='email', max_length=30, unique=True, null=False)
    first_name = models.CharField(verbose_name='first name', max_length=20, null=False)
    last_name = models.CharField(verbose_name='last name', max_length=20, null=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    profile_id = models.AutoField(verbose_name='profile id', unique=True, primary_key=True)
    language = models.CharField(verbose_name='language', max_length=5, choices=LANGUAGE_CHOICES, default='en')
    theme = models.CharField(verbose_name='theme', max_length=20, null=True, default='Light')
    contact_id = models.IntegerField(verbose_name='contact id', unique=True, null=True)
    profile_img = models.ImageField(verbose_name='profile img', null=True)
    user = models.OneToOneField(User, verbose_name='user id', null=True, on_delete=models.CASCADE)


class Server(models.Model):
    server_id = models.AutoField(verbose_name='server id', primary_key=True)
    name = models.CharField(verbose_name='server name', max_length=50, null=False)


class Chat(models.Model):
    chat_id = models.AutoField(verbose_name='chat id', primary_key=True)
    name = models.CharField(verbose_name='chat name', max_length=50)
    server_id = models.OneToOneField(Server, verbose_name='server id', null=True, on_delete=models.CASCADE)


class Message(models.Model):
    message_id = models.AutoField(verbose_name='message id', primary_key=True)
    user = models.ForeignKey(User, verbose_name='user id', null=False, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='text', max_length=300)
    date_time = models.DateTimeField(verbose_name='datetime', auto_now_add=True)
    chat_id = models.OneToOneField(Chat, verbose_name='chat id', on_delete=models.CASCADE, default=0)















