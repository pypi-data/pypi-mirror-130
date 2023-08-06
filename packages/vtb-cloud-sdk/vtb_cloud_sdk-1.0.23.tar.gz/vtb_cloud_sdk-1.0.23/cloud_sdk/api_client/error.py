import functools


class ApiClientError(IOError):
    client_name = None

    def __init__(self, *, response=None, message=None, **kwargs):
        super().__init__()

        self._response = response
        self._message = message
        self.status_code = response.status_code if response is not None else None
        self.kwargs = kwargs

    def __str__(self):
        return f"<ResponseError {self.status_code} - {self.code or ''}: {self.message} {self.json}>"

    def get_client_name(self):
        return self.client_name or self.__class__.__module__.split(".")[-1]

    @functools.cached_property
    def json(self):
        if self.content_type is None or self.content_type.split(";", 1)[0] != "application/json":
            return None
        return self._response.json()

    @functools.cached_property
    def error(self):
        json = self.json
        if json:
            return json.get("error")
        return None

    @property
    def content_type(self):
        if self._response is not None:
            return self._response.headers.get("content-type", "")
        else:
            return None

    @property
    def url(self):
        return self._response.url

    @property
    def code(self):
        error = self.error
        return error.get("code") if error else None

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        if self._message:
            return self._message
        json = self.json
        if not json:
            return None

        return json.get("message") or json.get("detail")
