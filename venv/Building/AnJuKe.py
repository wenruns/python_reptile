import websockets,json,Client,time,traceback,os,math,re,Custom,hashlib,Db

class Anjuke:

    _page = '1'

    _area = ''

    _proxy = '89ip'

    _buildingServer = None

    _client = None

    _stop = False

    _db = None

    def __init__(self, buildingServer, data:dict):
        self._buildingServer = buildingServer
        self._page = int(data.get('startPage', 1))
        self._area = data.get('areaName', 'dg')
        self._proxy = data.get('proxyName', '89ip')

    def stop(self, stop = True):
        self._stop = stop;
        return self

    def getDb(self):
        if(not self._db or self._db is None):
            self._db = Db.DB(host='10.1.11.88', username='root', password='root0769', dbname='bkqw_estate', port = 3309)
        return self._db

    def _getClient(self):
        if not self._client or self._client is None:
            self._client = Client.Client(self.output)
            self._client.agent(agentName=self._proxy)
        return self._client

    # 获取请求url
    def _getUrl(self):
        return 'https://' + self._area + '.fang.anjuke.com/loupan/all/p' + str(self._page) + '/'

    # 设置页码
    def setPage(self, page=1):
        self._page = page
        return self

    # 设置区域
    def setArea(self, area):
        self._area = area
        return self

    def output(self, msg, type):
        print(type, msg)
        response = json.dumps({
            'task': 'info',
            'status': True,
            'type': type,
            'msg': msg,
        })
        # self._websocket.send(f"{response}")

    def saveData(self, data, content):
        if isinstance(data, list) and len(data):
            res = self.getDb().table('bkqw_estate_building_temp').insert(data)
            if(res):
                flag = hashlib.md5(content.encode('utf-8')).hexdigest()
                self.getDb().table('bkqw_estate_reptile_records').insert({
                    'source_name':'an_ju_ke',
                    'flag': flag,
                    'created_at': math.ceil(time.time()),
                    'updated_at': math.ceil(time.time()),
                })
                return True
            # else:
                # self.saveData(data, content)
        return False

    # 启动爬取任务
    def repitleInfo(self):
        self.output('任务已创建','楼盘服务')
        while True:
            try:
                if(self._stop):
                    break;
                else:
                    self.output('正在爬取数据', '楼盘服务')
                    url = self._getUrl()
                    client = self._getClient()
                    content = client.request(url=url)
                    data = self.filterData(content)
                    res = self.saveData(data, content)
                    if res:
                        self._page += 1
            except Exception as err:
                self.output('发生不确定错误', '楼盘服务')
                traceback.print_exc()
                break;
        self.output('任务已关闭', '楼盘服务')
        return False


    def filterData(self, content):
        result = re.findall(
            r'<divclass="key-listimglazyload">(.*?)<divclass="list-page">',
            content,
            re.M | re.S | re.X | re.U
        )
        content = result.pop()
        result = re.findall(
            r'<aclass="lp-name"href="(.*?)"soj="(.*?)"target="_blank"><spanclass="items-name">(.*?)</span></a>|<spanclass="list-map"target="_blank">(.*?)</span>|<spanclass="building-area">建筑面积：([0-9]+-[0-9]+㎡)</span>|([0-9]+)室|<iclass="status-iconwuyetp">(.*?)</i>|<spanclass="tag">(.*?)</span>|class="group-marksoj"target="_blank"title="(.*?)">.*?</a>|均价<span>(.*?)</span>(.*?)</p>',
            content,
            re.M | re.S | re.X | re.U
        )
        print(result)
        listData = [];
        for item in result:
            if item[0]:
                i = 0
                data = {
                    # 'detail_url': item[0],
                    # 'soj': item[1],
                    'name': item[2],
                    'detail_address': item[3],
                    # 'area_num': item[4],
                    # 'unit_type': [],
                    'type': item[6],
                    # 'status': item[7],
                    # 'tags': [],
                    'avgpri': item[9],
                    # 'price_unit': item[10],
                    'created_at': math.ceil(time.time()),
                    'updated_at': math.ceil(time.time()),
                }
            else:
                for k in item:
                    data = self.filterItem(i, k, data)
                    i += 1
            if data and i==11:
                data = self.checkDatabase(data)
                if isinstance(data, dict):
                    listData.append(data)
        file = open('./html/data' + str(math.ceil(time.time())) + '.json', 'w', encoding='utf-8')
        file.write(json.dumps(listData))
        file.close()
        return listData

    def checkDatabase(self, data:dict):
        # print(data)
        string = data.get('name').strip() + data.get('detail_address').strip() + data.get('type').strip() + data.get('avgpri').strip()
        flag = hashlib.md5(string.encode('utf-8')).hexdigest()
        # print(flag)
        res = self.getDb().table('bkqw_estate_building_temp').where('flag', '=', flag).first()
        if res:
            return False
        return data



    def filterItem(self, i, val, data):
        if val and data:
            # if i == 0:
                # data['detail_url'] = val
            # elif i == 1:
                # data['soj'] = val
            if i == 2:
                data['name'] = val
            elif i == 3:
                data['detail_address'] = val
            # elif i == 4:
            #     data['area_num'] = val
            # elif i == 5:
            #     data['unit_type'].append(val)
            elif i == 6:
                data['type'] = val
            # elif i == 7:
            #     data['status'] = val
            # elif i == 8:
            #     data['tags'].append(val)
            elif i == 9:
                data['avgpri'] = val
            # else:
            #     data['price_unit'] = val
        return data