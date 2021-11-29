from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import User, FriendsList, Chat



@receiver(post_save, sender=User, dispatch_uid='user.save_user_profile')
def save_user_FriendsList(sender, instance, created, **kwargs):
    if created:
        FriendsList.objects.create(user=instance)


@receiver(post_save, sender=Chat, dispatch_uid='chat.save')
def save_user_Chat(sender, instance, created, **kwargs):
    if created:
        Chat.objects.get(id=instance.id).user.add()
