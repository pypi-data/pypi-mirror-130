import re
import json
from collections import namedtuple
from attrdict import AttrDict
from typing import List, Union, Callable


Request = namedtuple("Request", ["query_params", "data", "json", "headers"])


class Response:
    def __init__(self, method, text=None, data=None, status_code=200, headers=None):
        self.status_code = status_code
        self.request = AttrDict(method=method)
        self._text = text
        self._json = data
        self.headers = headers or {"content-type": "application/json"}

    def json(self):
        return self._json

    @property
    def text(self):
        if self._text:
            return self._text

        if self._json:
            self._text = json.dumps(self._json)
        return self._text


class MagicRuleMatcher:
    def __init__(self, method: str, url: Union[str, re.Pattern],
                 return_value: Union[dict, "Response", Callable[[str, str, str, dict, dict], Union[dict, Response]]],
                 *, query_params=None, data=None, json=None, headers=None):
        self.method = method.lower()
        self.url = url
        self.query_params = query_params
        self.data = data
        self.json = json
        self.headers = headers
        self.return_value = return_value
        self._requests: List[Request] = []

    def str_url(self):
        if isinstance(self.url, re.Pattern):
            return self.url.pattern
        return self.url

    def match(self, method, url, *, query_params, data, json, headers):
        if callable(method):
            method = method.__name__
        if self.method != method.lower():
            return None

        if not self.match_value(url, self.url):
            return None

        return True

    def match_value(self, value, expected_value):
        if isinstance(expected_value, re.Pattern):
            return expected_value.match(value)
        if expected_value in value:
            return True
        return False

    def add_request(self, query_parameters, data, json, headers):
        self._requests.append(Request(query_parameters, data, json, headers))

    def get_last_request(self) -> Request:
        return self._requests[-1]


class MagicClient:
    def __init__(self):
        self.rules: List[MagicRuleMatcher] = []

    def add_rule(self, rule: MagicRuleMatcher):
        self.rules.append(rule)

    def insert_rule(self, rule: MagicRuleMatcher):
        self.rules.insert(0, rule)

    def make_response(self, response_value, method, url, query_params, data, json, headers):
        if callable(response_value):
            response_value = response_value(url=url, query_params=query_params,
                                            data=data, json=json, headers=headers)
        if isinstance(response_value, Response):
            return response_value
        if isinstance(response_value, dict):
            return Response(method, status_code=200, data=response_value)

        return response_value

    def __call__(self, method, url, query_params, data, json, headers):
        if callable(method):
            method = method.__name__

        for r in self.rules:
            if r.match(method, url, query_params=query_params, data=data, json=json, headers=headers):
                return self.make_response(r.return_value, method, url, query_params, data, json, headers)
        mocked_url = ",".join(f"{rule.method} {rule.str_url()}" for rule in self.rules)
        raise Exception(f"Rule not found for {method} and {url}. Known urls {mocked_url}")
