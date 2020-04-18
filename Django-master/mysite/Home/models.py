from django.db import models

# Create your models here.


class Mydb(models.Model):
    Username = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)


