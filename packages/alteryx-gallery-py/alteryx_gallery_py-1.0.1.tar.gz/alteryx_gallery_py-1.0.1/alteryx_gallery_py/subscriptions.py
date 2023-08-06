# Subscriptions.py

import binascii
import hashlib
import hmac
import json
import random
import time
from urllib.parse import quote, urlencode

import requests

class Subscriptions:
    def __init__(self,api_key,client_secret,gallery_url):
        """Class used to call the Alteryx Gallery Subscriptions API"""
        self.__gallery_url = gallery_url[:-1] if gallery_url.endswith("/") else gallery_url
        self.__api_key = api_key
        self.__client_secret = client_secret

    def __get_nonce(self):
        """Retur an 'only use once number' for Oauth."""
        return str(str(random.getrandbits(64)) + str(int(time.time())))

    def __authorize(self, params, url, http_method):
        """Return HMAC-SHA1 sign."""
        params.sort()
        normalized_params = urlencode(params)
        base_string = "&".join((http_method, quote(url,safe="~"), quote(normalized_params,safe="~"))).encode("utf-8")
        sig = hmac.new(bytes("&".join([self.__client_secret,'']),encoding="ascii"), base_string, hashlib.sha1)
        return binascii.b2a_base64(sig.digest())[:-1]

    def __make_get_request(self, url, params):
        """Create an API get request and return result."""
        base_url = self.__gallery_url + url
        params = [(k, v) for k, v in params.items()]
        params = params + [
            ('oauth_consumer_key', self.__api_key),
            ('oauth_nonce', self.__get_nonce()),
            ('oauth_signature_method', "HMAC-SHA1"),
            ('oauth_timestamp', int(time.time())),
            ('oauth_version', '1.0')
        ]
        # retrieve signature
        signature = self.__authorize(params, base_url, "GET")
        params = params + [('oauth_signature',signature)]
        # make request
        r = requests.get(base_url, params, allow_redirects=True)
        return r.content

    def __make_post_request(self, url, data):
        """Create an API post request and return result."""
        base_url = self.__gallery_url + url
        # retrieve signature
        params = [
            ('oauth_consumer_key', self.__api_key),
            ('oauth_nonce', self.__get_nonce()),
            ('oauth_signature_method', "HMAC-SHA1"),
            ('oauth_timestamp', int(time.time())),
            ('oauth_version', '1.0')
        ]
        signature = self.__authorize(params, base_url, "POST")
        params = params + [('oauth_signature', signature)]
        # make request
        r = requests.post(base_url, json=data, params=params)
        return r.content

    def get_workflows(self, **kwargs):
        """Find workflows in a subscription."""
        return json.loads(self.__make_get_request("/api/v1/workflows/subscription/", kwargs))

    def get_questions(self, app_id, **kwargs):
        """Return the questions for the given Alteryx Analytics Application."""
        return json.loads(self.__make_get_request(f"/api/v1/workflows/{app_id}/questions/", kwargs))

    def create_job(self, app_id, **kwargs):
        """Queue an app execution job. Return the ID of the job."""
        return json.loads(self.__make_post_request(f"/api/v1/workflows/{app_id}/jobs/", kwargs))

    def list_jobs(self, app_id, **kwargs):
        """Return the jobs for the given Alteryx Analytics App."""
        return json.loads(self.__make_get_request(f"/api/v1/workflows/{app_id}/jobs/", kwargs))

    def get_job(self, job_id, **kwargs):
        """Retrieve the job and its current state."""
        return json.loads(self.__make_get_request(f"/api/v1/jobs/{job_id}/", kwargs))

    def get_job_output(self, job_id, output_id, **kwargs):
        """Return output for a given job."""
        return self.__make_get_request(f"/api/v1/jobs/{job_id}/output/{output_id}/", kwargs)

    def download_app(self, app_id, **kwargs):
        """Return app that was requested."""
        return self.__make_get_request(f"/api/v1/{app_id}/package/", kwargs)

if __name__ == "__main__":
    pass
