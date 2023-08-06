import dataclasses
import posixpath
import functools
import typing


@dataclasses.dataclass()
class ServiceConfig:
    url: str
    ssl_verify: bool = True
    token: str = None
    timeout: float = 10

    def override(self, config):
        if not config:
            return

        for name, value in config.items():
            setattr(self, name, value)


@dataclasses.dataclass()
class KeycloakConfig:
    url: str
    client_id: str
    client_secret_key: str
    realm_name: str = "Portal"
    ssl_verify: bool = True


class Config:
    def __init__(self, url, ssl_verify=True, timeout=10, keycloak: typing.Optional[KeycloakConfig] = None,
                 services=None):
        self.base_url = url
        self.ssl_verify = ssl_verify
        self.timeout = timeout
        self.keycloak = keycloak
        self.services = services or {}

    def __str__(self):
        return f"<Config {self.base_url}>"

    @staticmethod
    def urljoin(base_url, service_url):
        if service_url.startswith("http"):
            return service_url
        return posixpath.join(base_url, service_url)

    def _get_service_config(self, service_name, url_suffix):
        config = ServiceConfig(self.urljoin(self.base_url, url_suffix),
                               ssl_verify=self.ssl_verify, timeout=self.timeout)
        config.override(self.services.get(service_name))

        return config

    @functools.cached_property
    def authorizer(self):
        return self._get_service_config("authorizer", "authorizer/")

    @functools.cached_property
    def order_service(self):
        return self._get_service_config("order_service", "order-service/")

    @functools.cached_property
    def product_catalog(self):
        return self._get_service_config("product_catalog", "product-catalog/")

    @functools.cached_property
    def portal(self):
        return self._get_service_config("portal", "portal/")

    @functools.cached_property
    def references(self):
        return self._get_service_config("references", "references/")

    @functools.cached_property
    def calculator(self):
        return self._get_service_config("calculator", "calculator/")

    @functools.cached_property
    def state_service(self):
        return self._get_service_config("state_service", "state-service/")

    @functools.cached_property
    def checker(self):
        return self._get_service_config("checker", "checker/")
