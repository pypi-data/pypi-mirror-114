from __future__ import annotations
from typing import Optional, Union, Dict, List, Any

import datetime as dt
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin

try:
    from ._utils import Decorators
except ImportError:
    from _utils import Decorators

class Client:

    def __init__(
        self,
        url: str,
        apikey: str,
        session: Optional[requests.Session] = None,
        **kwargs
    ) -> None:
        """ Create a conection with Certronic API using recived parameters

        Args:
            url (str): Full url to Certronic API
            apikey (str): API-Key provided by Certronic
            session (Optional[requests.Session], optional):
                Optional requests session.
                Defaults to None
        """

        self.client_url = urlparse(url)
        self.client_fullpath = url
        self.apikey = apikey
        self.session = session
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json",
            "Accept-Encoding": "gzip,deflate",
            "apikey": apikey
        }


    def __str__(self) -> str:
        return f'Certronic Client for {self.client_fullpath}'

    def __repr__(self) -> str:
        return "{}(url='{}', apikey='{}', session={})".format(
            self.__class__.__name__,
            self.client_fullpath,
            self.apikey,
            self.session
        )

    def __enter__(self, *args, **kwargs) -> Client:
        self.start_session()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.close_session()

    def start_session(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def close_session(self):
        self.session.close()

    @Decorators.ensure_session
    def get(
        self,
        path: str,
        params: dict = None,
        **kwargs
    ) -> Union[Dict, List, requests.Response]:
        """ Sends a GET request to Certronic url

        Args:
            path (str): path to add to client full path URL
            params (dict, optional):
                Data to send in the query parameters of the request.
                Defaults to None.

        Raises:
            ConnectionError: If response status not in range(200, 300)

        Returns:
            Union[Dict, List]: JSON Response if request is not stream.
            requests.Response: If request is stream.
        """

        # prepare url
        url = urljoin(self.client_fullpath, path)

        # consulting certronic
        response = self.session.get(url=url, params=params, **kwargs)

        # raise if was an error
        if response.status_code not in range(200, 300):
            raise ConnectionError({
                'status': response.status_code,
                'detail': response.text
            })

        # if request is stream type, return all response
        if kwargs.get("stream"):
            return response

        # return json response
        return response.json()

    def bulk_get(self, path: str, params: dict = {}, \
            together: tuple = tuple(), max_workers: int = 50, \
            response_to_dict: bool = False, **kwargs):
        """
        UNUSED

        Sends multiple GET requests to Certronic url simultaneously.
        
        :param path: path to add to client full path URL.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param together: Iterator of dicts to get together. E.g. 
            [{
                'page': 1
            },{
                'page': 2
            }]
        :max_workers: int to specify max workers number to run simultaneously.
        :response_to_dict: bool to group responses if there are dict objects.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`dict` object
        :rtype: dict
        """

        # structures prepare
        responses = {} if response_to_dict else []
        processes = []
        params_ = params

        # create executor context
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # processes prepare
            for e_ in together:
                params_.update(e_)
                processes.append(
                    executor.submit(
                        self.get,
                        path=path,
                        params=params_,
                        **kwargs
                    )
                )

            # execute and put result in out structure
            if response_to_dict:
                [responses.update(r.result()) for r in as_completed(processes)]
            else:
                [responses.append(r.result()) for r in as_completed(processes)]

            # close executor
            executor.shutdown(wait=True)

        # return responses
        # list of pages result
        return responses

    @Decorators.ensure_session
    def post(
        self,
        path: str,
        params: dict = None,
        data: dict = None,
        json: dict = None,
        **kwargs
    ) -> Union[Dict, List]:
        """ Sends a POST request to Certronic url

        Args:
            path (str): Path to add to client full path URL
            params (dict, optional):
                Data to send in the query parameters of the request.
                Defaults to None.
            data (dict, optional):
                Form Data to send in the request body.
                Defaults to None.
            json (dict, optional):
                JSON Data to send in the request body.
                Defaults to None.

        Raises:
            ConnectionError: If response status not in range(200, 300)

        Returns:
            Union[Dict, List]: JSON Response
        """

        # prepare url
        url = urljoin(self.client_fullpath, path)

        # consulting certronic
        response = self.session.post(
            url=url,
            params=params,
            data=data,
            json=json,
            **kwargs
        )

        # raise if was an error
        if response.status_code not in range(200, 300):
            raise ConnectionError({
                'status': response.status_code,
                'detail': response.text
            })

        # return json response
        return response.json()

    def get_employees(
        self,
        page: Optional[int] = 1,
        pageSize: Optional[int] = 50,
        updatedFrom: Optional[Union[dt.datetime, str]] = None,
        includeDocuments: bool = None,
        customFields: Optional[List[Union[int, str]]] = None,
        **kwargs
    ) -> Union[Dict, List]:
        """ Get employees from Certronic API with client.get()

        Args:
            page (Optional[int], optional): Page number. Defaults to 1.
            pageSize (Optional[int], optional):
                Max results per page.
                Defaults to 50.
            updatedFrom (Optional[Union[dt.datetime, str]], optional):
                Datetime to apply as start filter of employees.
                Defaults to None.
            includeDocuments (bool, optional):
                Boolean to get documents detail.
                Defaults to None.
            customFields (Optional[List[Union[int, str]]], optional):
                List of Custom fields to get from employe.
                Defaults to None.

        Returns:
            Union[Dict, List]: List of JSON employees obtained from Certronic
        """    

        # path prepare
        path = 'employees.php'

        # datetime to str
        if isinstance(updatedFrom, dt.datetime):
            updatedFrom = updatedFrom.strftime("%Y-%m-%d %H:%M:%S")

        # foce None if is False
        if not includeDocuments:
            includeDocuments = None

        # parameters prepare
        params = {
            "updatedFrom": updatedFrom,
            "includeDocuments": includeDocuments,
            "customFields": customFields,
            "pageSize": pageSize,
            "page": page
        }

        # request.get -> json
        return self.get(path=path, params=params, **kwargs)


    def post_clockings(
        self,
        clockings: List[Dict[str, Any]],
        **kwargs
    ) -> Union[Dict, List]:
        """ Send clockings to Certronic API

        Args:
            clockings (List[Dict[str, Any]]):
                List of clockings. Must be structure like:
                clockings = [{
                    "id": 3456,
                    "center": "BA01",
                    "ss": "12-12345678-9",
                    "action": "in/out",
                    "datetime": "2020-02-11T12:39:00.000Z"
                }]

        Returns:
            Union[Dict, List]: JSON Certronic API response.
        """        

        # path prepare
        path = 'clocking.php'

        # return response
        return self.post(path=path, json={"clockings": clockings}, **kwargs)

