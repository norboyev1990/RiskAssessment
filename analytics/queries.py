class Query():

    @staticmethod
    def get_statuses():
        return '''
            select
                   Status,
                   MAX(cl.name) as Title,
                   sum(totalloan) as Balance,
                   sum(totalloan)/max(t.totals) Percent,
                   count(*) as Counts,
                   sum(totalreserve) as Reserve,
                   sum(totalneeded) as Needed
            from (
                select
                   sum(vsego_zadoljennost) as totalloan,
                   sum(ostatok_rezerv) as totalreserve,
                   client_status(nvl(max(days), 0),nvl(max(arrear_days),0),
                        sum(ostatok_sudeb),sum(ostatok_vneb_prosr),sum(ostatok_peresm)) as status,
                   get_reserve(
                        client_status(nvl(max(days), 0),nvl(max(arrear_days),0),
                        sum(ostatok_sudeb),sum(ostatok_vneb_prosr),sum(ostatok_peresm)),
                        sum(vsego_zadoljennost), sum(ostatok_rezerv)) as totalneeded
                from credits
                where report_id = %s
                group by unique_code) a
            left join credits_classes cl on cl.CODE = a.status,
            (select sum(vsego_zadoljennost) totals from credits_reportdata where report_id=%s) t
            group by status
            order by status desc
        '''

    @staticmethod
    def find_clients_by_status():
        return '''
            select 
                UNIQUE_CODE as ClientID,
                MAX(NAME_CLIENT) as ClientName,
                sum(VSEGO_ZADOLJENNOST) as TotalLoans,
                client_status(nvl(max(days), 0),nvl(max(arrear_days),0),
                sum(ostatok_sudeb),sum(ostatok_vneb_prosr),sum(ostatok_peresm)) as Status, 
                count(*) as CountLoans
            from CREDITS cr
            where REPORT_ID = %s
            group by UNIQUE_CODE
            having client_status(nvl(max(days), 0),nvl(max(arrear_days),0),
                sum(ostatok_sudeb),sum(ostatok_vneb_prosr),sum(ostatok_peresm)) = %s
        '''