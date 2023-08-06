import urllib.request

from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from beeprint import pp
from contextlib import contextmanager
import allure


# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context


def pformat(strings):
    return pp(strings, output=False, max_depth=20, text_autoclip_maxline=20)


def record(body, title=""):
    if not body:
        body = "no records ,please check something"
    allure.attach(str(body), str(title), allure.attachment_type.TEXT)


class BaseUser(object):

    def __init__(self, base_url, mutation, login, proxy=None):
        self.base_url = base_url
        self.mutation = mutation
        self.headers = {"Content-Type": "application/json"}
        if proxy:  # 调试使用
            authinfo = urllib.request.HTTPBasicAuthHandler()

            proxy_support = urllib.request.ProxyHandler(proxy)

            # build a new opener that adds authentication and caching FTP handlers
            opener = urllib.request.build_opener(proxy_support, authinfo,
                                                 urllib.request.CacheFTPHandler)

            # install it
            urllib.request.install_opener(opener)

        self.graphql_client = HTTPEndpoint(base_url, self.headers)
        self.login_info = login
        self.login()

    def f(self, api_name, op: Operation):
        with allure.step(
                '{user} send request {query_name}'.format(user=self.login_info["account"], query_name=api_name)):
            with self.play_api_name(api_name):
                data = self.graphql_client(op)
                record(self.graphql_client.url, "发送的url")
                record(self.headers, "发送的headers")
                record(pformat(op), "发送的参数")
                record(pformat(data), "返回的结果")
                if data.get("errors"):
                    raise SendRequestError("\n op  %s get error %s" % (op, data.get("errors")))
                return data

    def update_headers(self, **kwargs):
        for key in kwargs.keys():
            self.headers[key] = kwargs[key]
        self.graphql_client.base_headers = self.headers

    def update_token(self, token=None):
        token_dict = {}
        if token:
            token_dict["authorization"] = "Token " + token
        else:
            self.graphql_client.base_headers.pop('authorization', None)
        self.update_headers(**token_dict)

    @allure.step("登录 {1}")
    def _login(self, login_information):
        account, password = login_information.values()
        variables = {"input": {"account": account, "password": password}}
        op = Operation(self.mutation)
        op.login(**variables)
        token = self.f("login", op)["data"]["login"]["token"]
        self.update_token(token)

    def login(self):
        try:
            self._login(self.login_info)
        except Exception as e:
            print(e)
            record(e)
            record(self.login_info)
            record("登录错误")
            raise Exception("登录失败，请查看原因")

    @contextmanager
    def play_api_name(self, name):
        tmp = self.base_url
        self.graphql_client.url = "?".join([tmp, name])
        yield
        self.graphql_client.url = tmp


class SendRequestError(AssertionError):
    pass
