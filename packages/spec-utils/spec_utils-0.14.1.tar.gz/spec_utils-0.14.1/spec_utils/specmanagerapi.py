from __future__ import annotations
from typing import Optional, Union, Dict, List, Any

import datetime as dt
import requests
from urllib.parse import urlparse, urlencode, urljoin, quote

try:
    from ._utils import Decorators
except ImportError:
    from _utils import Decorators

__specmanager__ = "5.0.0r17013"


class Client:
    
    def __init__(
        self,
        url: str,
        apikey: str,
        session: Optional[requests.Session] = None,
        **kwargs
    ) -> None:
        """ Create a connector for SPECManager API using recived parameters.

        Args:
            url (str): Full url to SPECManager API
            apikey (str): API-Key provided by SPEC SA
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

    def __str__(self):
        return f'SPECManager Client for {self.client_fullpath}'

    def __repr__(self):
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
        """ Sends a GET request to SPEC Manager API.

        Args:
            path (str): Path to add to client full path URL
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

    @Decorators.ensure_session
    def post(
        self,
        path: str,
        params: dict = None,
        data: dict = None,
        json: dict = None,
        **kwargs
    ) -> Union[Dict, List]:
        """ Sends a POST request to SPEC Manager url.

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
            params=urlencode(params, quote_via=quote),
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

    def get_clockings(
        self,
        _type: str,
        _from: Union[dt.datetime, str],
        _to: Union[dt.datetime, str],
        fromHistory: Optional[bool] = False,
        employeeDetail: Optional[bool] = False,
        employeeData: Optional[List[Union[int, str]]] = [],
        pageSize: Optional[int] = 20,
        page: Optional[int] = 1,
        **kwargs
    ) -> Union[Dict, List]:
        """ Get clockings from SM API with self.get() passing _type and 
            parameters recived.

        Args:
            _type (str): Employee type. Eg. 'own', 'contractor', etc.
            _from (Union[dt.datetime, str]):
                Datetime to apply as start filter of clockings.
            _to (Union[dt.datetime, str]):
                Datetime to apply as end filter of clockings.
            fromHistory (Optional[bool], optional):
                True or False to get clockings from HISTORICO.
                Defaults to False.
            employeeDetail (Optional[bool], optional):
                True to get serialized employee.
                Defaults to False.
            employeeData (Optional[List[Union[int, str]]], optional):
                List of Optional Data of employee to get from SM.
                Defaults to [].
            pageSize (Optional[int], optional):
                Max results per page.
                Defaults to 20.
            page (Optional[int], optional):
                Page number.
                Defaults to 1.

        Returns:
            Union[Dict, List]: List of match clockings
        """
        
        # path prepare
        path = f'clockings/{_type}'

        # datetime to str
        if isinstance(_from, dt.datetime):
            _from = _from.strftime("%Y%m%d%H%M%S")

        if isinstance(_to, dt.datetime):
            _to = _to.strftime("%Y%m%d%H%M%S")

        # parameters prepare
        params = {
            "from": _from,
            "to": _to,
            "fromHistory": fromHistory,
            "employeeDetail": employeeDetail,
            "pageSize": pageSize,
            "page": page
        }

        # append data
        if employeeData:
            params["employeeData"] = ','.join([str(e) for e in employeeData])

        # request.get -> json
        return self.get(path=path, params=params, **kwargs)
        

    def get_clockings_contractor(
        self,
        _from: Union[dt.datetime, str],
        _to: Union[dt.datetime, str],
        fromHistory: Optional[bool] = False,
        employeeDetail: Optional[bool] = False,
        employeeData: Optional[List[Union[int, str]]] = [],
        pageSize: Optional[int] = 20,
        page: Optional[int] = 1,
        **kwargs
    ) -> Union[Dict, List]:
        """ Get contractor clockings from SM API with self.get_clockings() and 
            recived parameters.

        Args:
            _from (Union[dt.datetime, str]):
                Datetime to apply as start filter of clockings.
            _to (Union[dt.datetime, str]):
                Datetime to apply as end filter of clockings.
            fromHistory (Optional[bool], optional):
                True or False to get clockings from HISTORICO.
                Defaults to False.
            employeeDetail (Optional[bool], optional):
                True to get serialized employee.
                Defaults to False.
            employeeData (Optional[List[Union[int, str]]], optional):
                List of Optional Data of employee to get from SM.
                Defaults to [].
            pageSize (Optional[int], optional):
                Max results per page.
                Defaults to 20.
            page (Optional[int], optional):
                Page number.
                Defaults to 1.

        Returns:
            Union[Dict, List]: List of match clockings
        """

        # parameters prepare
        params = {
            "_type": "contractor",
            "_from": _from,
            "_to": _to,
            "fromHistory": fromHistory,
            "employeeDetail": employeeDetail,
            "pageSize": pageSize,
            "page": page,
            "employeeData": employeeData
        }

        # request.get -> json
        return self.get_clockings(**params, **kwargs)

    def post_employee(
        self,
        _type: str,
        code: int,
        nif: str,
        lastName: str,
        firstName: str,
        companyCode: str,
        companyName: str,
        comment: Optional[str] = None,
        centers: Optional[List[Dict[str, Any]]] = [],
        optionalData: Optional[List[Dict[str, Any]]] = [],
        isActive: Optional[bool] = None,
        card: Optional[str] = None,
        cardRequired: Optional[bool] = False,
        **kwargs
    ) -> Union[Dict, List]:
        """ Send employee to SM API with self.post() passing _type and 
            recived parameters.

        Args:
            _type (str): 
                Employee type enpoint to add in POST /employees/{_type} SM API.
                E.g. 'contractor', 'encae', 'own', etc
            code (int): Employee code field.
            nif (str): Employee DNI field.
            lastName (str): Employee lastName field.
            firstName (str): Employee firstName field.
            companyCode (str): Company code (nif).
            companyName (str): Company name.
            comment (Optional[str], optional):
                Comment to assign at current employee.
                Defaults to None.
            centers (Optional[List[Dict[str, Any]]], optional):
                List of dict with 'center' and 'dueDate' keys. E.g.
                    [{
                        "center": "AR",
                        "dueDate": dt.date(2020, 12, 31)
                    }, {
                        "center": "ES",
                        "dueDate": dt.date(2021, 12, 31)
                    }]
                Defaults to [].
            optionalData (Optional[List[Dict[str, Any]]], optional):
                list of dict with opcionals data to assign. E.g.
                    [{
                        "level": 1,
                        "value": "some-value-to-data-1",
                    },{
                        "level": 8,
                        "value": "some-value-to-data-8",
                    }]
                Defaults to [].
            isActive (Optional[bool], optional):
                Boolean to high/down employee.
                Defaults to None.
            card (Optional[str], optional):
                Card number to assign to employee.
                Empty or None to clean. -requires cardRequired = True-.
                Defaults to None.
            cardRequired (Optional[bool], optional):
                Boolean to set if empty card parameter clean or do nothing.
                Defaults to False.

        Returns:
            Union[Dict, List]: Import result
        """

        # path prepare
        path = f'employees/{_type}'

        # json prepare
        params = {
            "code": code,
            "nif": nif,
            "lastName": lastName,
            "firstName": firstName,
            "comment": comment,
            "isActive": isActive,
            "companyCode": companyCode,
            "companyName": companyName,
            "card": card,
            "cardRequired": cardRequired
        }

        # centers parse
        if centers:
            params["centers"] = ','.join([
                f'{_c.get("center")}:{_c.get("dueDate").strftime("%Y%m%d")}' \
                    for _c in centers
            ])

        if optionalData:
            params["optionalData"] = ','.join([
                f'{_od.get("level")}:{_od.get("value")}'for _od in optionalData
            ])

        # request.get -> json
        return self.post(path=path, params=params, **kwargs)

    def post_employees(
        self,
        employeeData: Union[List[Dict[str, Any]], Dict[str, Any]],
        **kwargs
    ) -> Union[Dict, List]:
        """ Send employee to SM API with self.post_employee() passing 
            employeeData.

        Args:
            employeeData (Union[List[Dict[str, Any]], Dict[str, Any]]):
                Dict or list with params of self.post_employee().
                To get more info of employeeData structure, check help for 
                post_employee() method.

        Returns:
            Union[Dict, List]: Import result
        """

        # check items
        if isinstance(employeeData, list):
            # empty response
            response = {}
            
            for employee in employeeData:
                # rewrite if OK, raise if error
                response = self.post_employee(**employee, **kwargs)

            # return last response (or raise before)
            return response

        # 1 dict employee by default
        return self.post_employee(**employeeData, **kwargs)

    def post_employee_encae(
        self,
        code: int,
        nif: str,
        lastName: str,
        firstName: str,
        companyCode: str,
        companyName: str,
        centers: list = [],
        optionalData: list = [],
        **kwargs
    ) -> Union[Dict, List]:
        """
        -- DONT USE
        Send encae employee to SM API with self.post_employee() and 
        recived parameters.

        :param code: int with employee code
        :param nif: str with employee DNI field
        :param ss: str with employee SS field
        :param lastName: str with employee lastName field
        :param firstName: str with employee firstName field
        :param companyCode: str with company code (nif)
        :param companyName: str with company name
        :param centers: list of dict with 'center' and 'dueDate' keys. E.g.
            [{
                "center": "AR",
                "dueDate": dt.date(2020, 12, 31)
            }, {
                "center": "ES",
                "dueDate": dt.date(2021, 12, 31)
            }]
        :param optionalData: list of dict with opcionals data to assign. E.g.
            [{
                "level": 1,
                "value": "some-value-to-data-1",
            },{
                "level": 8,
                "value": "some-value-to-data-8",
            }]
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`json` object
        :rtype: json
        """

        # json prepare
        query = {
            "_type": "encae",
            "code": code,
            "nif": nif,
            "lastName": lastName,
            "firstName": firstName,
            "companyCode": companyCode,
            "companyName": companyName,
            "centers": centers,
            "optionalData": optionalData
        }

        # request.get -> json
        return self.post_employee(**query, **kwargs)

