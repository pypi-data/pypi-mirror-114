import attr
from typing import Dict

from http import HTTPStatus

import requests
from logbook import Logger

logger = Logger(__name__)


@attr.s
class GeniApi(object):
    geni_base_url = attr.ib(type=str)
    geni_username = attr.ib(type=str)
    geni_password = attr.ib(type=str)

    headers = attr.ib(type=Dict, init=False)

    session = attr.ib(type=requests.Session, init=False)
    token = attr.ib(type=str, init=False)

    @staticmethod
    def fetch_login_token(login_url: str, session: requests.Session, payload: str) -> str:
        """
        :param login_url: <str>
        :param session: <requests object> maintains session information to prevent user from being logged out.
        :param payload: <str> defined in fetch_payload
        :return: <str> token. Auth token needed for subsequent requests
        """
        logger.debug(f'login request to url: {login_url}')
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        response = session.post(login_url, data=payload, headers=headers)
        token = response.headers.get('Set-Authorization', None)
        if not token:
            raise ValueError(f"Incorrect username and password provided for {login_url.split('aut')[0]} \n"
                             f"Geni Error message: {response.text}")

        token = response.headers['Set-Authorization']
        return token

    @staticmethod
    def get_login_payload(user: str, password: str) -> str:
        return f'{{"@dto":"Account","username":"{user}","password":"{password}"}}'

    def generate_headers(self) -> dict:
        login_url = f"{self.geni_base_url}/auth/login"
        with requests.Session() as session:
            self.session = session
            self.token = self.fetch_login_token(login_url=login_url,
                                                session=session,
                                                payload=self.get_login_payload(self.geni_username, self.geni_password))
            headers = {
                'content-type': "application/json",
                'authorization': self.token,
                'cache-control': "no-cache",
            }
        self.headers = headers

    def make_http_request(self, url: str, params=None) -> dict:
        """
        Makes http request to url provided.  If returned value indicates that token has expired, login and resent
        http prequest
        :param url: <str> endpoint used for http request
        :param params: <dict> params used for http request (depends on url)
        :return:
        """
        logger.debug(f'get request to url: {url}')
        if not hasattr(self, 'headers') or self.headers is None:
            self.generate_headers()
        my_request = self.session.get(url, headers=self.headers, params=params)
        if my_request.status_code == HTTPStatus.UNAUTHORIZED:
            self.generate_headers()
            my_request = self.session.get(url, headers=self.headers, params=params)

        return my_request.json()
