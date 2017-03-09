# -*- coding: utf-8 -*-
import pymongo
from config import DB_CONFIG

from db.ISqlHelper import ISqlHelper


class MongoHelper(ISqlHelper):
    def __init__(self):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'],connect=False)

    def init_db(self):
        self.db = self.client.proxy
        self.proxys = self.db.proxys

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        # 插入前检测本地时候存储有
        if value:
            proxy = dict(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                         country=value['country'],
                         area=value['area'], speed=value['speed'], score=0)
            self.proxys.insert(proxy)

    def delete(self, conditions=None):
        if conditions:
            self.proxys.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.proxys.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None):

        '''
        默认返回评分高的,速度快的
        :param count: 设置返回的个数
        :param conditions: 只会获取 types和 protocol 字段(需要去除count键)
        :return:
        '''
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None) #字典获取值,如果不存在对应的key返回默认值 None
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}

        items = self.proxys.find(conditions, limit=count).sort(
            [("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
        results = []

        for item in items:
            #print  item
            result = (item['ip'], item['port'], item['score'])
            results.append(result)
        return results


if __name__ == '__main__':
    from db.MongoHelper import MongoHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    print  sqlhelper.select(5,{})
    # items= sqlhelper.proxys.find({'types':0})
    # for item in items:
    # print item
    # # # print sqlhelper.select(None,{'types':u'0'})
    pass
