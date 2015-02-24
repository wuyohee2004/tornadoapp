#coding=utf-8
#
# from weibo import APIClient
# #1.生成URL过程
# APP_KEY = '1173024669'
# APP_SECRET = 'a38512798f1042a608662eb319749761'
# CALLBACK_URL = 'http://e.com/weibo/callback'
#
# client = APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
# url = client.get_authorize_url()
#
# print url
#
# #2.授权成功后会跳到callback url,并传一个code参数
# code = url.web.framework.request.get('code')
# r = client.request_access_token(code)
# access_token = r.access_token # 新浪返回的token，类似abc123xyz456
# expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# # TODO: 在此可保存access token
# client.set_access_token(access_token, expires_in)

import wmi


def sys_version():
    conn = wmi.WMI(computer='192.168.2.2',user=r'.\jin',password='111')
    a=conn.Win32_Process.Create(CommandLine='query user')
    print(a)
if __name__ == '__main__':
    user=r'JIN-PC\jin'
    print user
    sys_version()


