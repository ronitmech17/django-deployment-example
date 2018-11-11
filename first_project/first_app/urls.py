from django.urls import path
from first_app import views

app_name = 'tradingterminal'

urlpatterns = [
    path('userLogin/',views.userLogin,name='userLogin'),
    path('newUser/',views.newUser,name='newUser'),
    path('optionchain/',views.optionchain,name='optionchain'),
]
