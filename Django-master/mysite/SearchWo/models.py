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
    task_name = models.TextField(db_column='Task_Name', blank=True, null=True)  # Field name made lowercase.
    next_escalation_level = models.CharField(db_column='Next_Escalation_Level', max_length=2, blank=True,
                                             null=True)  # Field name made lowercase.
    next_escalation_date = models.DateField(db_column='Next_Escalation_Date', blank=True,
                                            null=True)  # Field name made lowercase.
    escalation_history = models.TextField(db_column='Escalation_History', blank=True,
                                          null=True)  # Field name made lowercase.
    order_type = models.TextField(db_column='Order_Type', blank=True, null=True)  # Field name made lowercase.
    task_status = models.TextField(db_column='Task_Status', blank=True, null=True)

    def __str__(self):
        return (self.ProjectId + "," + self.SvcNo + "," + self.WorkOrder)

    class Meta:
        verbose_name_plural = "Pegasus Records"
        managed = False
        db_table = 'SearchWo_pegasus'
