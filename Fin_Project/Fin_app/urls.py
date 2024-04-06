from django.urls import path
from .views import *

urlpatterns = [
    
    path('employee_data/', Employee_Details_By_Pk.as_view(), name='employee-detail'),
]