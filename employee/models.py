from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.files import FileField
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .validators import validate_file_extension
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50,default='Anonymous')
    email = models.EmailField(max_length=254, unique=True)
    username = None
    is_registered = models.BooleanField(default= False)
    #changed the username field from username to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )

    def __str__(self):
        return str(self.email)

class Employee(models.Model):
    # method for validating file type as well as saving the file into a folder
    def aadharFile(instance,filename):
        now = datetime.now()
        extension = filename.split(".")
        if extension[-1] == 'pdf':
            return ''.join(['documents/aadhar_card/',now.strftime("%d-%m-%Y"),'/',str(instance.email),'/',filename])
        else:
            content = {'error': ['Unsupported file type']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    def panFile(instance,filename):
        now = datetime.now()
        extension = filename.split(".")
        if extension[-1] == 'pdf':
            return ''.join(['documents/pan_card/',now.strftime("%d-%m-%Y"),'/',str(instance.email),'/',filename])
        else:
            content = {'error': ['Unsupported file type']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    def passportFile(instance,filename):
        now = datetime.now()
        extension = filename.split(".")
        if extension[-1] == 'pdf':
            return ''.join(['documents/passport/',now.strftime("%d-%m-%Y"),'/',str(instance.email),'/',filename])
        else:
            content = {'error': ['Unsupported file type']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    def licenseFile(instance,filename):
        now = datetime.now()
        extension = filename.split(".")
        if extension[-1] == 'pdf':
            return ''.join(['documents/driving_license/',now.strftime("%d-%m-%Y"),'/',str(instance.email),'/',filename])
        else:
            content = {'error': ['Unsupported file type']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    class Gender(models.TextChoices):
        MALE = 'Male'
        FEMALE = 'Female'
        RATHER_NOT_SPECIFY = 'Rather not specify'
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=254, unique=True)
    gender = models.CharField(max_length=50, choices=Gender.choices, default=Gender.MALE)
    age = models.IntegerField(default=20)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    role = models.CharField(max_length=25,default='Employee')
    bank_name = models.CharField(max_length=25)
    account_no = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=50)
    bank_branch_location = models.CharField(max_length=15)
    aadhar_card = FileField(upload_to=aadharFile,validators=[validate_file_extension ])
    pan_card = FileField(upload_to=panFile,validators=[validate_file_extension ])
    passport = FileField(upload_to=passportFile,validators=[validate_file_extension ])
    driving_license = FileField(upload_to=licenseFile,validators=[validate_file_extension ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )
    def __str__(self):
        return str(self.email)

class Invite(models.Model):
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )
    def __str__(self):
        return str(self.email)

class Notifications(models.Model):
    message = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True )


# class Employee_Bank_Details(models.Model):
#     employee = models.OneToOneField(Employee, on_delete=CASCADE, default= None,unique=True,blank=True,null=True)
#     bank_name = models.CharField(max_length=25)
#     account_no = models.CharField(max_length=50)
#     ifsc_code = models.CharField(max_length=50)
#     branch_location = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True )
#     def __str__(self):
#         return str(self.employee)

# class Employee_Documents(models.Model):
#     employee = models.OneToOneField(Employee, on_delete=CASCADE, default= None,unique=True,blank=True,null=True)
#     aadhar_card = FileField(upload_to='documents/aadhar_card/%Y/%m/%d')
#     pan_card = FileField(upload_to='documents/pan_card/%Y/%m/%d')
#     passport = FileField(upload_to='documents/passport/%Y/%m/%d')
#     driving_license = FileField(upload_to='documents/driving_license/%Y/%m/%d')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True )
#     def __str__(self):
#         return str(self.employee)
