import time,socket,random
from Client.UserAgent import user_agents
from urllib import error,parse,request,response,robotparser
from Client.Agent import Agent
import traceback



class Client:
    # 是否使用代理IP
    _agent = False

    # 代理IP服务商
    _agent_name = '89ip'

    # 代理服务
    _agent_service = None

    # 回调
    _callback = None

    # 请求发送次数
    _request_times = 0

    # 回调
    def _checkCallback(self, msg, type):
        if self._callback:
            self._callback(msg, type);

    # 获取代理服务商提供者
    def _getAgentService(self):
        if not self._agent_service or self._agent_service is None:
            self._agent_service = Agent(self._callback)
        return self._agent_service

    # 获取代理IP
    def _getProxyip(self):
        server = self._getAgentService()
        return server.getProxyIp()

    # 初始化方法
    def __init__(self, callback=None):
        self._callback = callback

    # 代理商设置
    def agent(self, useAgent=True, agentName = '89ip'):
        self._agent = useAgent
        self._agent_name = agentName
        return self

    # 发送网络请求
    def request(self, method='GET', url='', params = {}):
        method = method.upper()
        self._checkCallback('正在发送请求(url='+url+'))','请求服务')
        socket.setdefaulttimeout(6)
        if self._agent:
            proxy_support = request.ProxyHandler({'http': self._getProxyip()})
            opener = request.build_opener(proxy_support, request.HTTPHandler)
        # user_agent = random.choice(user_agents)
        # self._checkCallback('使用代理：'+user_agent, '请求服务')
        try:
            req = request.Request(url=url,method=method)
            req.add_header('Referer', 'http://www.baidu.com')
            req.add_header('User-Agent', "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36")
            req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')
            req.add_header('Accept-Language','zh-CN,zh;q=0.9')
            content = request.urlopen(req).read().decode('utf-8')
            # self._request_times = 0
            return content;
        except error.URLError as e:
            self._checkCallback('发送请求失败(url='+url+', err:'+str(e)+'))', '请求服务')
            # if(self._request_times<3):
            #     self._request_times += 1
            time.sleep(10)
            return self.request(method, url, params)
            # else:
            #     self._request_times = 0
            #     raise Exception('请求失败', 'CLIENT-REQUEST-FAIL_001')
            # traceback.print_exc()
        except error.HTTPError as e:
            self._checkCallback('发送请求失败(url=' + url + ', err:'+str(e)+'))', '请求服务')
            # if (self._request_times < 3):
            #     self._request_times += 1
            time.sleep(10)
            return self.request(method, url, params)
            # else:
            #     self._request_times = 0
            #     raise Exception('请求失败', 'CLIENT-REQUEST-FAIL_001')
            # traceback.print_exc()
        except Exception as e:
            self._checkCallback('发送请求失败(url=' + url + ', err:'+str(e)+'))', '请求服务')
            # if (self._request_times < 3):
            #     self._request_times += 1
            time.sleep(10)
            return self.request(method, url, params)
            # else:
            #     self._request_times = 0
            #     raise Exception('请求失败', 'CLIENT-REQUEST-FAIL_001')
            # traceback.print_exc()