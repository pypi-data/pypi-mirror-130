import requests
import sys
import time


class Bulk:
    GRANT_TYPE = 'password'
    access_token = ''
    instance_url = ''
    auth_url = ''
    DEFAULT_API_VERSION = 'v47.0'
    api_version = ''
    job_url = ''
    JOB_STATUS_CHECK_INTERVAL = 5  # in seconds.
    max_records = 50001

    def __init__(self, client_id, client_secret, username, password, sandbox, api_version=DEFAULT_API_VERSION):
        print('api version :'+api_version)
        self.api_version = api_version
        self.access_token = ''
        self.instance_url = 'https://test.salesforce.com' if sandbox else 'https://login.salesforce.com'
        auth_url = self.instance_url + '/services/oauth2/token?grant_type='
        auth_url = auth_url+'{}&client_id={}&client_secret={}&username={}&password={}'.format(self.GRANT_TYPE,
                                                                                              client_id,
                                                                                              client_secret,
                                                                                              username,
                                                                                              password)
        response = requests.post(auth_url)
        print(response.json())
        if 'access_token' not in response.json():
            print('auth failed')
        else:
            self.access_token = response.json()['access_token']
            self.job_url = response.json()['id']
            self.instance_url = response.json()['instance_url']
            print('authorized')

    def get_auth2_token(self):
        return self.access_token

    def get_auth_url(self):
        print(self.auth_url)

    def get_request_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json'
        }

    def create_query_job(self, soql):
        uri = self.instance_url + \
            "/services/data/{}/jobs/query".format(self.api_version)

        body = {
            'operation': 'query',
            'query': soql
        }

        response = requests.post(
            url=uri, headers=self.get_request_headers(), json=body)
        print(response.json())
        print('job id :{}'.format(response.json()['id']))
        return response.json()['id']

    def get_query_job_status(self, job_id):
        uri = self.instance_url + \
            "/services/data/{}/jobs/query/{}".format(self.api_version, job_id)
        response = requests.get(url=uri, headers=self.get_request_headers())
        return response.json()

    def query(self, soql):
        job_id = self.create_query_job(soql)
        job_status_response = self.wait_for_job_complete(job_id, 'query')
        total_number_of_records = job_status_response['numberRecordsProcessed']
        print('records to be fetched :{}'.format(total_number_of_records))
        query_result = ''
        if(total_number_of_records > self.max_records):
            query_result = self.get_query_results(job_id, self.max_records)
        else:
            query_result = self.get_query_results(job_id)

        print('query completed')
        return query_result

    def get_query_results(self, job_id, max_records=None):
        sf_locator = ''
        result_data = ''
        request_uri = self.instance_url + \
            "/services/data/{}/jobs/query/{}/results".format(
                self.api_version, job_id)
        uri = ''
        if max_records:
            request_uri = request_uri+'?maxRecords={}'.format(max_records)
        uri = request_uri
        response = requests.get(url=uri, headers=self.get_request_headers())
        sf_locator = response.headers['Sforce-Locator']
        result_data = result_data+response.content.decode()
        while sf_locator != 'null':
            uri = request_uri + '&locator={}'.format(sf_locator)
            response = requests.get(
                url=uri, headers=self.get_request_headers())
            result_data = result_data+response.content.decode()
            if('Sforce-Locator' in response.headers):
                sf_locator = response.headers['Sforce-Locator']
            else:
                break

        return result_data

    def create_job(self, object_api_name, operation, external_id_field_name=None):

        request_url = self.instance_url + \
            "/services/data/{}/jobs/ingest".format(self.api_version)

        body = {
            'operation': operation,
            'object': object_api_name,
            'contentType': 'CSV',
            'externalIdFieldName': external_id_field_name
        }

        response = requests.post(
            headers=self.get_request_headers(), url=request_url, json=body)
        print(response.json())
        print('job {} created'.format(response.json()['id']))
        return response.json()['id']

    def upload_data(self, job, data):
        uri = self.instance_url + \
            '/services/data/{}/jobs/ingest/{}/batches/'.format(
                self.api_version, job)
        upload_header = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'text/csv',
            'Accept': 'application/json'
        }
        response = requests.put(headers=upload_header, url=uri, data=data)
        return response

    def upload_complete(self, job):
        uri = self.instance_url + \
            '/services/data/{}/jobs/ingest/{}/'.format(self.api_version, job)
        body = {
            'state': 'UploadComplete'
        }

        response = requests.patch(
            headers=self.get_request_headers(), url=uri, json=body)
        return response

    def get_job_status(self, job):

        uri = self.instance_url + \
            '/services/data/{}/jobs/ingest/{}/'.format(self.api_version, job)
        response = requests.get(headers=self.get_request_headers(), url=uri)
        return response.json()

    def wait_for_job_complete(self, job, operation='insert'):
        print('wait for job complete')
        job_state = ''
        status_response = ''

        if operation == 'query':
            status_response = self.get_query_job_status(job)
        else:
            status_response = self.get_job_status(job)
        job_state = status_response['state']
        print('{}..'.format(job_state))
        while job_state not in ('JobComplete', 'Aborted', 'Failed'):
            time.sleep(self.JOB_STATUS_CHECK_INTERVAL)
            if operation == 'query':
                status_response = self.get_query_job_status(job)
            else:
                status_response = self.get_job_status(job)

            job_state = status_response['state']
            print('{}..'.format(job_state))
            if job_state in ('JobComplete', 'Aborted', 'Failed'):
                break
        return status_response

    def insert(self, object_api_name, data):

        job_id = self.create_job(object_api_name, 'insert')
        self.upload_data(job_id, data)
        self.upload_complete(job_id)
        self.wait_for_job_complete(job_id)

    def upsert(self, object_api_name, external_id_field_name, data):

        job_id = self.create_job(
            object_api_name, 'upsert', external_id_field_name)
        self.upload_data(job_id, data)
        self.upload_complete(job_id)
        self.wait_for_job_complete(job_id)

    def delete(self, object_api_name, data):
        job_id = self.create_job(object_api_name, 'delete')
        self.upload_data(job_id, data)
        self.upload_complete(job_id)
        self.wait_for_job_complete(job_id)

    def get_rejected_records(self, job_id):
        uri = self.instance_url + \
            '/services/data/{}/jobs/ingest/{}/failedResults'.format(
                self.api_version, job_id)

        response = requests.get(headers=self.get_request_headers(), url=uri)
        return response.content.decode()

    def get_success_records(self, job_id):
        uri = self.instance_url + \
            '/services/data/{}/jobs/ingest/{}/successfulResults'.format(
                self.api_version, job_id)

        response = requests.get(headers=self.get_request_headers(), url=uri)
        return response.content.decode()
