import requests
import base64
from datetime import datetime, timedelta
import json
import time
from requests.structures import CaseInsensitiveDict


class BehavioralCohortsClient(object):
    DEFAULT_ENDPOINT = 'https://amplitude.com/api'

    def __init__(self, api_key, secret, endpoint='', logger=None):
        """copy constructor

        api_key (str): api key of the project.
        secret (str): secret key of the project.
        """
        self.api_key = api_key
        self.secret = secret
        self.endpoint = BehavioralCohortsClient.DEFAULT_ENDPOINT
        self.logger = logger

        if endpoint:
            self.endpoint = endpoint

    def _get_headers(self):
        """Get headers

        Returns:
            dict: dictionary of headers.
        """
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = (
            f'Basic {base64.b64encode(f"{self.api_key}:{self.secret}".encode()).decode()}')
        return headers

    def list_cohorts(self, name=''):
        """Get all cohorts.

        Args:
            name (str): name of cohorts.
        Returns:
            list|dict: response in dictionary format or list of cohorts if name is provided.
        """
        url = f'{self.endpoint}/3/cohorts'
        if self.logger:
            self.logger.debug(f"list_cohorts: {url}")
            self.logger.debug(f"headers:{self._get_headers()}")

        res = requests.get(url, headers=self._get_headers())
        if res.status_code != 200:
            raise Exception(res.text)
        output = res.json()
        if name:
            return [i for i in output['cohorts'] if i['name'] == name]
        return output

    def download_cohort(self, cohort_id, local_path='', timeout=3600):
        """Get cohort by cohort_id

        Args:
            cohort_id (str): cohort id.
            local_path (str[optional]): path for saving cohort file.
                if local_path is not provided, it will save to
                ./cohort_{request_id}.csv
            timeout (int[optional]): timeout in seconds. Method will exit if
                download time exceeds timeout.
        """
        if not local_path:
            local_path = f'cohort_{request_id}.csv'
        url = f'{self.endpoint}/5/cohorts/request/{cohort_id}'

        if self.logger:
            self.logger.debug(f"download_cohort: {url}")
            self.logger.debug(f"headers:{self._get_headers()}")
        res = requests.get(url, headers=self._get_headers())

        if res.status_code != 202:
            raise Exception(res.text)
        request_id = res.json()["request_id"]
        ready = False
        start = datetime.today()
        diff = -1
        while not ready and diff < timeout:
            status_res = requests.get(
                f'{self.endpoint}/5/cohorts/request-status/{request_id}',
                headers=self._get_headers())
            if status_res.status_code not in[200, 202]:
                raise Exception(status_res.text)
            status = status_res.json()

            if 'async_status' in status and status['async_status'] == 'JOB COMPLETED':
                ready = True
            diff = (datetime.today() - start).seconds
            time.sleep(20)
        url = f'{self.endpoint}/5/cohorts/request/{request_id}/file'
        r = requests.get(
            url, allow_redirects=True, headers=self._get_headers())
        open(local_path, 'wb').write(r.content)

    def create_cohorts(self, name, user_ids, owner, id_type='BY_USER_ID'):
        """Create cohorts by user ids.

        Args:
            name (str): name of the cohort.
            user_ids (list): user ids.
            owner (str): owner of the cohort.
            id_type (str[optional]): either BY_USER_ID or BY_AMP_ID
        Returns:
            dict: response.
        """
        payload = {
            'name': name,
            'app_id': self.api_key,
            'id_type': id_type,
            'ids': user_ids,
            'owner': owner,
            "published": True
        }
        url = f'{self.endpoint}/3/cohorts/upload'

        if self.logger:
            self.logger.debug(f"create_cohorts: {url}")
            self.logger.debug(f"headers:{self._get_headers()}")

        res = requests.post(
            url, data=json.dumps(payload), headers=self._get_headers())
        return res

    def update_cohort(self, cohort_id, **kwargs):
        """Update Cohort properties

        Args:
            cohort_id (str): internal cohort id.
            kwargs (dict): properties of the cohort.
        """
        payload = {
            "existing_cohort_id": cohort_id,
            **kwargs
        }
        url = f'{self.endpoint}/3/cohorts/upload'
        if self.logger:
            self.logger.debug(f"update_cohort: {url}")
            self.logger.debug(f"headers:{self._get_headers()}")
        res = requests.post(
            url, data=json.dumps(payload), headers=self._get_headers())
        return res

    def modify_membership(
            self, cohort_id, user_ids, id_type='BY_NAME', operation='ADD'):
        """Add users to cohort.

        Args:
            cohort_id (str): cohort_id.
            user_ids (list): List of ids to add or remove.
            id_type (str): The type of id being sent in the ids field.
                Valid options are: - BY_ID - BY_NAME For User count_group,
                BY_ID is amplitude id and BY_NAME is user id. For any other
                count_group, BY_ID is group id and BY_NAME is group name.
            operation (str): The operation to apply on ids field. Valid options
                are: - ADD - REMOVE
        Returns:
            dict: dictionary response.
        """
        payload = {
            "cohort_id": cohort_id,
            "memberships": [
                {
                    "ids": user_ids,
                    "id_type": id_type,
                    "operation": operation
                }
            ],
            "skip_invalid_ids": True,
        }
        url = f'{self.endpoint}/3/cohorts/membership'

        if self.logger:
            self.logger.debug(f"modify_membership: {url}")
            self.logger.debug(f"headers:{self._get_headers()}")
            self.logger.debug(f"payload:{payload}")

        return requests.post(
            url, data=json.dumps(payload), headers=self._get_headers())
