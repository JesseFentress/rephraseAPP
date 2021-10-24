from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', views.home),
    path('sign-up/', views.sign_up)
]

urlpatterns += staticfiles_urlpatterns()
