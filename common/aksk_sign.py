# -*- coding: utf-8 -*-

import time
import random
import string
import hashlib
from common.requ_case import ApiRequest


def make_aksk_sign(ak, sk, params=None):
    ts = str(int(round(time.time() * 1000)))
    ra = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    x = ''
    if params:
        for k in sorted(params):
            x = x + '%s=%s&' % (k, params[k])
        x = x[:-1]
    mes = ak + ts + ra + x + sk
    m = hashlib.md5()
    n = mes.encode(encoding='utf-8')
    m.update(n)
    sign = m.hexdigest()
    header = {
        'x-app-id': ak,
        'x-sign': sign,
        'x-timestamp': ts,
        'x-nonce-str': ra
    }
    # print(ts)
    # print(ra)
    # print(x)
    # print(sign)
    return header


if __name__ == '__main__':
    url = 'http://test-api-gateway.kaikeba.com/coursemanage/v1/app/manager/'
    ak = 'bsy1000000000008'
    sk = '404233a8271cd66617d6191860218a65'
    para = {'user': 1}
    header = make_aksk_sign(ak, sk, para)
    api = ApiRequest(url=url, method='GET', params=para, headers=header)
    r, s = api.test_api()
    print(r)
    print(s)

