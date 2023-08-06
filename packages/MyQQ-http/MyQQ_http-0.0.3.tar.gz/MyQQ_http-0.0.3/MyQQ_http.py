import requests
import threading
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

echo_mode=False
Running_ThreadingList=[]
Bot_List=[]

class HTTPHandler(BaseHTTPRequestHandler):
    def handler(self):
        #print("data:",self.rfile.readline().decode())
        self.wfile.write(self.rfile.readline())
    
    def do_GET(self):
        #print(self.requestline)
        data= {
            'result_code':'',
            'result_desc':'Success',
            'timestamp': '',
            'data': {}
        }
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):
        #print(self.headers)
        #print(self.command)
        req_datas = self.rfile.read(int(self.headers['content-length']))
        recv_json=json.loads(req_datas)
        #print(recv_json)
        names=globals()
        names['%s_msg'%(str(recv_json['MQ_robot']))] = recv_json['MQ_msg']
        if echo_mode == True:
            print(unquote(recv_json['MQ_msg']))
        data= {
            'result_code':'',
            'result_desc':'Success',
            'timestamp': '',
            'data': {}
        }
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def start_httpserver(callback_port):
    http_server = HTTPServer(('',callback_port),HTTPHandler)
    http_server.serve_forever()


def global_set(API_port,token,callback_port):
    global gAPIport,gtoken,gcallback_port
    gAPIport = API_port
    gtoken = token
    gcallback_port = callback_port
    a=threading.Thread(name='MQ_gbalsten',target=start_httpserver,args=(callback_port,))
    Running_ThreadingList.append(a)
    a.start()


class filter:
    def __init__(self,param,key=[],is_refused=False):
        self.param = param
        self.key = key
        self.is_refused=is_refused

    def set_on(self,msg):
        if self.is_refused == False:
            if msg[self.param] in self.key:
                return msg
        elif self.is_refused == True:
            if msg[self.param] in self.key:
                return ''

class robot:
    def __init__(self,qq_num):
        self.qq_num = str(qq_num)
        self.api_url = 'http://localhost:%s/MyQQHTTPAPI'%(str(gAPIport))
        self.token = str(gtoken)
        self.callback_port = str(gcallback_port)
        Bot_List.append(self)
        globals()['%s_lastmsg'%(self.qq_num)] = '0'

    def msg_loop(self):
        names = globals()
        last_msg=names['%s_lastmsg'%(self.qq_num)]
        if '%s_msg'%(self.qq_num) in names:
            new_msg=names['%s_msg'%(self.qq_num)]
            if new_msg != last_msg:
                last_msg = new_msg
                return new_msg
            else:
                time.sleep(0.001)
        else:
            time.sleep(0.001)

    def call_api(self,api_name,params,print_result=False):
        if echo_mode == True:
            print_result == True
        params_post={
            'function':api_name,
            'token':self.token,
            'params':params
        }
        raw_result=requests.post(self.api_url,json=params_post)
        result=raw_result.text
        if print_result == True:
            print(result)
        return raw_result

def get_friendlist(bot_name):
    raw_result = bot_name.call_api(api_name='Api_GetFriendList',params={"c1":bot_name.qq_num}).json()
    return raw_result['data']['ret']['result']['0']['mems']

def if_friend_exist(bot_name,friend_qq,friend_name=''):
    friend_qq=str(friend_qq)
    for i in get_friendlist(bot_name):
        if i[u'name'] == friend_name:
            return True
        if str(i[u'uin']) == friend_qq:
            return True
    return False

def get_grouplist(bot_name):
    raw_result = bot_name.call_api(api_name='Api_GetGroupList',params={"c1":bot_name.qq_num}).json()
    return raw_result['data']['ret']['data']['group']

def if_group_exist(bot_name,group_qq,group_name=''):
    group_qq=str(group_qq)
    a=str(get_grouplist(bot_name))
    if group_qq in a:
        return True
    if group_name != '':
        if group_name in a:
            return True
    return False

def send_msg(bot_name,toQQ,content,anony=False):
    toQQ=str(toQQ)
    content=str(content)
    params={
        'c1':bot_name.qq_num,
        'c2':0,
        'c3':'',
        'c4':'',
        'c5':'',
        'c6':content,
        'c7':0
    }
    if anony == True:
        params['c2'] = 1
    if if_friend_exist(bot_name,toQQ) == True:
        params['c2'] = 0
        params['c3'] = 1
        params['c5'] = toQQ
    elif if_group_exist(bot_name,toQQ) == True:
        params['c3'] = 2
        params['c4'] = toQQ
    bot_name.call_api('Api_SendMsgEx',params=params)

def relay(bot_name='',fromQQ='',toQQ=''):
    while True:
        if bot_name == '':
            for bot in Bot_List:
                if bot.msg_loop() != None:
                    return 0

