from django.db import models

class Currency(models.Model):
    CODE = models.CharField(max_length=3, db_index=True)
    NAME = models.CharField(max_length=3)

    def __str__(self):
        return "{}: {}".format(self.CODE, self.NAME)

class CurrencyRate(models.Model):
    Currency = models.ForeignKey(Currency, related_name="currency", on_delete=models.CASCADE)
    RateDate = models.DateField()
    RateValue = models.FloatField()

    def __str__(self):
        return "{}: {} | {}".format(self.RateDate, self.Currency.NAME, str(self.RateValue))

class Industry(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=50, null=True)

class EcoSphere(models.Model):
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=50, null=True)

class OKED(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255)
    sect_code = models.CharField(max_length=5, default='00000')
    sect_name = models.CharField(max_length=255, null=True)
    industry = models.ForeignKey(Industry, related_name='oked_industry', on_delete=models.CASCADE, null=True)
    ecosphere = models.ForeignKey(EcoSphere, related_name='oked_sphere', on_delete=models.CASCADE, null=True)

class OKNX(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, related_name='oknx_industry', on_delete=models.CASCADE, null=True)
    ecosphere = models.ForeignKey(EcoSphere, related_name='oknx_sphere', on_delete=models.CASCADE, null=True)


