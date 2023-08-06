#!/usr/bin/env python

from typing import Optional

import requests


class ManageOrdersServices:
    """A class wrapping ManageOrders' API.

    This class wraps ManageOrders' API.
    """

    def __init__(self, base_url: str, username: str, password: str):
        self._base_url: str = base_url
        self.__username: str = username
        self.__password: str = password

        self.__id_token: Optional[str] = None
        self.__refresh_token: Optional[str] = None
        self.__access_token: Optional[str] = None

    def _make_request(
            self,
            method: str,
            path: str,
            headers: Optional[dict[str, str]] = None,
            data: Optional[dict[str, str]] = None,
            authenticated: bool = True
    ) -> dict[str, str]:
        args = {
            'method': method,
            'url': self._base_url + path,
            'headers': headers or dict()
        }

        if authenticated:
            args['headers']['Authorization'] = self.__id_token

        if data is not None:
            args['json'] = data

        response = requests.request(**args)
        response.raise_for_status()
        return response.json()

    def _update_token(
            self,
    ):
        response = self._make_request(
            method='post',
            path='signin',
            data={'username': self.__username, 'password': self.__password},
            authenticated=False
        )
        self.__id_token = response['id_token']
        self.__refresh_token = response['refresh_token']
        self.__access_token = response['access_token']

