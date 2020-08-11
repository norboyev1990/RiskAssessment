import pandas as pd
from django.db import connection
from django.db.models.expressions import RawSQL
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from credits.models import DataByGeocode
from credits.queries import Query
from .models import Clients, InfoCredits

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def clients_list(request):
    MAX_OBJECTS = 20
    sql = """
        SELECT 
            UNIQUE_CODE AS ClientID,
            MAX(NAME_CLIENT) AS ClientName,
            MAX(SUBJECT) AS ClientType,
            SUM(VSEGO_ZADOLJENNOST) AS TotalLoans,
            MAX(ADRESS_CLIENT) AS Address
        from credits
        WHERE REPORT_id = %s AND CLIENT_TYPE = 'J'
        GROUP BY UNIQUE_CODE
    """

    cursor = connection.cursor()
    cursor.execute(sql, [1])
    results = dictfetchall(cursor)
    data = {"results": list(results)}
    return JsonResponse(data)

def clients_detail(request, pk):
    pass

def get_stat_data(request):
    month = pd.to_datetime(request.current_month)
    model = InfoCredits.objects.raw('SELECT ROWNUM as id, T.* FROM TABLE(GET_INDS(%s)) T', [month])

    data = {"results": {
        "kpr": {"values": model[0].New_Value, "increase": model[0].Percent},
        "npl": {"values": model[1].New_Value, "increase": model[1].Percent},
        "tox": {"values": model[3].New_Value, "increase": model[3].Percent},
        "prs": {"values": model[8].New_Value, "increase": model[8].Percent},
    }}
    return JsonResponse(data)

def get_gdp_data(request):
    month = pd.to_datetime(request.current_month)
    model = InfoCredits.objects.raw('SELECT ROWNUM as id, T.* FROM TABLE(GET_INDS(%s)) T', [month])
    gdpData = {}
    gdpName = {}
    geoTitle = "Токсичные кредиты"
    geoData = DataByGeocode.objects.raw(Query.orcl_toxics_by_branches(), [4])
    for p in geoData:
        gdpData[p.GeoCode] = int(p.Balance)
        gdpName[p.GeoCode] = p.Title

    data = {"results": {
        "gdp_data": gdpData,
        "gdp_name": gdpName,
    }}
    return JsonResponse(data)
