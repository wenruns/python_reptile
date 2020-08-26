import asyncio,websockets,Custom,json,WThread,random,string
from Building import AnJuKe


class Server:
    _reptileServer = {}

    # 检测客户端权限，用户名密码通过才能退出循环
    async def _checkPermission(self, websocket:websockets.server.WebSocketServerProtocol, path):
        while True:
            recv_str = await websocket.recv()
            cred_dict = recv_str.split(":")
            if cred_dict[0] == "admin" and cred_dict[1] == "123456":
                response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
                await websocket.send(response_str)
                return True
            else:
                response_str = "sorry, the username or password is wrong, please submit again"
                await websocket.send(response_str)

    def runTask(self, data:dict):
        sourceName = data.get('sourceName', 'an_ju_ke');
        server = Custom.switch(sourceName, {
            'an_ju_ke': AnJuKe.Anjuke(self, data)
        })
        self._reptileServer[data.get('token', sourceName)] = server
        server.repitleInfo()
        return True

    # 启动爬虫服务
    async def reptile(self, websocket: websockets.server.WebSocketServerProtocol, data:dict):
        token = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        data['token'] = token
        WThread.WThread(self.runTask, data).start()
        response = json.dumps({
            'task':'start',
            'token':token,
            'errmsg':'ok',
        })
        await websocket.send(f"{response}")
        return token


    async def checkStatus(self, websocket: websockets.server.WebSocketServerProtocol, token):
        if not token or token is None:
            response = json.dumps({
                'task':'check',
                'status': False,
                'errmsg': '未携带token'
            })
            await websocket.send(f"{response}")
        else:
            response = json.dumps({
                'task':'check',
                'status':True,
                'errmsg':'OK',
                'token':token,
            })
            await websocket.send(f"{response}")

    # 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
    async def _onMessage(self, websocket: websockets.server.WebSocketServerProtocol, path):
        while True:
            try:
                recv_text = await websocket.recv()
                try:
                    data = json.loads(recv_text)
                except:
                    data = recv_text
                print('info: ', data)
                if isinstance(data, dict):
                    task = data.get('task', 'check')
                    if task == 'check':
                        await self.checkStatus(websocket, data.get('reptile_token'))
                    elif task == 'start':
                        await self.reptile(websocket,data)
                    else:
                        print('...')
                else:
                    response_text = 'recieved: ' + data
                    await websocket.send(response_text)
            except Exception as err:
                print(type(err), err)
                break;

    # 服务器端主逻辑
    # websocket和path是该函数被回调时自动传过来的，不需要自己传
    async def _listen(self, websocket:websockets.server.WebSocketServerProtocol, path):
        # await self._checkPermission(websocket, path)
        await self._onMessage(websocket, path)


    def run(self):
        # 把ip换成自己本地的ip
        start_server = websockets.serve(self._listen, '0.0.0.0', 8888)
        # 如果要给被回调的main_logic传递自定义参数，可使用以下形式
        # 一、修改回调形式
        # import functools
        # start_server = websockets.serve(functools.partial(main_logic, other_param="test_value"), '10.10.6.91', 5678)
        # 修改被回调函数定义，增加相应参数
        # async def main_logic(websocket, path, other_param)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()