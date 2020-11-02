from django.urls import path
from .views import *

urlpatterns = [
    path('', group_required('Manager CD')(Search.as_view()), name="tax_services_url"),
    path('payer/<str:slug>/', group_required('Manager CD')(PayerDetail.as_view()), name="payer_detail_url"),

    # Cервисы для физ. лицо

    path('payer/<str:slug>/salaries/', group_required('Manager CD')(SalariesList.as_view()), name="salaries_list_url"),
    path('payer/<str:slug>/taxdebts/', group_required('Manager CD')(TaxDebtsList.as_view()), name="taxdebts_list_url"),
    path('payer/<str:slug>/founders/', group_required('Manager CD')(FoundersList.as_view()), name="founders_list_url"),
    path('payer/<str:slug>/dividend/', group_required('Manager CD')(DividendList.as_view()), name="dividend_list_url"),
    path('payer/<str:slug>/objects/', group_required('Manager CD')(ObjectsList.as_view()), name="objects_list_url"),
    path('payer/<str:slug>/leaseds/', group_required('Manager CD')(LeasedsList.as_view()), name="leaseds_list_url"),

    # Cервисы для юр. лицо

    path('payer/<str:slug>/employee/', group_required('Manager CD')(EmployeeList.as_view()), name="employee_list_url"),
    path('payer/<str:slug>/balances/', group_required('Manager CD')(BalancesList.as_view()), name="balances_list_url"),
    path('payer/<str:slug>/finances/', group_required('Manager CD')(FinancesList.as_view()), name="finances_list_url"),
    path('payer/<str:slug>/base_nds/', group_required('Manager CD')(ViewBaseNDS.as_view()), name="base_nds_url"),
    path('payer/<str:slug>/report_enp/', group_required('Manager CD')(ViewReportENP.as_view()), name="report_enp_url"),

    path('payer/<str:slug>/generate_xls/', group_required('Manager CD')(GenerateExcel.as_view()), name="generate_xls_url"),
    path('payer/<str:slug>/generate_word/', group_required('Manager CD')(GenerateWord.as_view()), name="generate_word_url")

]