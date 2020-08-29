from django.db import models

class List(models.Model):
    TITLE = models.CharField(max_length=255)
    ISSUE_YEAR = models.IntegerField()
    ISSUE_MONTH = models.IntegerField()
    DATE_CREATE = models.DateTimeField()

class Data(models.Model):
    ISSUANCE = models.ForeignKey(List, related_name="issuance", on_delete=models.CASCADE)
    CODE_REGION = models.CharField(max_length=3, null=True)
    MFO = models.CharField(max_length=5, null=True)
    NAIMEN_RAYON = models.CharField(max_length=255, null=True)
    NAME_CLIENT = models.CharField(max_length=255, null=True)
    CREDIT_SCHET = models.CharField(max_length=20, null=True)
    BALANS_SCHET = models.CharField(max_length=20, null=True)
    CODE_VAL = models.CharField(max_length=3, null=True)
    PROCENT_CREDIT = models.FloatField(null=True)
    PROCENT_PROSR = models.FloatField(null=True)
    SUMMA_DOGOVOR = models.FloatField(null=True)
    SUMMA_FACT = models.FloatField(null=True)
    DATE_VIDACHI = models.DateField(null=True, blank=True)
    DATE_POGASH = models.DateField(null=True, blank=True)
    DETALI_PLATEJA = models.CharField(max_length=1024, null=True)
    SEL_CREDITA = models.CharField(max_length=255, null=True)
    OTRASL_CLIENTA = models.CharField(max_length=255, null=True)
    VID_CREDITA = models.CharField(max_length=255, null=True)
    ISTOCHNIK_CREDITA = models.CharField(max_length=255, null=True)
    ZARUBEJNIY_BANK = models.CharField(max_length=512, null=True)
    SCHET_KORRESPONDENT = models.CharField(max_length=25, null=True)
    MFO_KORRESPONDENT = models.CharField(max_length=25, null=True)
    NAME_KORRESPONDENT = models.CharField(max_length=255, null=True)
    DATE_PERVOY_VYBOR = models.DateField(null=True, blank=True)
    ID_DOGOVOR = models.CharField(max_length=25, null=True)