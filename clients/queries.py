class Query():

    @staticmethod
    def findClients():
        return '''
            SELECT 
                UNIQUE_CODE AS ClientID,
                MAX(NAME_CLIENT) AS ClientName,
                MAX(SUBJECT) AS Subject,
                MAX(CLIENT_TYPE)  AS ClientType,
                MAX(CB.NAME) AS BranchName,
                NVL(SUM(VSEGO_ZADOLJENNOST),0) AS TotalLoans,
                NVL(SUM(OSTATOK_REZERV),0) AS TotalReserve,
                MAX(ADRESS_CLIENT) AS Address,
                CLIENT_STATUS_2(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                    sum(ostatok_vneb_prosr),sum(ostatok_peresm), UNIQUE_CODE) AS ClientStatus,
                NVL(GET_RESERVE(CLIENT_STATUS_2(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                    sum(ostatok_vneb_prosr),sum(ostatok_peresm),UNIQUE_CODE), 
                    SUM(VSEGO_ZADOLJENNOST), SUM(OSTATOK_REZERV)),0) AS NeededReserve,
                NVL(SUM(OSTATOK_SUDEB),0) AS SummaSudeb,
                NVL(SUM(OSTATOK_VNEB_PROSR),0) AS SummaVneb,
                NVL(SUM(OSTATOK_PERESM),0) AS SummaPeresm,
                NVL(SUM(OSTATOK_PROSR),0) as TotalOverdue,
                MAX(DAYS) as OverdueDays,
                NVL(SUM(OSTATOK_NACH_PROSR_PRCNT),0) as NachPercent,
                MAX(ARREAR_DAYS) as ArrearDays
            from credits
            left join CREDITS_BRANCH CB on CREDITS.MFO = CB.CODE
            WHERE REPORT_id = %s and MFO like %s and CLIENT_TYPE LIKE %s
            GROUP BY UNIQUE_CODE
            having CLIENT_STATUS_2(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                    sum(ostatok_vneb_prosr),sum(ostatok_peresm), UNIQUE_CODE) like %s
                and (LOWER(MAX(NAME_CLIENT)) like LOWER(%s) or UNIQUE_CODE like %s)
             
        '''

    @staticmethod
    def findClientByID():
        return '''
            SELECT ClientID,
                MAX(ClientName) ClientName,
                MAX(ClientType) ClientType,
                MAX(CLIENT_TYPE) Subject,
                MAX(INN_PASSPORT) Passport,
                COUNT(*) CountLoans, 
                SUM(VSEGO_ZADOLJENNOST)  AS TotalLoans,
                MAX(substr(ADRESS_CLIENT, 1, pos-1)) AS Address,
                MAX(substr(ADRESS_CLIENT, pos+1)) AS Phone,
                CLIENT_STATUS(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                sum(ostatok_vneb_prosr),sum(ostatok_peresm)) AS Status,
                GET_RESERVE(CLIENT_STATUS(nvl(max(days), 0),nvl(max(arrear_days),0),sum(ostatok_sudeb),
                sum(ostatok_vneb_prosr),sum(ostatok_peresm)), 
                SUM(VSEGO_ZADOLJENNOST), SUM(OSTATOK_REZERV)) AS Reserve,
                NVL(SUM(OSTATOK_REZERV), 0) AS OstatokReserve
            FROM (
                SELECT 
                    UNIQUE_CODE AS ClientID,
                    NAME_CLIENT AS ClientName,
                    CLIENT_TYPE,
                    INN_PASSPORT,
                    CASE SUBJECT 
                        WHEN TRANSLATE('ЮЛ' USING nchar_cs) THEN 'ЮРИДИЧЕСКОЕ ЛИЦА'
                        WHEN TRANSLATE('ИП' USING nchar_cs) THEN 'ИНДИВИДУАЛНОЕ ПРЕДПРИЯТИЯ'
                        ELSE 'ФИЗИЧЕСКОЕ ЛИЦА' END AS ClientType,
                    VSEGO_ZADOLJENNOST,
                    DAYS,
                    ARREAR_DAYS,
                    OSTATOK_SUDEB,
                    OSTATOK_VNEB_PROSR,
                    OSTATOK_PERESM,
                    OSTATOK_REZERV,
                    CASE instr(ADRESS_CLIENT,',') WHEN 0 THEN 999 
                    ELSE instr(ADRESS_CLIENT,',') END  AS POS,
                    ADRESS_CLIENT
                from credits
                WHERE REPORT_id = %(report_id)s
                ) T
            WHERE ClientID = %(unique_code)s
            GROUP BY ClientID
        '''

    @staticmethod
    def findCredits():
        return '''
            select
                UNIQUE_CODE as UniqueCode,
                CODE_CONTRACT as CodeContract,
                DATE_DOGOVOR as DateContract,
                SUM_DOG_EKV as SummaContract,
                CREDIT_PROCENT as CreditPercent,
                DATE_POGASH as DateClosed,
                VSEGO_ZADOLJENNOST as BalanceCredit,
                VID_KREDITOVANIYA as TypeCredit,
                PURPOSE_CREDIT as PurposeCredit,
                NVL(OSTATOK_NACH_PROSR_PRCNT,0) as NachPercent,
                NVL(OSTATOK_PROSR,0) as SummaOverdue,
                NVL(DAYS,0) as DaysOverdue,
                NVL(ARREAR_DAYS,0) as DaysOverduePercent,
                NVL(OSTATOK_SUDEB,0) as SummaSudeb,
                NVL(OSTATOK_VNEB_PROSR,0) as SummaVneb,
                NVL(OSTATOK_PERESM,0) as SummaPeresm,
                NVL(OSTATOK_REZERV,0) as OstatokReserve,
                GET_RESERVE(%(client_status)s, VSEGO_ZADOLJENNOST, OSTATOK_REZERV) as Reserve
            from CREDITS
            where UNIQUE_CODE = %(unique_code)s 
                and REPORT_ID = %(report_id)s
        '''


    @staticmethod
    def findContracts():
        return '''
            select
                CP.ID as id,
                DATE_POGASH as DatePogash,
                PROGNOZ_POGASH as PrognozPogash,
                OSTATOK_NACH_PRCNT as OstatokPercent,
                CY.NAME as CurrencyName
            from  CREDITS_PAYMENTS CP
            left join CREDITS_CURRENCY CY on CY.CODE = CP.CODE_VAL
            where UNIQUE_NIKI = %s
            order by DATE_POGASH
        '''