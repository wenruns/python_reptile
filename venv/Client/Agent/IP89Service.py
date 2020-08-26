import random
import re

class IP89Service:

    def __init__(self):
        print('89ip -- init')

    def getUrl(self):
        self.nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        return 'http://www.89ip.cn/tqdl.html?api=1&num=' + random.choice(self.nums) + '&port=&address=&isp=';

    def format(self, content):
        # print('content=',content)
        res = re.findall(r"([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]+)", content)
        return res





