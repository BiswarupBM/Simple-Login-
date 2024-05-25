"""
Module for handling REST API requests
"""

from urllib.parse import urljoin

import requests


class Client:
    """A REST API client that ensures JSON responses"""

    def __init__(self, base_url: str, verify: bool = True) -> None:
        """
        Constructor

        :param base_url: The API's base URL. All requests made by this
            client are based on this URL
        :type base_url: str
        :param verify: Whether to verify certificates, defaults to True
        :type verify: bool, optional
        """
        self.base_url = base_url
        self.verify = verify

    def __repr__(self) -> str:
        return f"RESTClient('{self.base_url}')"

    def request(
        self,
        method: str,
        endpoint: str = "",
        **kwargs,
    ) -> tuple[bool, dict | str]:
        """
        Make a request to the API

        :param method: The type of HTTP request to make ("GET", etc)
        :type method: str
        :param endpoint: The API endpoint to request, the part that
            comes after the base URL, defaults to ""
        :type endpoint: str, optional
        :param kwargs: Keyword arguments passed directly on to the
            :func:`requests.request` function. Here is where you provide
            JSON, headers, etc.
        :type kwargs: dict

        :return: Whether the request succeeded (status code was < 400),
            and the response as JSON. If the response does not return
            valid JSON, a dict with key "msg" and value of the response
            text is returned
        :rtype: tuple[bool, dict]
        """
        method = method.upper()
        url = urljoin(self.base_url, endpoint)
        response = requests.request(method, url, verify=self.verify, **kwargs)
        success = response.status_code < 400
        try:
            return success, response.json()
        except requests.exceptions.InvalidJSONError:
            return success, {"msg": response.text}

    def delete(self, endpoint: str = "", **kwargs) -> tuple[bool, dict | str]:
        """
        Make a DELETE request to the given endpoint

        See :meth:`request` for param and return info
        """
        return self.request("DELETE", endpoint, **kwargs)

    def get(self, endpoint: str = "", **kwargs) -> tuple[bool, dict | str]:
        """
        Make a GET request to the given endpoint

        See :meth:`request` for param and return info
        """
        return self.request("GET", endpoint, **kwargs)

    def patch(self, endpoint: str = "", **kwargs) -> tuple[bool, dict | str]:
        """
        Make a PATCH request to the given endpoint

        See :meth:`request` for param and return info
        """
        return self.request("PATCH", endpoint, **kwargs)

    def post(self, endpoint: str = "", **kwargs) -> tuple[bool, dict | str]:
        """
        Make a POST request to the given endpoint

        See :meth:`request` for param and return info
        """
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str = "", **kwargs) -> tuple[bool, dict | str]:
        """
        Make a PUT request to the given endpoint

        See :meth:`request` for param and return info
        """
        return self.request("PUT", endpoint, **kwargs)
