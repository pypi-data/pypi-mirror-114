"""
3.0
1. 发送参数，修改自动生成参数后的修改方式，采用传入位置或者相对位置参数进行修改参数 (ok)
2. 从结果中获取数据采取两种方式：（1）原生的sgqlc的类型（2）jmespath进行修改 (ok)
3. 接口留一个方法， 使用hamcrest对返回的数据进行校验 (ok)
"""
from .graphql_api import GraphqlApi
from .tools import fake, create_timestamp, create_num_string
from .gen_params import GenParams
from .special_graphql_api import GraphqlQueryListAPi, GraphqlQueryAPi, GraphqlOperationAPi

__all__ = ["GraphqlApi", "fake", "create_timestamp", "create_num_string", "GenParams",
           "GraphqlQueryAPi", "GraphqlQueryListAPi", "GraphqlOperationAPi"]
