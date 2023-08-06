# 齐欣云服 API

[![Org](https://img.shields.io/static/v1?label=org&message=Truth%20%26%20Insurance%20Office&color=597ed9)](http://bx.baoxian-sz.com)
![Author](https://img.shields.io/static/v1?label=author&message=v.stone@163.com&color=blue)
![License](https://img.shields.io/github/license/seoktaehyeon/qixin-api)
[![python](https://img.shields.io/static/v1?label=Python&message=3.8&color=3776AB)](https://www.python.org)
[![PyPI](https://img.shields.io/pypi/v/qixinApi.svg)](https://pypi.org/project/qixinApi/)

操作|方法
---|---
账户列表查询|.get_partner_info_list()
订单详情|.get_order(insure_num)
投保单列表|.list_order()
查询昨日投保单|.list_yesterday_order()

```bash
from qixinApi.qixinApi import QxSdk

pId = ''
sKey = ''

client = QxSdk(partner_id=pId, secret_key=sKey)
# client = QxSdk(partner_id=pId, secret_key=sKey, env_type='test')
try:
    for item in client.list_order(page_index=1, page_size=1)['orders']['data']:
        detail = client.get_order(item['insureNum'])
        print(detail['orderDetail']['applicant']['cName'])
        print(detail['orderDetail']['productName'])
finally:
    client.close()
```
