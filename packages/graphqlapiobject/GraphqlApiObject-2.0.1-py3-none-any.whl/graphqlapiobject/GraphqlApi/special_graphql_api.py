import logging
import random

from .graphql_api import GraphqlApi
from .gen_params import GenParams


class FieldValueNotExistError(Exception):
    pass


class GraphqlQueryListAPi(GraphqlApi):

    def query(self, offset=0, limit=10, **kwargs):
        return self.run(offset=offset, limit=limit, **kwargs)

    def query_full(self, offset=0, limit=10, **kwargs):
        return self.set("__fields__").run(offset=offset, limit=limit, **kwargs)

    def query_ids(self, offset=0, limit=10, **kwargs):
        return self.set("data.__fields__", "id").run(offset=offset, limit=limit, **kwargs)

    def filter_result(self, path: str, value):
        """data[?name == 'value']"""
        if not path.startswith("data"):
            path = "data." + self.api_name + ".data." + path
        paths = path.split(".")
        name, path = paths[-1], ".".join(paths[:-1])
        path += f"[?{name} == '{value}']"
        return self.capture(path)

    def search_result(self, path: str, value):
        """data[?name == 'value']"""
        result = self.filter_result(path, value)
        if result:
            logging.info(f"筛选出的值{result}")
            return result[0]
        else:
            raise AssertionError(f"从 {self.data} 中使用 jmespath {path} 没找到值")

    def random(self, num=1):  # 随机从列表中取一个值
        data = self.result.data
        if num == 1:
            return random.choice(data)
        else:
            return random.sample(data, num)


class GraphqlQueryAPi(GraphqlApi):

    def query(self, id_):
        return self.run(id=id_)

    def query_full(self, id_):
        return self.set("__fields__").run(id=id_)


class GraphqlOperationAPi(GraphqlApi):

    def __init__(self, user):
        super(GraphqlOperationAPi, self).__init__(user)
        self.gen: GenParams = GenParams(self.api.schema)
        self.variables = None

    def _run(self, optional: bool, paths: dict):
        v = self.gen.gen(self.api, optional)
        for key, value in paths.items():
            v.change(key, value)
        self.variables = v.result
        return self.run(**self.variables)

    def auto_run(self, paths: dict):  # 自动生成参数进行测试
        return self._run(False, paths)

    def auto_tidy_run(self, paths: dict):  # 非必要的参数不填写进行测试
        return self._run(True, paths)
