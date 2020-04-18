from django.db import models

# Create your models here.
class WorkOrderEscalation(models.Model):
    ProjectId = models.CharField(max_length=200)
    WorkOrder = models.CharField(max_length=200)
    CircuitId = models.CharField(max_length=200)
    CrdDate = models.DateField()
    Status = models.CharField(max_length=200)
    Assignee = models.CharField(max_length=200)
    AssignedTeam = models.CharField(max_length=200)

