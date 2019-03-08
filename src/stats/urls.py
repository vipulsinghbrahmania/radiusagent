from django.urls import path                                                                                                      
from . import views 
                                          

urlpatterns = [                                                          
    path('', views.home, name='stats-home'),  # path to the homepage.                
]