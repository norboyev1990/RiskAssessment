from django.db import models


@classmethod
class PeriodList1(models.Model):
    Code = models.IntegerField(db_index=True)
    Name = models.CharField(max_length=25)
    MinD = models.IntegerField()
    MaxD = models.IntegerField()


@classmethod
class PeriodList2(models.Model):
    Code = models.IntegerField(db_index=True)
    Name = models.CharField(max_length=25)
    MinD = models.IntegerField()
    MaxD = models.IntegerField()
