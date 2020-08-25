class Query():
    @staticmethod
    def krp_by_month():
        return '''
            select 
                 sum(c.vsego_zadoljennost)/1000000000 total
            from credits c
            left join credits_listreports l on l.id = c.report_id
            where l.report_year = %s
            group by l.report_month
            order by l.report_month
        '''

    @staticmethod
    def npl_by_month():
        return '''
            select sum(balance)/1000000000 total 
            from (
                select report_id, sum(vsego_zadoljennost) as balance
                from credits c
                group by  report_id, unique_code
                having 
                    nvl(max(days), 0) > 90 or nvl(max(arrear_days),0) > 90
                    or sum(ostatok_sudeb) is not null
                    or sum(ostatok_vneb_prosr) is not null) a
            left join credits_listreports l on l.id = a.report_id
            where l.report_year = %s
            group by l.report_month
            order by l.report_month
        '''

    @staticmethod
    def tox_by_month():
        return '''
            select l.report_month, sum(balance) 
            from (
                select report_id, sum(vsego_zadoljennost) as balance
                from credits c
                group by  report_id, unique_code
                having 
                    nvl(max(days), 0) <= 90 and nvl(max(arrear_days),0) <= 90
                    and sum(ostatok_sudeb) is null
                    and sum(ostatok_vneb_prosr) is null
                    and sum(ostatok_peresm) is not null) a
            left join credits_listreports l on l.id = a.report_id
            where l.report_year = %s
            group by l.report_month
            order by l.report_month;
        '''

    @staticmethod
    def prs_by_month():
        return '''
            select 
                 sum(c.ostatok_prosr)/1000000000 total
            from credits c
            left join credits_listreports l on l.id = c.report_id
            where l.report_year = %s
            group by l.report_month
            order by l.report_month
        '''

    @staticmethod
    def res_by_month():
        return '''
            select 
                 sum(c.ostatok_rezerv)/1000000000 total
            from credits c
            left join credits_listreports l on l.id = c.report_id
            where l.report_year = %s
            group by l.report_month
            order by l.report_month
        '''

    @staticmethod
    def full_by_month():
        return '''
            select ROWNUM as id, x.* from (
                select 
                    'kpr' as title,
                     l.report_month,
                     sum(c.vsego_zadoljennost)/1000000000 total,
                     sum(c.ostatok_prosr)/1000000000 prosr,
                     sum(c.ostatok_rezerv)/1000000000 reserv
                from credits c
                left join credits_listreports l on l.id = c.report_id
                where l.report_year = 2020
                group by l.report_month
                union all
                select 'npl' as title, l.report_month, sum(balance)/1000000000 total, null, null
                from (
                    select report_id, sum(vsego_zadoljennost) as balance
                    from credits c
                    group by  report_id, unique_code
                    having
                        nvl(max(days), 0) > 90 or nvl(max(arrear_days),0) > 90
                        or sum(ostatok_sudeb) is not null
                        or sum(ostatok_vneb_prosr) is not null) a
                left join credits_listreports l on l.id = a.report_id
                where l.report_year = 2020
                group by l.report_month
                union all
                select 'tox' as title, l.report_month, sum(balance)/1000000000, null, null
                from (
                    select report_id, sum(vsego_zadoljennost) as balance
                    from credits c
                    group by  report_id, unique_code
                    having
                        nvl(max(days), 0) <= 90 and nvl(max(arrear_days),0) <= 90
                        and sum(ostatok_sudeb) is null
                        and sum(ostatok_vneb_prosr) is null
                        and sum(ostatok_peresm) is not null) a
                left join credits_listreports l on l.id = a.report_id
                where l.report_year = 2020
                group by l.report_month) x
            order by title, report_month
        '''