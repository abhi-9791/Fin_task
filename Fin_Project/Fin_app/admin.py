from django.contrib import admin
from .models import *
admin.site.register([Employee,Address,WorkExperience,Qualification,Project])
