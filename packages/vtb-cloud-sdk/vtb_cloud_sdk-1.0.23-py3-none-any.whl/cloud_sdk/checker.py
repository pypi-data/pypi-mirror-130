from cloud_sdk.api_client import ApiClientError, BaseApiClient, ApiClientMode
from cloud_sdk.api_client.http_client import RequestHttpClient
from cloud_sdk.auth import SDKAuthorizationToken


class CheckerClientError(ApiClientError):
    @property
    def error_code(self):
        json = self.json
        if not json:
            return None
        if not isinstance(json, dict):
            return None

        error = json.get("error", {})
        code = error.get("code")
        return code


class CheckerClient(BaseApiClient):
    name = 'checker'
    ClientError = CheckerClientError

    def __init__(self, url, token, ssl_verify=True, raw_http_client=None, timeout=None):
        raw_http_client = raw_http_client or RequestHttpClient(url=url, ssl_verify=ssl_verify)
        mode = ApiClientMode(timeout=timeout)
        super().__init__(raw_http_client=raw_http_client, authorizer=SDKAuthorizationToken(token), mode=mode)

    def check(self, graph_id: str, project_name: str, category: str, product_id: str,
              params: dict, graph_version: str=None):
        json = {
            "graph_id": graph_id,
            "project_name": project_name,
            "category": category,
            "product_id": product_id,
            "params": params
        }
        if graph_version:
            json["graph_version"] = graph_version
        return self.post("api/v1/validate", json=json)

    def version(self):
        return self.get("api/version")

    def health(self):
        return self.get("api/v1/health")
