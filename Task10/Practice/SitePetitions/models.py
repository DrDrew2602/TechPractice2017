from django.db import models
# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

class Petitions():
    name = models.CharField()
    datecreate = models.DateField()
    category = models.CharField()
    goal = models.CharField()
    description = models.CharField()