from rest_framework import serializers
from .models import Address, WorkExperience, Qualification, Project, Employee

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['hno', 'street', 'city', 'state']

class WorkExperience_Serializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'from_date', 'to_date', 'address']

class Qualification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['qualification_name', 'percentage']

class Project_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'photo']

class Employee_Serializer(serializers.ModelSerializer):
    address_details = AddressSerializer()
    work_experience = WorkExperience_Serializer(many=True)
    qualifications = Qualification_Serializer(many=True)
    projects = Project_Serializer(many=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'age', 'gender', 'phone_no', 'address_details', 'work_experience', 'qualifications', 'projects']
