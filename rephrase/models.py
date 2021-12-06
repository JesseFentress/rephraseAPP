from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from rephraseAPP.settings import LANGUAGE_CHOICES
from django.conf.global_settings import LANGUAGES
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, language, password=None, is_admin=False,
                    is_staff=False, is_superuser=False):
        if not username:  # If there is no username submitted
            raise ValueError("Username is required")  # Raise error
        if not email:  # If there is no email submitted
            raise ValueError("Email is required")  # Raise error
        if not first_name:  # If there is no first name submitted
            raise ValueError("First Name is required")  # Raise error
        if not last_name:  # If there is no last name submitted
            raise ValueError("Last Name is required")  # Raise error
        if not language:  # If there is no language submitted
            raise ValueError("Language is required")  # Raise error
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name,
                          last_name=last_name, language=language, is_admin=is_admin, is_staff=is_staff,
                          is_superuser=is_superuser)   # Create a model object
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the nwe User model
        return user  # Return the user

    def create_superuser(self, username, email, first_name, last_name, password, language):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            language=language,
            is_admin=True,
            is_staff=True,
            is_superuser=True
        )  # Creates a new superuser for admin purposes
        return user  # Return the superuser


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, null=False)  # Username field
    email = models.EmailField(verbose_name='email', max_length=30, unique=True, null=False)  # Email field
    first_name = models.CharField(verbose_name='first name', max_length=20, null=False)  # First name field
    last_name = models.CharField(verbose_name='last name', max_length=20, null=False)  # Last name field
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)  # Date field
    language = models.CharField(verbose_name='language', max_length=7, choices=LANGUAGES, default='en')  # Language field
    theme = models.CharField(verbose_name='theme', max_length=20, null=True, default='Light')  # Theme field (not used)
    profile_img = models.ImageField(verbose_name='profile img', null=True, default='default.jpg', upload_to='images')  # Profile image field

    # Required by AbstractBaseUser class related to admin/superuser permissions
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()  # Handles user object creation

    USERNAME_FIELD = 'username'  # Identifier field
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'language']  # Required fields

    # More required methods and methods relating to user admin permissions
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Server(models.Model):
    name = models.CharField(verbose_name='server name', max_length=50, null=False)  # Server name field
    
    def __str__(self):
        return self.name


class Chat(models.Model):
    name = models.CharField(verbose_name='chat name', max_length=50)  # Chat name field
    server = models.ForeignKey(Server, verbose_name='server', null=True, blank=True, on_delete=models.CASCADE)  # Related server FK field
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='chat_users', blank=True, related_name='chat_users')  # Users belonging to a chat
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, verbose_name='user', null=False, on_delete=models.CASCADE)  # User FK field for sender of the message
    chat = models.ForeignKey(Chat, verbose_name='chat', on_delete=models.CASCADE, default=0)  # Chat FK field for the related chat
    text = models.TextField(verbose_name='text', max_length=300)  # Text field for the message
    date_time = models.DateTimeField(verbose_name='datetime', auto_now_add=True)  # Date field for time sent
    
    def __str__(self):
        return self.text


class FriendsList(models.Model):
    # User field for the owner of the friends list, operates like a FK field
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user', null=True, on_delete=models.CASCADE, related_name='fl_user')
    # Friends field to hold all of a user's friends
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='friends', blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, user):
        if user not in self.friends.all():  # If the friend is not already in the friends list
            self.friends.add(user)  # Add the user to the friends list
            self.save()  # Save changes

    def remove_friend(self, user):
        if user in self.friends.all():  # If the user is in the friends list
            self.friends.remove(user)  # Remove the user from the friends list
            self.save()  # Save changes
