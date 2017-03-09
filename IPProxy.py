# coding:utf-8

from multiprocessing import Value, Queue, Process
from api.apiServer import start_api_server
from db.DataStore import store_data

from validator.Validator import validator, getMyIP
from spider.ProxyCrawl import startProxyCrawl

if __name__ == "__main__":
    myip = getMyIP()
    DB_PROXY_NUM = Value('i', 0)
    q1 = Queue()
    q2 = Queue()
    p0 = Process(target=start_api_server) #开启服务
    p1 = Process(target=startProxyCrawl, args=(q1, DB_PROXY_NUM)) #检测数据库中ip并进行打分,ip数量少于设定值开始重新爬取原先网站
    p2 = Process(target=validator, args=(q1, q2, myip)) #检测重新获取的ip有效性,
    p3 = Process(target=store_data, args=(q2, DB_PROXY_NUM)) #存储q2中ip
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()
