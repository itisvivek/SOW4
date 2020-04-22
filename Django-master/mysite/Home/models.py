from django.db import models

# Create your models here.


class Mydb(models.Model):
    Username = models.CharField(max_length=200)
    Password = models.CharField(max_length=200)


class Pol(models.Model):
    projectid = models.TextField(db_column='ProjectID', blank=True, null=True)  # Field name made lowercase.
    projectcrd = models.DateField(db_column='ProjectCRD', blank=True, null=True)  # Field name made lowercase.
    projectstatus = models.TextField(db_column='ProjectStatus', blank=True, null=True)  # Field name made lowercase.
    team = models.TextField(db_column='Team', blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'POL'
