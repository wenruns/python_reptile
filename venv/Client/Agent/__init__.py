from Client.Agent.CustomService import CustomService
from Client.Agent.IP89Service import IP89Service
import Client
from urllib import error,parse,request,response,robotparser

class Agent:

    _client = None

    _proxyips = {}

    _agent_name = '89ip'

    _agents = {}

    _callback = None

    _request_times = 0

    def _checkCallback(self, msg, type):
        if self._callback:
            self._callback(msg, type)

    def __init__(self, callback=None):
        self._callback = callback


    # 获取请求客户端
    def getClient(self):
        if(not self._client or self._client is None):
            self._client = Client.Client(self._callback)
        return self._client

    # 设置代理商
    def useAgent(self, agentName=''):
        self._agent_name = agentName
        return self

    # 获取代理商名称
    def getAgentName(self):
        if(not self._agent_name or self._agent_name is None):
            self._agent_name = '89ip'
        return self._agent_name

    # 获取代理商服务
    def getAgentService(self):
        name = self.getAgentName()
        if(name not in self._agents):
            if name == 'custom':
                self._agents[name] = CustomService();
            else:
                self._agents[name] = IP89Service();
        return self._agents[name];

    # 获取代理IP
    def getProxyIp(self):
        self._checkCallback('获取代理IP','代理服务')
        name = self.getAgentName()
        if(name not in self._proxyips or not self._proxyips[name] or self._proxyips[name] is None):
            agentService = self.getAgentService()
            if(hasattr(agentService,'customProxyIp')):
                self._proxyips[name] = agentService.customProxyIp()
            else:
                self._proxyips[name] = self.requestProxyIP(agentService)
        proxyiplist = self._proxyips[name];
        if not proxyiplist or proxyiplist is None:
            self._checkCallback('获取代理ip失败', '代理服务')
            if self._request_times<3:
                self._request_times += 1
                return self.getProxyIp()
            else:
                self._request_times = 0
                raise Exception('获取代理ip失败', 'PROXYIPSERVICE-FAIL_001')
        ip = proxyiplist.pop();
        self._checkCallback('ip: ' + ip, '代理服务')
        return ip


    def requestProxyIP(self, agentService:IP89Service):
        client = self.getClient()
        res = client.request(url= agentService.getUrl())
        return agentService.format(res)
