from django.contrib import admin
from rephrase.models import User, Message, Server, Chat, Contact, UserFriend, UserChat
# Register your models here.


#class UserAdmin(admin.ModelAdmin):
    #list_display = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'language',
                   # 'theme', 'profile_img', 'is_staff']


# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['profile_id', 'language', 'theme', 'contact_id', 'profile_img', 'user']


# class MessageAdmin(admin.ModelAdmin):
#     list_display = ['message_id', 'user', 'text', 'date_time', 'chat_id']


# class ServerAdmin(admin.ModelAdmin):
#     list_display = ['server_id', 'name']


# class ChatAdmin(admin.ModelAdmin):
#     list_display = ['chat_id', 'name', 'server_id']


# admin.site.register(Profile, ProfileAdmin)
# admin.site.register(User, UserAdmin)
# admin.site.register(Message, MessageAdmin)
# admin.site.register(Server, ServerAdmin)
# admin.site.register(Chat, ChatAdmin)

admin.site.register(User)
admin.site.register(Message)
admin.site.register(Server)
admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(UserFriend)
admin.site.register(UserChat)

