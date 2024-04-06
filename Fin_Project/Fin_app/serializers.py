from rest_framework import serializers
from .models import Address, WorkExperience, Qualification, Project, Employee
from django.db import transaction
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['hno', 'street', 'city', 'state']
        read_only=('id',)
        

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
        fields = ['title', 'description']
        # read_only=('photo',)

class Employee_Serializer(serializers.ModelSerializer):
    address_details = AddressSerializer()
    work_experience = WorkExperience_Serializer(many=True)
    qualifications = Qualification_Serializer(many=True)
    projects = Project_Serializer(many=True)

    class Meta:
        model = Employee
        fields = ['name', 'email', 'age', 'gender', 'phone_no','address_details', 'work_experience', 'qualifications', 'projects','photo']
        read_only=('id,')
    def create(self,validated_data):
        address_data = validated_data.pop('address_details')
        work_experience_data = validated_data.pop('work_experience')
        qualifications_data = validated_data.pop('qualifications')
        projects_data = validated_data.pop('projects')
        # photo=validated_data('photo')

        # Create employee instance
        with transaction.atomic():
            address_details = AddressSerializer.create(AddressSerializer(), validated_data=address_data)
            work_experience_instances = []
            for work_experience_item in work_experience_data:
                work_experience_serializer = WorkExperience_Serializer(data=work_experience_item)
                work_experience_serializer.is_valid(raise_exception=True)
                work_experience_instance = work_experience_serializer.save()
                work_experience_instances.append(work_experience_instance)
            qualification_instances = []
            for qualification_item in qualifications_data:
                qualification_serializer = Qualification_Serializer(data=qualification_item)
                qualification_serializer.is_valid(raise_exception=True)
                qualification_instance = qualification_serializer.save()
                qualification_instances.append(qualification_instance)
            project_instances = []
            for project_item in projects_data:
                project_serializer = Project_Serializer(data=project_item)
                project_serializer.is_valid(raise_exception=True)
                project_instance = project_serializer.save()
                project_instances.append(project_instance)
            employee = Employee.objects.create(address_details=address_details,**validated_data)
            employee.work_experience.set(work_experience_instances)
            employee.qualifications.set(qualification_instances)
            employee.projects.set(project_instances)
            return employee
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address_details', None)
        work_experience_data = validated_data.pop('work_experience', [])
        qualifications_data = validated_data.pop('qualifications', [])
        projects_data = validated_data.pop('projects',[])
        
        
        # Update Address instance if data is provided
        if address_data:
            address_serializer = AddressSerializer(instance.address_details, data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address_serializer.save()
        
     
        instance.work_experience.all().delete()
        for work_experience_item in work_experience_data:
            work_experience_serializer = WorkExperience_Serializer(data=work_experience_item)
            work_experience_serializer.is_valid(raise_exception=True)
            work_experience_instance = work_experience_serializer.save()
            instance.work_experience.add(work_experience_instance)
        
        
        instance.qualifications.all().delete()
        for qualification_item in qualifications_data:
            qualification_serializer = Qualification_Serializer(data=qualification_item)
            qualification_serializer.is_valid(raise_exception=True)
            qualification_instance = qualification_serializer.save()
            instance.qualifications.add(qualification_instance)
        instance.projects.all().delete()
        for projects_item in projects_data:
            projects_serializer = Project_Serializer(data=projects_item)
            projects_serializer.is_valid(raise_exception=True)
            project_instance = projects_serializer.save()
            instance.projects.add(project_instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance