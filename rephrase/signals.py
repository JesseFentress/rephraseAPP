from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import User, FriendsList, Chat



@receiver(post_save, sender=User, dispatch_uid='user.save_user_profile')  # Triggers when a user is created
def save_user_FriendsList(sender, instance, created, **kwargs):
    if created:  # If a User object is created
        FriendsList.objects.create(user=instance)  # Create a friends list for the user


@receiver(post_save, sender=Chat, dispatch_uid='chat.save')  # Triggers when a chat is saved (don't think it actually works)
def save_user_Chat(sender, instance, created, **kwargs):
    if created:  # If a chat is created
        Chat.objects.get(id=instance.id).user.add()  # Add the user who created the chat to the chat
