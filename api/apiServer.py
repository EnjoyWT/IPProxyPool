# coding:utf-8
'''
定义几个关键字，count type,protocol,country,area,
'''
import json
import sys
import web
import config
from db.DataStore import sqlhelper
#from db.SqlHelper import Proxy

urls = (
    '/', 'select',
    '/delete', 'delete'
)

conditions_name = ['types', 'protocol','counttry']
def start_api_server():
    sys.argv.append('0.0.0.0:%s' % config.API_PORT)
    app = web.application(urls, globals())
    app.run()


class select(object):
    def GET(self):

        inputs = web.input()
        count = inputs.get('count', None)
        #此处添加对 请求key的处理,无论传什么值 只会获取数据库对应的key值
        conditions = {}
        for condition_name in conditions_name:
            value = inputs.get(condition_name, None)  # 字典获取值,如果不存在对应的key返回默认值 None
            if value:
                conditions[condition_name] = value

        json_result = json.dumps(sqlhelper.select(inputs.get('count', None), conditions))
        return json_result


class delete(object):
    params = {}

    def GET(self):
        inputs = web.input()
        json_result = json.dumps(sqlhelper.delete(inputs))
        return json_result


if __name__ == '__main__':
    sys.argv.append('0.0.0.0:8000')
    app = web.application(urls, globals())
    app.run()
