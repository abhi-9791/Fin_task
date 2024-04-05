from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Employee
from .serializers import Employee_Serializer
