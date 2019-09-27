from django.db import models
from datetime import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta

import re	# the regex module

class BlogManager(models.Manager):
    def filler_validator(self, postData):
        errors = {}
        # curr_date = str((datetime.now() - timedelta(weeks=260)))

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 2:
            errors["password"] = "Password should be at least 8 characters"
        if datetime.strptime(postData['birth_date'], "%Y-%m-%d") > datetime(year=2001, month=9, day=1):
            errors["birth_date"] = "Must be at least 18"
        # if datetime.strptime(postData['birth_date'], "%Y-%m-%d") < datetime.today():
        #     errors["birth_date"] = "BirthDate should be in the past"

        if len(postData['carModel']) < 2:
            errors["carModel"] = "Car Model should be at least 3 characters"

        if len(postData['carColor']) < 3:
            errors["carColor"] = "Car Color should be at least 5 characters"

        if len(postData['plate']) > 7:
            errors["plate"] = "License Plate # can't be more than 7 characters"
        if Driver.objects.filter(email=postData['email']):
            errors["email"] = "email is taken"

        if Filler.objects.filter(email=postData['email']):
            errors["email"] = "email is taken"
            
        if (postData['password']) != (postData['password_confirm']):
            errors["password"] = "Password's should match"
        return errors


    def driver_validator(self, postData):
        errors = {}
        # curr_date = str((datetime.now() - timedelta(weeks=260))
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 2:
            errors["password"] = "Password should be at least 8 characters"
        if datetime.strptime(postData['birth_date'], "%Y-%m-%d") > datetime(year=2001, month=9, day=1):
            errors["birth_date"] = "Must be at least 18"
        # if datetime.strptime(postData['birth_date'], "%Y-%m-%d") < datetime.today():
        #     errors["birth_date"] = "BirthDate should be in the past"

        if Driver.objects.filter(email=postData['email']):
            errors["email"] = "email is taken"

        if Filler.objects.filter(email=postData['email']):
            errors["email"] = "email is taken"

        if (postData['password']) != (postData['password_confirm']):
            errors["password"] = "Password's should match"
        return errors


    def loginValidFiller(self, request):
        thefiller = Filler.objects.filter(email=request.POST['email']) 
        if thefiller: 
            logged_filler = thefiller[0] 
            if not bcrypt.checkpw(request.POST['password'].encode(), logged_filler.password.encode()):
                messages.error(request, "Invalid password")
            else:
                return True
        messages.error(request, "Invalid email")
        return False

    def loginValidDriver(self, request):
        thedriver = Driver.objects.filter(email=request.POST['email']) 
        if thedriver: 
            logged_driver = thedriver[0] 
            if not bcrypt.checkpw(request.POST['password'].encode(), logged_driver.password.encode()):
                messages.error(request, "Invalid password")
            else:
                return True
        messages.error(request, "Invalid email")
        return False

    def submittingFillerForm(self, postData):
        errors = {}
        Number_REGEX = re.compile(r'^[0-15]+$')
        if not Number_REGEX.match(postData['Gallons']):  
            errors['Gallons'] = "First name should be at least 2 characters"
        return errors

    # def book_add_valid(self, request):
    #     errors = {}
    #     if len(request.POST['titleName']) == 0:
    #         errors["titleName"] = "Must have a Title"
    #     if len(request.POST['descriptionName']) < 5:
    #         errors["descriptionName"] = "Description should be at least 5 characters"
    #     return errors



class Filler(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirm = models.CharField(max_length=255)
    car_make = models.CharField(max_length=255)
    car_year =  models.IntegerField()
    car_model = models.CharField(max_length=255)
    car_color = models.CharField(max_length=255)
    plate = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()   

    def __repr__(self):
        return f"<Filler object: {self.first_name} {self.last_name}({self.id})>"



class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirm = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()   

    def __repr__(self):
        return f"<Driver object: {self.first_name} {self.last_name}({self.id})>"

class Address(models.Model):
    address1 = models.CharField("Address line 1",max_length=1024)
    address2 = models.CharField("Address line 2",max_length=1024)
    zip_code = models.CharField("ZIP / Postal code",max_length=12)
    state = models.CharField("ZIP / Postal code",max_length=255, blank=True, null=True )
    city = models.CharField("City",max_length=1024)
    country = models.CharField("Country",max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    objects = BlogManager()   

    def __repr__(self):
        return f"<Address object:{self.address1}  {self.address2} {self.city} {self.country} () {self.id}  )>"


TYPE_CHOICES = [
    ('87', 'Unleaded'),
    ('89', 'Plus'),
    ('91', 'Premium'),
]
class Order(models.Model):
    gallons = models.IntegerField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    address = models.ForeignKey(Address, related_name="order",blank=True, null=True,  on_delete=models.PROTECT )
    price = models.DecimalField( max_digits=5, decimal_places=2)
    filler = models.ForeignKey(Filler, related_name="order" ,blank=True, null=True,  on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, related_name="order",blank=True, null=True,  on_delete=models.PROTECT)
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()   

    def __repr__(self):
        return f"<Order object: {self.gallons}  {self.price}  {self.address} {self.type} ({self.id})>"





#     def __repr__(self):
#         return f"<Book object: {self.title} {self.desc}({self.id})>"
    # class Meta:
    #     verbose_name = "Shipping Address"
    #     verbose_name_plural = "Shipping Addresses"