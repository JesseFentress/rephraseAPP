from django.contrib import admin
from rephrase.models import User, Message, Server, Chat, UserChat, FriendsList, FriendRequest
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'language',
                   'theme', 'profile_img', 'is_staff']
    list_filter = ['username']
    search_fields = ['username']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat', 'text', 'date_time']


class ServerAdmin(admin.ModelAdmin):
    list_display = ['name']


class ChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'server_id',]
    list_filter = ['user']


class UserChatAdmin(admin.ModelAdmin):
    list_display =['user', 'chat']


class FriendsListAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['user']


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'is_active']


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(UserChat, UserChatAdmin)
admin.site.register(FriendsList, FriendsListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)

