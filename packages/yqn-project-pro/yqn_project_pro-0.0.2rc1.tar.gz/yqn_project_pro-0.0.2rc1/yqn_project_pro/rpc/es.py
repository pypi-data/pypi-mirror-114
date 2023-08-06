# -*- coding: utf-8 -*-
# @author: YuHuiMing
# @file: es.py
# @time: 2021/7/15
# @desc:
import json

from elasticsearch import NotFoundError, Transport, RequestsHttpConnection, Elasticsearch, helpers
from yqn_project_pro.utils import error_mark
from yqn_project_pro.rpc import RPCConfigBase


class EsClient(RPCConfigBase):

    def __init__(self, **kwargs):
        super(EsClient, self).__init__(**kwargs)
        self._host = None
        self._port = None
        self._index = None
        self._doc = None
        self._username = None
        self._password = None
        self.base_url = None
        self.init_es_params()

    def init_es_params(self):
        self._host = self.get_config("es_host")
        self._port = self.get_config("es_port")
        self._index = self.get_config("es_index")
        self._doc = self.get_config("es_doc")
        self._username = self.get_config("es_username")
        self._password = self.get_config("es_password")
        assert all([self._host, self._port, self._index, self._doc]), "es config error"
        self.base_url = "/%s/%s" % (self._index, self._doc)

    def connect(self, **kwargs):
        if self.connector is None:
            # 基于requests实例化es连接池
            self.connector = Transport(hosts=[{'host': self._host}], port=self._port, http_auth=(self._username, self._password),
                                       connection_class=RequestsHttpConnection).connection_pool
        connector = self.connector.get_connection()
        return connector

    def reconnect(self, **kwargs):
        pass

    def request(self, method, url, headers=None, params=None, body=None):
        """
        向es服务器发送一个求情
        @method     请求方式
        @url        请求的绝对url  不包括域名
        @headers    请求头信息
        @params     请求的参数：dict
        @body       请求体：json对象(headers默认Content-Type为application/json)
        # return    返回体：python内置数据结构
        """
        conn = self.connect()
        try:
            status, headers, body = conn.perform_request(method, url, headers=headers, params=params, body=body)
        except Exception as e:
            error_mark(e)
            raise e
        if method == "HEAD":
            return status
        return json.loads(body)

    @staticmethod
    def deal_es_port_data(es_data):
        ret_list = []
        if es_data:
            _hits = es_data.get("hits", {})
            for es_row in _hits.get("hits", []):
                ret_list.append(es_row.get("_source"))
        return ret_list

    def query(self, body):
        """query by body"""
        url = self.base_url + "/_search"
        resp_data = self.request("GET", url=url, body=json.dumps(body, ensure_ascii=False))
        ret = self.deal_es_port_data(resp_data)
        return ret

    def insert_by_id(self, _id, data):
        """insert one by id"""
        url = self.base_url + f"/{_id}"
        ret = self.request("POST", url=url, body=json.dumps(data))
        return ret

    def delete_all_data(self):
        url = self.base_url + f"/_delete_by_query"
        del_all_body = {
            "query": {
                "match_all": {}
            }
        }
        ret = self.request("POST", url=url, body=json.dumps(del_all_body))
        return ret

    def insert_array(self, docs: list):
        """insert es data, array[dict...]"""
        insert_list = []
        for doc in docs:
            es_data = {
                "_index": self._index,
                "_type": self._doc,
                "_source": doc
            }
            if doc.get("id"):
                es_data["_id"] = doc.get("id")
            insert_list.append(es_data)
        es = Elasticsearch([self._host], http_auth=(self._username, self._password),
                           port=self._port, timeout=5000)
        helpers.bulk(es, insert_list, request_timeout=10 * 60)
        es.close()

    def get_count(self):
        url = self.base_url + "/_count"
        ret = self.request("POST", url=url, body={})
        return ret.get("count")

    def get_id(self, _id):
        url = self.base_url + f"/{_id}"
        ret = self.request("GET", url)
        return ret.get("_source")

    def get_ids(self, _ids):
        url = self.base_url + f"/_search"
        req_body = {
          "query": {
            "ids": {
                 "values": [str(_id) for _id in _ids]
            }
          }
        }
        ret = self.request("GET", url, body=json.dumps(req_body))
        return self.deal_es_port_data(ret)

    def update_by_id(self, _id, data):
        url = self.base_url + f"/{_id}/_update"
        update_body = {
            "doc": data
        }
        ret = self.request("POST", url, body=json.dumps(update_body))
        return ret

    def close(self, **kwargs):
        pass
