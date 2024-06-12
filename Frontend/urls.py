from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.login,name='login'),
    path("register/",views.register,name='register'),
    path("about/",views.about,name='about'),
    path("team/",views.team,name='team'),
    path("contact/",views.contact,name='contact'),
    path("listen_to_frontend/",views.listenToFrontend,name='listen_to_frontend'),
    
]
