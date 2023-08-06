import requests

class Robot:
    def __init__(self,name,qq_num,APIport,token):
        self.name = name
        self.qq_num = str(qq_num)
        self.api_url = 'http://localhost:%s/MyQQHTTPAPI'%(str(APIport))
        self.token = str(token)

    def call_api(self,api_name,params,print_result=False):
        params_post={
            'function':api_name,
            'token':self.token,
            'params':params
        }
        raw_result=requests.post(self.api_url,json=params_post)
        result=raw_result.text
        if print_result == True:
            print(result)
