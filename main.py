# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# 最基本的线程创建
# import _thread
# import time
# def print_time( threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print("(%d)%s:%s" % ( count, threadName, time.ctime(time.time())) )
#
# try:
#     _thread.start_new_thread( print_time, ("thread-1", 1, ) )
#     _thread.start_new_thread( print_time, ('thread-2', 4, ) )
# except:
#     print("Error: unable to start thread")
#
# while 1:
#     pass

#线程模块
# import threading
# import time
#
# exitFlag = 0
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if(exitFlag):
#             (threading.Thread).exit()
#         time.sleep(delay)
#         print("%s: %s" % (threadName, time.ctime(time.time())))
#         counter -= 1
#
#
# class MyThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         #super(self.__class__, self).__init__()
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print("starting " + self.name)
#         print_time(self.name, self.counter, 5)
#         print("exiting " + self.name)
#
# thread1 = MyThread(1, 'thread-1', 1)
# thread2 = MyThread(2, 'thread-2', 2)
#
# thread1.start()
# thread2.start()
#
# print("exiting main thread")

# from Include.test.funModel import *

# from Db import DB
# from Db.BuildSql import BuildSql
#
# db = DB(host = '127.0.0.1', username='root', password='root', dbname='test')
#
# res = db.table('test').get()
# print(res)
#
#
# from Client import Client
#
# client = Client()
#
# res = client.agent().request(url='https://dg.fang.anjuke.com/')
# #
# print(res)

# import Building,time
#
# Building.Server().run()


# import os
# file = open('./test.txt', 'w')
# print(file)
# file.write('sss')
# file.close()


# import random,string

# print(''.join(random.sample(string.ascii_letters + string.digits, 32)))

# file = open('./htmlContent'+str(time.time())+'.txt', 'w')
# file.write('hello word')
# file.close()

# def consumer():
#     status = True
#     while True:
#         print('consumer', status)
#         n = yield status
#         print('n=', n)
#         print("我拿到了{}!".format(n))
#         if n == 3:
#             status = False
#
# def producer(consumer):
#     n = 5
#     while n > 0:
#         print('p-n=', n)
#         # yield给主程序返回消费者的状态
#         yield consumer.send(n)
#         print('p-n=aaa')
#         n -= 1
#
# if __name__ == '__main__':
#     c = consumer()
#     c.send(None)
#     p = producer(c)
#
#     for status in p:
#         print('status='+str(status))
#         if status == False:
#             print("我只要3,4,5就行啦")
#             break
#     print("程序结束")


import Building

file = open('./html/anjuke-1_.html', 'r', encoding='UTF-8')
content = file.read()
# print(content)

content = content.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '').replace('&nbsp;', '')
# fo = open('./html/data.html', 'w', encoding='utf-8')
# fo.write(content)
# fo.close()

# <div class="key-list imglazyload">
# <div class="list-page">
# pattern = re.compile(r'<div class="key-list imglazyload">', re.M|re.S|re.X|re.U)
file.close()

obj = Building.AnJuKe.Anjuke(None, {});
data = obj.filterData(content)
print(data)
res = obj.saveData(data, content)
print(res)


# import AliOss,Db
#
# aliOss = AliOss.AliOss('LTAI4GCNbM8N7ygEvSazmRt3', '9ItUuJA1J4cfG2mZ1Ugkhy1m4lLZP9', 'http://oss-cn-hongkong.aliyuncs.com','shudeng')
#
# data = aliOss.getFileList('', '')
#
# db = Db.DB(host='localhost', username='root', password='root', dbname='oss_files')
# res = db.table('new_oss_files').insert(data)
# print(res)

# import re
#
# string = 'xls/人教版八年级上册英语单词表.xls'
# print(re.match('.*/$', string))
# lastPosition = string.rfind('/')
# print(lastPosition, string[lastPosition+1:string.rfind('.')])





