import random
from typing import Any, List

from .tools import fake, create_timestamp
import weakref


class ParamType:
    __slots__ = ("is_required", "is_list", "type_", "in_list_required")

    def __init__(self, type_str: str = None):
        self.is_required = False
        self.is_list = False
        self.type_ = None
        self.in_list_required = False
        if type_str:
            self.handle(type_str)

    def handle(self, type_str):
        if type_str.endswith("!"):  # 必填
            self.is_required = True
            type_str = type_str[:-1]
        if type_str.startswith("["):  # 列表
            self.is_list = True
            type_str = type_str[1:-1]
            if type_str.endswith("!"):  # 去掉列表之后可能还是必填
                self.in_list_required = True
                type_str = type_str[:-1]
        self.type_ = type_str


class Cached(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.__cache = weakref.WeakValueDictionary()

    def __call__(cls, name, *args):
        if args in cls.__cache:
            return cls.__cache[args]
        else:
            obj = super().__call__(name, *args)
            cls.__cache[args] = obj
            return obj


class ChangeParamsByPath:
    @classmethod
    def _handle_path(cls, path: str):
        if path.endswith("]"):
            index = 0
            while path[index] != "[":
                index += 1

            return path[0:index], path[index + 1:-1] if path[index + 1:-1] == "*" else int(path[index + 1:-1])
        else:
            return path, None

    @classmethod
    def _change(cls, obj: dict, paths: List[str], value: Any):
        path, index = cls._handle_path(paths[0])
        if len(paths) == 1 and obj.get(path):  # 迭代终止条件
            if index is None:
                obj[path] = value
            else:
                if index == "*":
                    for i in range(len(obj[path])):
                        obj[path][i] = value
                else:
                    obj[path][index] = value
        else:
            if obj.get(path):
                new_obj = obj.get(path)
                if index is not None:  # 拿到的是列表
                    if index == "*":
                        for i in new_obj:
                            cls._change(i, paths[1:], value)
                    else:
                        cls._change(new_obj[index], paths[1:], value)
                else:
                    cls._change(new_obj, paths[1:], value)
            else:
                for key, new_obj in obj.items():
                    if isinstance(new_obj, list):
                        for i in new_obj:
                            cls._change(i, paths, value)
                    elif isinstance(new_obj, dict):
                        cls._change(new_obj, paths, value)

    @classmethod
    def change(cls, obj: dict, path: str, value: Any):
        """
        :param obj: 要修改的对象
        :param path: 修改的path，将符合条件第一个path修改为对应的value，暂时期望支持
            （1）正常path，'name',
            （2）部分相对path 'input.name'
            （3）批量修改列表中的path 'input.hlist[*].name'
        :param value: 要修改的值
        :return:
        """
        paths = path.split(".")
        return cls._change(obj, paths, value)


class GenParams(metaclass=Cached):
    def __init__(self, schema):
        self.schema = schema
        self.result = None

    def change(self, path: str, value: Any):
        ChangeParamsByPath.change(self.result, path, value)
        return self.result

    def gen(self, api, optional=False):
        self.result = {}
        for param in api.args.values():
            self.result[param.name] = self.__gen(param, optional)
        return self

    def __gen(self, param, optional):
        def handle(param_):
            r = {}
            for n in param_.__field_names__:
                t = getattr(param_, n)
                if optional and not ParamType(str(self.__type__(t))).is_required:
                    continue
                try:
                    r[param_.graphql_name] = self.__gen(t, optional)
                except AttributeError as e:
                    r[t.graphql_name] = self.__gen(t, optional)

            return r

        type_ = self.__type__(param)
        param_type = ParamType(str(type_))
        if param_type.is_list:
            if hasattr(type_, "converter") and "String" in str(type_):
                return [self._string(param) for i in range(3)]
            return [self.__gen(getattr(self.schema, param_type.type_), optional) for i in range(3)]
        elif hasattr(type_, "__field_names__"):
            result = handle(type_)
            return result
        elif hasattr(param, "__field_names__"):
            result = handle(param)
        elif hasattr(type_, "__choices__"):
            return random.choice(type_.__choices__)
        else:
            return getattr(self, "_" + str(param_type.type_).lower())(param)

    def __type__(self, obj):
        try:
            return obj.type
        except AttributeError as e:
            return obj

    @staticmethod
    def _int(param):
        return fake.random_int

    @staticmethod
    def _float(param):
        return fake.pyfloat

    @staticmethod
    def _string(param):
        return getattr(fake, param.name)

    @staticmethod
    def _boolean(param):
        return random.choice([True, False])

    @staticmethod
    def _id(param):
        return 1

    @staticmethod
    def _timestamp(param):
        return create_timestamp()

    @staticmethod
    def _jsonstring(param):
        return "[]"

    @staticmethod
    def _json(param):
        return {"json": "json"}
