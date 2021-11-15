from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/', views.edit_account, name='edit'),
    path('chats/', views.chat_list, name='chat-list'),
    path('chats/<int:chat_id>/', views.chat, name='chat'),
    path('send', views.send, name='send'),
    path('getMessages/<int:chat_id>/', views.getMessages, name='getMessages')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
