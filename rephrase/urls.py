from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', views.home, name='home'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account, name='account')
]

urlpatterns += staticfiles_urlpatterns()
