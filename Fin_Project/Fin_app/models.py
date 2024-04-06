from django.db import models
class Address(models.Model):
    hno = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    def __str__(self):
        return self.city
class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    address = models.CharField(max_length=200)
    def __str__(self):
        return self.company_name
class Qualification(models.Model):
    qualification_name = models.CharField(max_length=100)
    percentage = models.FloatField()
    def __str__(self):
        return self.qualification_name


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_no = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='projects/',blank=True,null=True)
    address_details = models.OneToOneField(Address, on_delete=models.CASCADE)
    work_experience = models.ManyToManyField(WorkExperience)
    qualifications = models.ManyToManyField(Qualification)
    projects = models.ManyToManyField(Project)
    
    def __str__(self):
        return self.name
