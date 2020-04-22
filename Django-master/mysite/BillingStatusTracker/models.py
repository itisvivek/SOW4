from django.db import models

# Create your models here.
class Billing(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    projectid = models.CharField(max_length=200)  # Field name made lowercase.
    svcno = models.CharField(max_length=200)  # Field name made lowercase.
    svcorderstatus = models.CharField(max_length=200)  # Field name made lowercase.
    workorder = models.CharField(max_length=200)  # Field name made lowercase.
    workorderstatus = models.CharField(max_length=200)  # Field name made lowercase.
    crd = models.DateField()  # Field name made lowercase.
    speed = models.CharField(max_length=200)  # Field name made lowercase.
    updates = models.CharField(max_length=200)  # Field name made lowercase.
    Billed_status = models.CharField(max_length=200)
    Billed_by = models.CharField(max_length=200)  # request.user.get_username()
    Billed_date = models.DateField()

    class Meta:
        managed = True
        # db_table = 'SearchWo_pegasus'