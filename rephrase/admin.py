from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from rephrase.models import User, Profile, Message, Server, Chat
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['profile_id', 'language', 'theme', 'contact_id', 'profile_img', 'user']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'user', 'text', 'date_time', 'chat_id']


class ServerAdmin(admin.ModelAdmin):
    list_display = ['server_id', 'name']


class ChatAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'name', 'server_id']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Chat, ChatAdmin)
