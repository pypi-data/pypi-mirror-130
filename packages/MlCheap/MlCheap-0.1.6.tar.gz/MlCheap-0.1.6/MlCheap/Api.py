from requests.adapters import HTTPAdapter, Response, Retry
import requests
from typing import Dict, Generator, Generic, List, TypeVar, Union
from .env import *


class Api:
    """Internal Api reference for handling http operations"""

    def __init__(self, api_key, api_instance_url=None, version="v1"):
        if api_key == "" or api_key is None:
            raise Exception("Please provide a valid API Key.")
        self.api_key = api_key
        self._auth = (self.api_key, "")
        self.version = version
        self.base_api_url = api_instance_url if api_instance_url else LABELER_BASE_URL
        self._headers = {
            "Content-Type": "application/json",
            "token": api_key,
        }
        self._headers_data = {
            'Content-Type': 'multipart/form-data',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            "token": api_key,
            'accept-encoding': 'gzip, deflate, br',

        }

    @staticmethod
    def _http_request(
            method,
            url,
            headers=None,
            auth=None,
            params=None,
            body=None,
            files=None,
            data=None,
    ) -> Response:

        https = requests.Session()
        retry_strategy = Retry(
            total=HTTP_TOTAL_RETRIES,
            backoff_factor=HTTP_RETRY_BACKOFF_FACTOR,
            status_forcelist=HTTP_STATUS_FORCE_LIST,
            method_whitelist=HTTP_RETRY_ALLOWED_METHODS,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        https.mount("http://", adapter)
        https.mount("https://", adapter)

        try:
            params = params or {}
            body = body or {}

            res = https.request(
                method=method,
                url=url,
                headers=headers,
                auth=auth,
                params=params,
                json=body,
                files=files,
                data=data,
            )

            return res
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        except Exception as err:
            raise Exception(err) from err

        except Exception as err:
            raise Exception(err) from err

    @staticmethod
    def _raise_on_respose(res: Response):
        try:
            message = res.json().get("error", res.text)
        except ValueError:
            message = res.text

        # exception = ExceptionMap.get(res.status_code, ScaleException)
        raise Exception(message, res.status_code)

    def _api_request(
            self,
            method,
            endpoint,
            headers=None,
            auth=None,
            params=None,
            body=None,
            files=None,
            data=None,
    ):
        """Generic HTTP request method with error handling."""

        url = f"{self.base_api_url}/{self.version}/{endpoint}"
        res = self._http_request(method, url, headers, auth, params, body, files, data)
        # json = None
        # if res.status_code == 200:
        #     json = res.json()
        # else:
        #     self._raise_on_respose(res)
        try:
            json = res.json()
            return json
        except:
            return res

    def get_request(self, endpoint, headers=None, params=None):
        """Generic GET Request Wrapper"""
        _headers = self._headers.copy()
        if headers:
            _headers.update(headers)
        return self._api_request(
            "GET", endpoint, headers=_headers, auth=self._auth, params=params
        )

    def delete_request(self, endpoint, headers=None, params=None):
        """Generic GET Request Wrapper"""
        _headers = self._headers.copy()
        if headers:
            _headers.update(headers)
        return self._api_request(
            "DELETE", endpoint, headers=_headers, auth=self._auth, params=params
        )

    def post_request(self, endpoint, headers=None, body=None, files=None, data=None):
        """Generic POST Request Wrapper"""
        if headers is None:
            headers = dict()
        if files is None:
            _headers = self._headers.copy()
        else:
            _headers = self._headers_data.copy()
        if headers:
            _headers.update(headers)
        return self._api_request(
            "POST",
            endpoint,
            headers=_headers,
            auth=self._auth,
            body=body,
            files=files,
            data=data,
        )

    def put_request(self, endpoint, headers=None, body=None, files=None, data=None):
        """Generic PUT Request Wrapper"""
        if headers is None:
            headers = dict()
        if files is None:
            _headers = self._headers.copy()
        else:
            _headers = self._headers_data.copy()
        if headers:
            _headers.update(headers)
        return self._api_request(
            "PUT",
            endpoint,
            headers=_headers,
            auth=self._auth,
            body=body,
            files=files,
            data=data,
        )
