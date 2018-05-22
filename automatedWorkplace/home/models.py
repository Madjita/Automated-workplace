from django.db import models
from django.utils import timezone


class TableAutomatedWorkstation(models.Model):
    name = models.TextField();
    about = models.TextField();
# Create your models here.

class TableDevice(models.Model):
    nameDevice = models.TextField();
    name = models.TextField();
    ip = models.CharField(max_length=50);
    serial = models.TextField();
    mode = models.CharField(max_length=100);
    IdWorkstation = models.ForeignKey(TableAutomatedWorkstation,on_delete=models.CASCADE);
