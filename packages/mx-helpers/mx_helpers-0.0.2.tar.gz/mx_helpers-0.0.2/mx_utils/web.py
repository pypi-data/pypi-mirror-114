# -*- coding: utf-8 -*-
# @Time    : 2021/7/7 10:50 上午
# @Author  : X.Lin
# @Email   : ****
# @File    : web.py
# @Software: PyCharm
# @Desc    :

import requests
from urllib.parse import urlparse

from . import logger


class HttpRequests(object):
    """ Http 请求类封装
    """

    _SESSIONS = {}  # {"domain-name": session, ... }

    @classmethod
    def _fetch(cls, method, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        session = cls._get_session(url)
        try:
            if method == "GET":
                response = session.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
            elif method == "POST":
                response = session.post(url, params=params, data=body, json=data, headers=headers,
                                              timeout=timeout, **kwargs)
            elif method == "PUT":
                response = session.put(url, params=params, data=body, json=data, headers=headers,
                                             timeout=timeout, **kwargs)
            elif method == "DELETE":
                response = session.delete(url, params=params, data=body, json=data, headers=headers,
                                                timeout=timeout, **kwargs)
            else:
                error = "http method error!"
                return None, None, error
        except Exception as e:
            logger.error("method: %s, url: %s, headers: %s, params: %s, body: %s, message: %s, error: %s",
                         method, url, headers, params, body, data, e, exc_info=True)
            return None, None, e
        code = response.status_code
        if code not in (200, 201, 202, 203, 204, 205, 206):
            text = response.text()
            logger.error("method: %s, url: %s, headers: %s, params: %s, body: %s, message: %s, code: %d, result: %s",
                         method, url, headers, params, body, data, code, text, exc_info=True)
            return code, None, text
        try:
            result = response.json()
        except:
            result = response.text()
            logger.warn(
                "response message is not json format!, method: %s, url: %s, headers: %s, params: %s, body: %s, message: %s, code: %d, result: %s",
                method, url, headers, params, body, data, code, result, exc_info=True)
        return code, result, None

    @classmethod
    def get(cls, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        """ HTTP GET
        """
        result = cls._fetch("GET", url, params, body, data, headers, timeout, **kwargs)
        return result

    @classmethod
    def post(cls, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        """ HTTP POST
        """
        result = cls._fetch("POST", url, params, body, data, headers, timeout, **kwargs)
        return result

    @classmethod
    def delete(cls, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        """ HTTP DELETE
        """
        result = cls._fetch("DELETE", url, params, body, data, headers, timeout, **kwargs)
        return result

    @classmethod
    def put(cls, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        """ HTTP PUT
        """
        result = cls._fetch("PUT", url, params, body, data, headers, timeout, **kwargs)
        return result

    @classmethod
    def _get_session(cls, url):
        """ Get the connection session for url's domain, if no session, create a new.

        Args:
            url: HTTP request url.

        Returns:
            session: HTTP request session.
        """
        parsed_url = urlparse(url)
        key = parsed_url.netloc or parsed_url.hostname
        if key not in cls._SESSIONS:
            session = requests.Session()
            cls._SESSIONS[key] = session
        return cls._SESSIONS[key]