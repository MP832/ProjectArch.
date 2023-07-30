from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('registratie/<uidb64>/<eve>', views.registratie, name='registratie'),
    path('merci',views.merci, name = 'merci'),
    path('send/<str:pk>',views.send, name='send'),
    path('send1/<str:pk>',views.mailsturen, name='send1'),
    path('terms', views.terms, name='terms'), 
    path('check/<uidb64>', views.qrcodecheck, name='check'),
    path('', views.overzicht , name='overzicht'),
    path('mailcentrum', views.mailselector, name='mailcentrum'),
    path('evenement/<str:pk>', views.evene, name='evenement'),
    path('download/<str:pk>', views.download_file, name='download_file'),

]
