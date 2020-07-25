from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('select/', views.select, name='select'),
    path('result/',views.result,name='result'),
    #path('select/<int:year>/',views.select,name='select')
]