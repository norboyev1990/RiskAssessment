import json

import pandas as pd
from django.db import connection
from django.db.models.expressions import RawSQL
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from credits.models import DataByGeocode, ListReports, ByTerms
from credits.queries import Query as Qry
from .models import Clients, InfoCredits, DataForLineChart
from . queries import Query
from credits.queries import Query as CreditsQuery

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def clients_list(request):
    month = pd.to_datetime(request.current_month)
    MAX_OBJECTS = 20
    sql = """
        SELECT 
            UNIQUE_CODE AS ClientID,
            MAX(NAME_CLIENT) AS ClientName,
            MAX(SUBJECT) AS ClientType,
            MAX(CB.NAME) AS BranchName,
            SUM(VSEGO_ZADOLJENNOST) AS TotalLoans,
            SUM(OSTATOK_REZERV) AS TotalReserve,
            MAX(ADRESS_CLIENT) AS Address,
            CLIENT_STATUS(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                sum(ostatok_vneb_prosr),sum(ostatok_peresm)) AS StatusClient,
            GET_RESERVE(CLIENT_STATUS(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                sum(ostatok_vneb_prosr),sum(ostatok_peresm)), 
                SUM(VSEGO_ZADOLJENNOST), SUM(OSTATOK_REZERV)) AS Reserve
        from credits
        left join CREDITS_BRANCH CB on CREDITS.MFO = CB.CODE
        WHERE REPORT_id = %s and CLIENT_TYPE = 'J'
        GROUP BY UNIQUE_CODE
    """

    cursor = connection.cursor()
    cursor.execute(sql, [month.month])
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
    geoData = DataByGeocode.objects.raw(Qry.orcl_toxics_by_branches(), [4])
    for p in geoData:
        gdpData[p.GeoCode] = int(p.Balance)
        gdpName[p.GeoCode] = p.Title

    data = {"results": {
        "gdp_data": gdpData,
        "gdp_name": gdpName,
    }}
    return JsonResponse(data)

def get_krp_by_month(request, type):
    month = pd.to_datetime(request.current_month)

    cursor = connection.cursor()

    obj = DataForLineChart.objects.raw(Query.full_by_month())
    kpr = []
    npl = []
    tox = []
    psr = []
    res = []
    for p in obj:
        if p.Title=='kpr':
            kpr.append(p.Total)
            psr.append(p.Prosr)
            res.append(p.Reserv)
        elif p.Title=='npl':
            npl.append(p.Total)
        else:
            tox.append(p.Total)

    result = {"result":{
        "kpr":kpr,
        "npl":npl,
        "tox":tox,
        "psr":psr,
        "res":res,
    }}
    # json_data = {"result": {"kpr": ["12000", "15000", "26946.70980173791", "27982.49422765372", "29742.10725456284", "30329.61006599574", "31515.38388095416"], "npl": ["991.4880915545", "861.86874575586", "1081.0339666956", "3637.29992199525", "1127.85109826379", "1383.78372974605", "1736.75536193891"], "tox": ["121.97318443327", "135.85664303761", "135.81901914716", "166.07014700864", "190.7927090907", "425.80470223889", "317.11509329138"], "psr": ["198.89177415448", "181.50186615989", "293.42528151373", "396.93961462499", "187.47117005656", "204.28948383675", "235.07739477534"], "res": ["769.92253768882", "810.74463102061", "917.5118377796", "899.92534737213", "922.44560144758", "950.60027264417", "944.50576655866"]}}

    return JsonResponse(result)

def get_data_subjects(request):
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = CreditsQuery.orcl_bysubjects()
    cursor = connection.cursor()
    cursor.execute(query, [report.id])
    data = dictfetchall(cursor)

    result = {"result":{
        "data":list(data)
    }}

    return JsonResponse(result)

def get_data_branches(request):
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = CreditsQuery.orcl_bybranches()
    cursor = connection.cursor()
    cursor.execute(query, [report.id])
    data = dictfetchall(cursor)

    result = {"result":{
        "data":list(data)
    }}

    return JsonResponse(result)

def get_data_average(request):
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = CreditsQuery.orcl_byaverageweight_fl()
    cursor = connection.cursor()
    cursor.execute(query, [report.id])
    data = dictfetchall(cursor)

    for idx in range(len(data)):
        if (data[idx]['TITLE'] == 'Овердрафт по пластиковым карточкам физических лиц'):
            data[idx]['TITLE'] = 'Овердрафт'
        elif (data[idx]['TITLE'] == 'Кредиты, выданные по инициативе банка'):
            data[idx]['TITLE'] = 'Кредиты выд. инц. банка'

    result = {"result":{
        "data":list(data)
    }}

    return JsonResponse(result)

def get_data_average_juridical(request):
    month = pd.to_datetime(request.current_month)
    report = ListReports.objects.get(REPORT_MONTH=month.month, REPORT_YEAR=month.year)

    query = '''
        select SROK, CODE_VAL, SUM(VSEGO_ZADOLJENNOST) BALANCE
        from CREDITS
        where REPORT_ID = %s
        group by SROK, CODE_VAL
        order by SROK, CODE_VAL
    '''
    cursor = connection.cursor()
    cursor.execute(query, [report.id])
    data = dictfetchall(cursor)

    types = [
        {
            'type': 'Краткосрочный',
            'percent': data[0]['BALANCE']+data[1]['BALANCE']+data[2]['BALANCE'],
            'subs': [{
                'type': "UZS",
                'percent': data[0]['BALANCE']
            }, {
                'type': "USD",
                'percent': data[1]['BALANCE']
            }, {
                'type': "EUR",
                'percent': data[2]['BALANCE']
            }]
        }, {
            'type': 'Долгосрочный',
            'percent': data[3]['BALANCE']+data[4]['BALANCE']+data[5]['BALANCE'],
            'subs': [{
                'type': "UZS",
                'percent': data[3]['BALANCE']
            }, {
                'type': "USD",
                'percent': data[4]['BALANCE']
            }, {
                'type': "EUR",
                'percent': data[5]['BALANCE']
            }, {
                'type': "JPY",
                'percent': data[6]['BALANCE']
            }]
        }]

    result = {"result":{
        "data":types
    }}

    return JsonResponse(result)
