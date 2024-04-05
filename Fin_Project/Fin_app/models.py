from django.db import models
class Address(models.Model):
    hno = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    address = models.CharField(max_length=200)

class Qualification(models.Model):
    qualification_name = models.CharField(max_length=100)
    percentage = models.FloatField()

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='projects/')

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    address_details = models.OneToOneField(Address, on_delete=models.CASCADE)
    work_experience = models.ManyToManyField(WorkExperience)
    qualifications = models.ManyToManyField(Qualification)
    projects = models.ManyToManyField(Project)
