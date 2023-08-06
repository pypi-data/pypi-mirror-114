#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com
import random

import requests
from hashlib import md5
from datetime import datetime
import json
from pprint import pprint
import random


class QxSdk(object):
    def __init__(self, partner_id, secret_key, env_type='prod'):
        """
        初始化 PageAPI object
        :param partner_id: 齐欣云服的 partnerId
        :param secret_key: 齐欣云服的密钥 Key
        :param env_type: 环境类型, 默认为 prod, 可以指定为 test
        """
        if env_type == 'prod':
            self.__base_url = 'https://api.qixin18.com/api'
        else:
            self.__base_url = 'https://tuneapi.qixin18.com/api'
        self.__partner_id = int(partner_id)
        self.__secret_key = str(secret_key)
        self.__session = requests.session()
        self.__headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'qixin-api/1.0'
        }

    def close(self):
        self.__session.close()

    def __trans_no(self):
        return '-'.join([
            str(self.__partner_id),
            datetime.now().strftime('%Y%m%d%H%M%S%f')
        ])

    def __post_sign(self, json_data):
        _md5_str = '%s%s' % (
            self.__secret_key,
            json.dumps(json_data).replace('": ', '":').replace(', "', ',"')
        )
        # print('sign string: %s' % _str)
        _md5 = md5()
        _md5.update(_md5_str.encode('utf-8'))
        return _md5.hexdigest()

    def __get_sign(self):
        _md5_str = '%s%s' % (
            self.__secret_key,
            self.__partner_id
        )
        # print('sign string: %s' % _str)
        _md5 = md5()
        _md5.update(_md5_str.encode('utf-8'))
        return _md5.hexdigest()

    def __post_request(self, post_url, post_params, post_body):
        print('POST %s \n %s \n %s' % (post_url, post_params, post_body))
        _rsp = self.__session.post(
            url=post_url,
            headers=self.__headers,
            params=post_params,
            json=post_body
        )
        assert _rsp.status_code == 200, '%s\n%s' % (_rsp.status_code, _rsp.content.decode('utf-8'))
        _rsp_json = _rsp.json()
        assert _rsp_json['respCode'] == 0, '%s\n%s' % (_rsp_json['respCode'], _rsp_json)
        # print('RESPONSE: %s' % _rsp_json)
        print('RESPONSE MSG: %s' % _rsp_json['respMsg'])
        pprint(_rsp_json['data'])
        return _rsp_json['data']

    def __get_request(self):
        pass

    def get_partner_info_list(self):
        """
        账户列表查询
        :return:
        """
        _url = '%s/getPartnerInfoList' % self.__base_url
        _body = {
            'transNo': self.__trans_no(),
            'partnerId': self.__partner_id
        }
        _params = {
            'sign': self.__post_sign(_body)
        }
        return self.__post_request(
            post_url=_url,
            post_params=_params,
            post_body=_body
        )

    def get_order(self, insure_num: str):
        """
        订单详情
        :return:
        """
        _url = '%s/orderDetail' % self.__base_url
        _body = {
            'transNo': self.__trans_no(),
            'partnerId': self.__partner_id,
            'insureNum': insure_num
        }
        _params = {
            'sign': self.__post_sign(_body)
        }
        return self.__post_request(
            post_url=_url,
            post_params=_params,
            post_body=_body
        )

    def list_order(self, page_index: int = 1, page_size: int = 100):
        """
        投保单列表
        :return:
        """
        _url = '%s/orderList' % self.__base_url
        _body = {
            'transNo': self.__trans_no(),
            'partnerId': self.__partner_id,
            'pageIndex': page_index,
            'pageSize': page_size,
        }
        _params = {
            'sign': self.__post_sign(_body)
        }
        return self.__post_request(
            post_url=_url,
            post_params=_params,
            post_body=_body
        )

    def list_yesterday_order(self):
        """
        查询昨日投保单
        :return:
        """
        _url = '%s/summaryOrder' % self.__base_url
        _body = {
            'transNo': self.__trans_no(),
            'partnerId': self.__partner_id,
        }
        _params = {
            'sign': self.__post_sign(_body)
        }
        return self.__post_request(
            post_url=_url,
            post_params=_params,
            post_body=_body
        )

    def get_insure_detail_url(self, insure_num, partner_uniq_key=None):
        if partner_uniq_key is None:
            partner_uniq_key = random.random()
        _url = 'https://api.qixin18.com/dispatch/cps/insureDetail'
        _params = '&'.join([
            'sign=%s' % self.__get_sign(),
            'partnerId=%s' % self.__partner_id,
            'partnerUniqKey=%s' % partner_uniq_key,
            'insureNum=%s' % insure_num
        ])
        return '?'.join([
            _url,
            _params
        ])


if __name__ == '__main__':
    print('This is QiXin API scripts')
