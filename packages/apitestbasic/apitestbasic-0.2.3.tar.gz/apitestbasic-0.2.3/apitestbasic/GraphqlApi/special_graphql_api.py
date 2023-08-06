import logging

from .graphql_api import GraphqlApi
from .decorator import Decorator
from .gen_params import GenParams
from functools import partial


class FieldValueNotExistError(Exception):
    pass


class GraphqlQueryListAPi(GraphqlApi):

    @Decorator.set_query()
    def query(self, offset=0, limit=10, **kwargs):
        self.api_op(offset=offset, limit=limit, **kwargs)

    @Decorator.set_full_query()
    def query_full(self, offset=0, limit=10, **kwargs):
        self.api_op(offset=offset, limit=limit, **kwargs)

    @Decorator.only_query_id()
    def query_ids(self, offset=0, limit=10, **kwargs):
        self.api_op(offset=offset, limit=limit, **kwargs)

    def filter_result(self, name: str, value):
        result = self.result.data
        names = name.split(".")

        def judge(obj):
            r = obj
            for name_ in names:
                r = getattr(r, name_)
            return r == value

        return list(filter(judge, result))

    def search_result(self, name: str, value):
        search_list = self.result.data
        if search_list and isinstance(search_list[0].obj, list):
            new_list = []
            for i in search_list:
                new_list.extend(i)
            search_list = new_list
        result = self.filter_result(name, value)
        if result:
            logging.info(result, "筛选出的值")
            return result[0]
        else:
            raise AssertionError(f"从 {result} 中没找到 {name} 字段为 {value} 的值")

    def normal_request(self):
        return self.query()


class GraphqlQueryAPi(GraphqlApi):

    @Decorator.set_query()
    def query(self, id_):
        self.api_op(id=id_)

    @Decorator.set_full_query()
    def query_full(self, id_):
        self.api_op(id=id_)


class GraphqlOperationAPi(GraphqlApi):

    def __init__(self, user):
        super(GraphqlOperationAPi, self).__init__(user)
        self._gen = partial(GenParams(self.api.schema).gen, self.api)
        self.variables = self.new_var()

    @Decorator.set_query()
    def manual_run(self, **kwargs):
        self.api_op(**kwargs)

    @Decorator.set_full_query()
    def manual_run_return_all(self, **kwargs):
        self.api_op(**kwargs)

    def new_var(self, optional=False):
        self.variables = self._gen(optional)
        return self.variables

    def run(self):
        return self.manual_run(**self.variables)

    def run_return_all(self, **kwargs):
        return self.manual_run_return_all(**self.variables)

    def run_part(self, **kwargs):
        self.variables.input.stay(list(kwargs.keys()))
        for key, value in kwargs.items():
            setattr(self.variables.input, key, value)
        return self.manual_run(**self.variables)


class GraphqlUpdateAPi(GraphqlOperationAPi):

    def __init__(self, user, set_id=None):
        self.set_id = set_id
        super(GraphqlUpdateAPi, self).__init__(user)

    @property
    def id(self):
        return self.set_id

    @id.setter
    def id(self, value):
        self.set_id = value
        self.variables.input.id = self.set_id

    def new_var(self, optional=False):
        self.variables = self._gen(optional)
        self.variables.input.id = self.set_id
        return self.variables


class GraphqlApiExtension:
    GraphqlQueryListAPi = GraphqlQueryListAPi
    GraphqlQueryAPi = GraphqlQueryAPi
    GraphqlOperationAPi = GraphqlOperationAPi
    GraphqlUpdateAPi = GraphqlUpdateAPi
