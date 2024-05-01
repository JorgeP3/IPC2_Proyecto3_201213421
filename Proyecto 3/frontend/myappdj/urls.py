from django.urls import path
from . import views #va a al marchivo views y trae todo

#http://localhost:8000/myappdj
urlpatterns=[ 
    #http://localhost:8000/myappdj/myform
    path ("myform/", views.myform_view,name='myform'),#myform es la vista del navegador, no confundir con las peticiones del backend
    path('get_response/',views.get_response_from_flask, name='get_response'),
    path('get_response2/',views.get_response_from_flask2, name='get_response'),
]
