from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from rephraseAPP.settings import LANGUAGE_CHOICES
from django.conf.global_settings import LANGUAGES
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, language, password=None, is_admin=False,
                    is_staff=False, is_superuser=False):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First Name is required")
        if not last_name:
            raise ValueError("Last Name is required")
        if not language:
            raise ValueError("Language is required")
        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name,
                          last_name=last_name, language=language, is_admin=is_admin, is_staff=is_staff,
                          is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

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
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True, null=False)
    email = models.EmailField(verbose_name='email', max_length=30, unique=True, null=False)
    first_name = models.CharField(verbose_name='first name', max_length=20, null=False)
    last_name = models.CharField(verbose_name='last name', max_length=20, null=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    
    language = models.CharField(verbose_name='language', max_length=7, choices=LANGUAGES, default='en')
    theme = models.CharField(verbose_name='theme', max_length=20, null=True, default='Light')
    profile_img = models.ImageField(verbose_name='profile img', null=True, default='default.jpg', upload_to='images')
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'language']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Server(models.Model):
    name = models.CharField(verbose_name='server name', max_length=50, null=False)
    
    def __str__(self):
        return self.name


class Chat(models.Model):
    name = models.CharField(verbose_name='chat name', max_length=50)
    server = models.ForeignKey(Server, verbose_name='server', null=True, on_delete=models.CASCADE)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='chat_users', blank=True, related_name='chat_users')
    
    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, verbose_name='user', null=False, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, verbose_name='chat', on_delete=models.CASCADE, default=0)
    text = models.TextField(verbose_name='text', max_length=300)
    date_time = models.DateTimeField(verbose_name='datetime', auto_now_add=True)
    
    def __str__(self):
        return self.text


class FriendsList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user', null=True, on_delete=models.CASCADE, related_name='fl_user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='friends', blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, user):
        if user not in self.friends.all():
            self.friends.add(user)
            self.save()

    def remove_friend(self, user):
        if user in self.friends.all():
            self.friends.remove(user)
            self.save()

    def unfriend(self, unfriended):
        my_friend_list = self
        my_friend_list.remove_friend(unfriended)
        unfriended_friend_list = FriendsList.objects.get(user=unfriended)
        unfriended_friend_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False

    def get_friends(self):
        my_friend_list = self.friends.all()
        f_list = []
        for friend in my_friend_list:
            list.append(friend)
        return f_list


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friends_list = FriendsList.objects.get(user=self)
        if receiver_friends_list:
            receiver_friends_list.add_friend(self.sender)
            sender_fiends_list = FriendsList.objects.get(user=self.sender)
            if sender_fiends_list:
                sender_fiends_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()


class UserChat(models.Model):
    user = models.ForeignKey(User, verbose_name='user', null=False, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, verbose_name='chat', null=False, on_delete=models.CASCADE)