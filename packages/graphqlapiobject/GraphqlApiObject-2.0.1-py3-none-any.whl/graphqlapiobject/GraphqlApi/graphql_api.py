from python_utils.formatters import camel_to_underscore
from sgqlc.operation import Operation
from ..User.base_user import BaseUser
import jmespath
from hamcrest import assert_that
from contextlib import contextmanager
from collections import defaultdict


class GraphqlApi(object):
    """
    期望使用的方式：
    （1）调用set方法设置query，然后发送数据
    （2）内置几个查询的query
    """
    api = None

    def __init__(self, user):
        if not isinstance(user, BaseUser):
            raise AssertionError("传入的参数不是指定的User实例")
        self.user = user
        self.api_name = self.api.graphql_name
        # 接口的下滑线形式的名称，sgqlc会把接口定义的驼峰形式的名转化为下划线，这里对应上
        self.camel_name = camel_to_underscore(self.api.name)
        self.sgqlc_schema = self.api.container  # schema对象
        self.op: Operation = Operation(self.sgqlc_schema)  # sgqlc的operation对象
        self.api_op = getattr(self.op, self.camel_name)  # 一个graphql接口可以查询多个，这里每个接口只查询一个，为类变量api
        self._query = defaultdict(list)  # 记录定义的query然后接口调用时执行
        self.data = None  # 返回的原始数据
        self.result = None  # 返回的sgqlc处理的数据

    def new_op(self):  # 每次发送接口重建一个operation，operation无法修改参数
        self.op = Operation(self.sgqlc_schema)
        self.api_op = getattr(self.op, self.camel_name)
        return self.api_op

    @contextmanager
    def complex_op(self, name, *args, **kwargs):
        """
        高级graphql查询可以在第二层接口中写参数，并设定第二层query的参数，虽然公司业务暂时没用到，留个口子
        example: issues = op.repository(owner=owner, name=name).issues(first=100)
        """
        tmp = self.api_op
        self.api_op = getattr(self.api_op, name)(*args, **kwargs)
        yield
        self.api_op = tmp

    def set(self, path, *args, **kwargs):  # 记录设定的query
        """
        :param path: query的路径
        :param args: 使用__fields__方法需要设定参数
        :param kwargs: 使用__fields__方法需要设定参数
        :return:
        """
        self._query[self.api_op].append((path, args, kwargs))
        return self

    q = set

    def f(self):  # send requests
        self.data = self.user.f(self.api_name, self.op)
        self.result = getattr(self.op + self.data, self.camel_name)
        self._query = defaultdict(list)  # 重设query
        self.new_op()  # 重设 operation
        return self

    def run(self, *args, **kwargs):
        def s(op, path, *q_args, **q_kwargs):
            for i in path.split("."):
                op = getattr(op, i)
            op(*q_args, **q_kwargs)

        self.api_op(*args, **kwargs)  # 给接口设定参数
        for api_op, queries in self._query.items():
            for query in queries:
                s(api_op, query[0], *query[1], **query[2])

        return self.f()

    def capture(self, path, options=None):  # 使用jmespath拿到返回数据的值
        return jmespath.search(path, self.data, options=options)

    def assert_that(self, matcher=None, reason=""):  # 使用hamcrest进行对结果的校验
        assert_that(self, matcher, reason)
        return self
