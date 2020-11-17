url_login = 'https://sso.garmin.com/sso/login'
req_login = s.get(url_login, params=params_login)
req_login2 = s.post(url_login, data=data_login)
# we need that to authenticate further, kind like a weird way to login but...
t = req_login2.cookies.get('CASTGC')
t = 'ST-0' + t[4:]
# now the auth with the cookies we got
url_post_auth = 'https://connect.garmin.com/post-auth/login'
params_post_auth = {'ticket': t}
req_post_auth = s.get(url_post_auth, params=params_post_auth)
# login should be done we upload now
url_upload =\
    'https://connect.garmin.com/proxy/upload-service-1.1/json/upload/.fit'
