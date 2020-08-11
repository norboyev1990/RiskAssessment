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
