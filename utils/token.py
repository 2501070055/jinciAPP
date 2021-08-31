import hashlib
import time


from django.shortcuts import HttpResponse
from django.conf import settings

api_key_record = {}


def api_auth(func):
    def inner(request, *args, **kwargs):
        client_md5_time_key = request.META.get('HTTP_AUTH_API', '')

        if client_md5_time_key == '':
            return HttpResponse('请填写TOKEN')

        if '|' not in client_md5_time_key:
            return HttpResponse('TOKEN格式错误')

        client_md5_key, client_ctime = client_md5_time_key.split('|')

        client_ctime = float(client_ctime)
        server_time = time.time()

        # 第一关：时间关 10s内访问
        if server_time - client_ctime > 10:
            return HttpResponse('访问时间超时！')

        # 第二关：规则关 防止修改时间
        temp = "%s|%s" % (settings.AUTH_API, client_ctime,)
        m = hashlib.md5()
        m.update(bytes(temp, encoding='utf-8'))
        server_md5_key = m.hexdigest()

        if server_md5_key != client_md5_key:
            return HttpResponse('规则不正确')

        # 删除过期TOKEN
        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]

        # 第三关
        if client_md5_time_key in api_key_record:
            return HttpResponse('令牌已使用过')
        else:
            api_key_record[client_md5_time_key] = client_ctime + 10
            return func(request, *args, **kwargs)

    return inner



