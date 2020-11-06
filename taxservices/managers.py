import requests
from django.db import models
from requests.auth import HTTPBasicAuth

from RiskAssessment import settings


class ServicesManager(models.Manager):
    def all(self, service_name, params):
        httpUrl = settings.TAX_BASE_URL + service_name
        basic_auth = HTTPBasicAuth(settings.TAX_USERNAME, settings.TAX_PASSWORD)

        response = requests.post(httpUrl, json=params, auth=basic_auth, proxies=settings.PROXIES)
        if (response.status_code == 200
                and response.json()['success']
                and response.json()['data']):

            response_data = response.json()['data']
            if 'rows' in response_data:
                response_data = response_data['rows']

            result_list = []
            for item in response_data:
                p = self.model(**item)
                result_list.append(p)
            return result_list

        return []

    def get(self, service_name, params):
        httpUrl = settings.TAX_BASE_URL + service_name
        basic_auth = HTTPBasicAuth(settings.TAX_USERNAME, settings.TAX_PASSWORD)

        response = requests.post(httpUrl, json=params, auth=basic_auth, proxies=settings.PROXIES)

        if (response.status_code == 200
                and response.json()['success']
                and response.json()['data']):
            return self.model(**response.json()['data'])

        return None


    def dictall(self, service_name, params):
        httpUrl = settings.TAX_BASE_URL + service_name
        basic_auth = HTTPBasicAuth(settings.TAX_USERNAME, settings.TAX_PASSWORD)

        response = requests.post(httpUrl, json=params, auth=basic_auth)
        if (response.status_code == 200
                and response.json()['success']
                and response.json()['data']):

            response_data = response.json()['data']
            if 'rows' in response_data:
                response_data = response_data['rows']

            result_dict = {}
            for item in response_data:
                result_dict[item['row_no']] = item
            return result_dict

        return {}
