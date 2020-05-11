from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

NEW = "new"
IN_PROGRESS = "In Progress"
FINISHED = "Finished"

STATUS_CHOICES = [
    (NEW, "new"),
    (IN_PROGRESS, "In Progress"),
    (FINISHED, "Finished"),
]

class User(AbstractUser):
    # org_id = models.ForeignKey('Organization', on_delete = models.CASCADE, null = True, blank = True)
    status = models.CharField(max_length = 100, choices = STATUS_CHOICES, blank = True)

class Organization(models.Model):
    user = models.OneToOneField('user', on_delete = models.CASCADE, default = 1)
    name = models.CharField(max_length = 150)
    type_id = models.CharField(max_length = 150)
    comm_address1 = models.TextField()
    comm_address2 = models.TextField()
    comm_country = models.CharField(max_length = 150)
    comm_state = models.CharField(max_length = 150)
    comm_district = models.CharField(max_length = 150)
    comm_phone = models.CharField(max_length = 150)
    comm_email = models.CharField(max_length = 150)
    comm_status = models.CharField(max_length = 150, choices = STATUS_CHOICES)
    comm_gstin = models.CharField(max_length = 150)
    bill_address1 = models.TextField()
    bill_address2 = models.TextField()
    bill_country = models.CharField(max_length = 150)
    bill_state = models.CharField(max_length = 150)
    bill_district = models.CharField(max_length = 150)
    bill_phone = models.CharField(max_length = 150)
    bill_email = models.CharField(max_length = 150)
    bill_status = models.CharField(max_length = 150, choices = STATUS_CHOICES)
    bill_gstin = models.CharField(max_length = 150)

    def __str__(self):
        return self.name

class Card(models.Model):
    card_number = models.CharField(max_length = 20)
    name_on_card = models.CharField(max_length = 100)
    expiry_date = models.CharField(max_length = 20)
    cvv = models.CharField(max_length = 10)
    org_id = models.ForeignKey('Organization', on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.name_on_card

class Project(models.Model):
    title = models.CharField(max_length = 150)
    summary = models.TextField()
    duration = models.CharField(max_length = 50)
    start_date = models.CharField(max_length = 50)
    end_date = models.CharField(max_length = 50)
    status = models.CharField(max_length = 100, choices = STATUS_CHOICES, blank = True)
    org_id = models.ForeignKey('Organization', on_delete = models.CASCADE, null = True, blank = True)

    def __str__(self):
        return self.title

class Plan(models.Model):
    description = models.CharField(max_length = 200)
    details = models.TextField()
    logins = models.CharField(max_length = 100)
    price = models.CharField(max_length = 100)
    created_date_time = models.CharField(max_length = 100)
    validity = models.CharField(max_length = 100)
    status = models.CharField(max_length = 100)

    def __str__(self):
        return self.description

class Subscription(models.Model):
    plan = models.ForeignKey('Plan', on_delete = models.CASCADE)
    project = models.ForeignKey('Project', on_delete = models.CASCADE)
    # name = models.CharField(max_length = 200)
    subscription_date_time = models.CharField(max_length = 100)
    renewal_date_time = models.CharField(max_length = 100)
    auto_renewal = models.BooleanField()
    status = models.CharField(max_length = 100)
    razorpay_order_id = models.CharField(max_length = 100)
