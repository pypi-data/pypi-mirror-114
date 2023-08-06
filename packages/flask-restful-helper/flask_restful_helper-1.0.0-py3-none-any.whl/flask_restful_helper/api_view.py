from flask import request
from flask_restful import Resource, reqparse

from flask_restful_helper.response import make_response


class ApiView(Resource):
    _logic = None
    decorators = []

    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.query_args = self.parser.parse_args()
        self.set_global_args()
        self.set_query_args()
        if self._logic is not None:
            self.logic = self._logic()

    def set_query_args(self):
        self.set_global_args()
        self.query_args = self.parser.parse_args()
        if request.method == 'GET':
            self.set_get_args()
        elif request.method == 'POST':
            self.set_post_args()
        elif request.method == 'PUT':
            self.set_put_args()
        elif request.method == 'PATCH':
            self.set_patch_args()
        elif request.method == 'DELETE':
            self.set_delete_args()
        self.query_args = self.parser.parse_args()

    def set_global_args(self):
        self.add_union_argument(arg1='page', arg2='results_per_page', type1=int, type2=int, location='args')
        self.parser.add_argument('sort', type=str, required=False, location='args')

    def add_mutex_argument(self, arg1, arg2, type1, type2, location):
        """
        arg1與arg2互斥
        :param arg1:
        :param arg2:
        :param type1:
        :param type2:
        :param location:
        :return:
        """
        self.parser.add_argument(arg1, type=type1, required=False, location=location)
        self.parser.add_argument(arg2, type=type2, required=False, location=location)
        self.query_args = self.parser.parse_args()
        if self.query_args[arg2]:
            self.parser.remove_argument(arg1)
        elif self.query_args[arg1]:
            self.parser.remove_argument(arg2)

        self.query_args = self.parser.parse_args()

    def add_union_argument(self, arg1, arg2, type1, type2, location):
        """
        arg1 與 arg2 必須同時被設定
        :param arg1:
        :param arg2:
        :param type1:
        :param type2:
        :param location:
        :return:
        """
        self.parser.add_argument(arg1, type=type1, required=False, location=location)
        self.parser.add_argument(arg2, type=type2, required=False, location=location)
        self.query_args = self.parser.parse_args()
        if self.query_args[arg2]:
            self.parser.replace_argument(arg1, type=type1, required=True, location=location)
        elif self.query_args[arg1]:
            self.parser.replace_argument(arg2, type=type2, required=True, location=location)

    def add_filter_argument(self, name, type, required, location):
        """
        一次加入單數與複數參數
        :param name:
        :param type:
        :param required:
        :param location:
        :return:
        """
        multiple_name = f'{name}[]'
        self.parser.add_argument(name, type=type, required=required, location=location)
        self.parser.add_argument(multiple_name, type=type, required=required, action='append', location=location)
        self.query_args = self.parser.parse_args()
        if self.query_args[name]:
            self.parser.remove_argument(multiple_name)
        elif self.query_args[multiple_name]:
            self.parser.remove_argument(name)

    def set_get_args(self):
        pass

    def get(self, pk=None):
        if pk is None:
            status, data, status_code = self.logic.list(query_args=self.query_args)
            return make_response(status, data, status_code)
        else:
            status, data, status_code = self.logic.retrieve(pk, query_args=self.query_args)
            return make_response(status, data, status_code)

    def set_post_args(self):
        pass

    def post(self):
        request_data = request.get_json(force=True)
        status, data, status_code = self.logic.create(data=request_data, query_args=self.query_args)
        return make_response(status, data, status_code)

    def set_put_args(self):
        pass

    def put(self, pk):
        request_data = request.get_json(force=True)
        status, data, status_code = self.logic.update(pk=pk, data=request_data, query_args=self.query_args)
        return make_response(status, data, status_code)

    def set_patch_args(self):
        pass

    def patch(self, pk):
        request_data = request.get_json(force=True)
        status, data, status_code = self.logic.update(pk=pk, data=request_data, partial=True,
                                                      query_args=self.query_args)
        return make_response(status, data, status_code)

    def set_delete_args(self):
        pass

    def delete(self, pk):
        status, data, status_code = self.logic.delete(pk=pk)
        return make_response(status, data, status_code)
