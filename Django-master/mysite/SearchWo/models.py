from django.db import models

# Create your models here.
class Pegasus(models.Model):
    ProjectId = models.CharField(max_length=200)
    SvcNo = models.CharField(max_length=200)
    SvcOrderStatus = models.CharField(max_length=200)
    WorkOrder = models.CharField(max_length=200)
    WorkOrderStatus = models.CharField(max_length=200)
    CRD = models.DateField()
    Speed = models.CharField(max_length=200)
    Updates = models.CharField(max_length=200)
    def __str__(self):
        return (self.ProjectId + "," + self.SvcNo + "," + self.WorkOrder)

    class Meta:
        verbose_name_plural = "Pegasus Records"


