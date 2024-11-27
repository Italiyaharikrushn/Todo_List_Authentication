from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male')
    age = models.PositiveIntegerField()
    profession = models.CharField(max_length=100)
