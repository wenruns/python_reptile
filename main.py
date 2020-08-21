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

from Include.test.funModel import *

from Db.Db import DB
from Db.BuildSql import BuildSql

db = DB(host = '127.0.0.1', username='root', password='root', dbname='test')

# def callback(query:BuildSql):
#     query.where('t.id','<', 40).where('u.id','>', 20)

# res = db.table('test').get()

res = db.table('test').where('id', '=', 6).delete()
print(res)

