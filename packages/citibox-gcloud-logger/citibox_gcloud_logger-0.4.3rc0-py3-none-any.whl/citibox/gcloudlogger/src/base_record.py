import logging


logger = logging.getLogger(__name__)


class ToDictMixin:
    def to_dict(self) -> dict:
        my_dict = {}
        for key, value in self.__dict__.items():
            key = key[1:] if key.startswith('_') else key

            if isinstance(value, ToDictMixin):
                my_dict[key] = value.to_dict()
            else:
                my_dict[key] = value.__dict__ if hasattr(value, '__dict__') else value

        return my_dict


class KwargsToPrivateMixin:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, f'_{key}', value)


class Body(KwargsToPrivateMixin, ToDictMixin):
    def __init__(
            self,
            **kwargs
    ):
        super().__init__(**kwargs)


class RequestHeaders(KwargsToPrivateMixin, ToDictMixin):
    def __init__(self, user_info: str = None, **kwargs):
        self._user_info: str = user_info

        super().__init__(**kwargs)

    @property
    def user_info(self) -> str:
        return self._user_info


class ResponseHeaders(KwargsToPrivateMixin, ToDictMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Params(KwargsToPrivateMixin, ToDictMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Request(KwargsToPrivateMixin, ToDictMixin):
    def __init__(
            self,
            headers: RequestHeaders,
            params: Params,
            body: Body = None,
            **kwargs
    ):
        assert headers is not None
        assert params is not None

        self._headers = headers
        self._params = params
        self._body = body

        super().__init__(**kwargs)


class Response(KwargsToPrivateMixin, ToDictMixin):
    def __init__(
            self,
            status_code: str,
            body: Body = None,
            headers: ResponseHeaders = None,
            **kwargs
    ):
        assert status_code is not None

        self._status_code = status_code
        self._body = body
        self._headers = headers

        super().__init__(**kwargs)

    @property
    def status_code(self) -> str:
        return self._status_code

    @property
    def body(self) -> Body:
        return self._body

    @property
    def headers(self) -> ResponseHeaders:
        return self._headers


class BaseRecord(KwargsToPrivateMixin, ToDictMixin):
    def __init__(
            self,
            url_fingerprint: str,
            duration: float,
            method: str,
            path: str,
            host: str,
            request: Request,
            response: Response,
            **kwargs
    ):
        assert url_fingerprint is not None
        assert duration is not None
        assert method is not None
        assert path is not None
        assert host is not None
        assert request is not None
        assert response is not None

        self._url_fingerprint = url_fingerprint
        self._duration = duration
        self._method = method
        self._path = path
        self._host = host
        self._request = request
        self._response = response
        super().__init__(**kwargs)

    @property
    def message(self) -> str:
        return f'{self._method} {self._response.status_code} {self._path}'
