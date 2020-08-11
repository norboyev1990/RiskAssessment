from django.db import models

class List(models.Model):
    TITLE = models.CharField(max_length=255)
    ISSUE_YEAR = models.IntegerField()
    ISSUE_MONTH = models.IntegerField()
    DATE_CREATE = models.DateTimeField()

class Data(models.Model):
    ISSUANCE = models.ForeignKey(List, related_name="issuance", on_delete=models.CASCADE)
    CODE_REGION = models.CharField(max_length=3)
    MFO = models.CharField(max_length=5)
    NAME_CLIENT = models.CharField(max_length=255)
    CREDIT_SCHET = models.CharField(max_length=20)
    BALANS_SCHET = models.CharField(max_length=20)
    CODE_VAL = models.CharField(max_length=3, null=True)
    PROCENT_CREDIT = models.FloatField()
    PROCENT_PROSR = models.FloatField()
    SUMMA_DOGOVOR = models.FloatField()
    SUMMA_FACT = models.FloatField()
    DATE_VIDACHI = models.DateField(null=True, blank=True)
    DATE_POGASH = models.DateField(null=True, blank=True)
    SEL_CREDITA = models.CharField(max_length=255)
    OTRASL_CLIENTA = models.CharField(max_length=255)
    VID_CREDITA = models.CharField(max_length=255)
    ISTOCHNIK_CREDITA = models.CharField(max_length=255)
    SCHET_KORRESPONDENT = models.CharField(max_length=25)
    MFO_KORRESPONDENT = models.CharField(max_length=25, null=True)
    NAME_KORRESPONDENT = models.CharField(max_length=255)
    DATE_PERVOY_VYBOR = models.DateField(null=True, blank=True)


