from django.db import models

class Classification(models.Model):
    Status = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=45, verbose_name="Класс")
    Balance = models.FloatField(verbose_name="Всего задолженность")
    Percent = models.FloatField(verbose_name="Доля, %")
    Counts = models.IntegerField(verbose_name="Количество")
    Reserve = models.FloatField(verbose_name="Резервы")
    Needed = models.FloatField(verbose_name="Необход. резервы")

    class Mete:
        managed = False

