from django.contrib import admin
from rephrase.models import User, Message, Server, Chat, FriendsList
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    # This is simply for displaying User model fields on the Admin page to check database data
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'language',
                   'theme', 'profile_img', 'is_staff']
    list_filter = ['username']
    search_fields = ['username']


class MessageAdmin(admin.ModelAdmin):
    # This is simply for displaying Message model fields on the Admin page to check database data
    list_display = ['user', 'chat', 'text', 'date_time']


class ServerAdmin(admin.ModelAdmin):
    # This is simply for displaying Server model fields on the Admin page to check database data
    list_display = ['name']


class ChatAdmin(admin.ModelAdmin):
    # This is simply for displaying Chat model fields on the Admin page to check database data
    list_display = ['name', 'server_id',]
    list_filter = ['user']


class FriendsListAdmin(admin.ModelAdmin):
    # This is simply for displaying FriendsList model fields on the Admin page to check database data
    list_display = ['user']
    list_filter = ['user']


admin.site.register(User, UserAdmin)  # Register the new display rules
admin.site.register(Message, MessageAdmin)   # Register the new display rules
admin.site.register(Server, ServerAdmin)   # Register the new display rules
admin.site.register(Chat, ChatAdmin)   # Register the new display rules
admin.site.register(FriendsList, FriendsListAdmin)   # Register the new display rules

