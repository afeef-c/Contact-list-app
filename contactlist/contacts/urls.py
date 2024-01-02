from django.urls import path
from . import views


urlpatterns = [

    path('register/', views.register, name="register"),
    path('adminlogin/', views.login_admin, name="adminlogin"),
    path('userlogin/', views.login_user, name="userlogin"),
    path('logout/', views.logout_user, name="logout"),
    

    path('', views.index, name='index'),
    path('add-contact/', views.addContact, name = 'add-contact'),
    path('profile/<str:pk>', views.contactProfile, name='profile'),
    path('edit-contact/<str:pk>', views.editContact, name='edit-contact'),
    path('delete/<str:pk>', views.deleteContact, name = 'delete') 
]