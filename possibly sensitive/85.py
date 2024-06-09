
import tornado.web
import tornado.ioloop
import json
import time
import datetime
import random
from db.peeweetools import Cookies
from db.redistools import RedisTools
from handle.getcookie import *
from handle.Interface import get_cookie, put_cookie, cookie_setting
from handle.testcookie import TestCookie
from tornado.websocket import WebSocketHandler


class Random(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url', None)
        if not url:
            self.render('None')
        lists = get_cookie(url)
        self.set_header('Content-Type', 'text/json')
        self.write(json.dumps(random.choice(lists)))


class All(tornado.web.RequestHandler):

    def get(self):
        url = self.get_argument('url', None)
        if not url:
            self.render('None')
        lists = get_cookie(url)
        self.set_header('Content-Type', 'text/json')
        self.write(json.dumps(lists))


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""

    def get(self):
        item = Cookies()
        items = item.to_dict()
        self.render("index.html", data=items)

    def post(self):
        post_data = dict()
        for key in self.request.arguments:
            post_data[key] = self.get_argument(key)
        print(post_data)
        operation = post_data.get("button", None)
        if operation == 'save':
            if post_data['test_type'] == 'None' or post_data['test_url'] \
                    == 'None' or post_data['test_sign'] == 'None':
                self.write(
                    '<script language="javascript"> alert("有未填项不能更新");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            obj = Cookies().get(domain=post_data['domain'])
            obj.test_type = post_data['test_type']
            obj.test_url = post_data['test_url']
            obj.test_sign = post_data['test_sign']
            obj.save()
            self.write(
                '<script language="javascript"> alert("更新成功"); </script>')
            return self.write("<script>location.href='/';</script>")
        elif operation == 'del':
            obj = Cookies().get(domain=post_data['domain'])
            obj.delete_instance()
            RedisTools.del_key('cookies:{}'.format(post_data['domain']))
            self.write(
                '<script language="javascript"> alert("{}删除成功"); </script>'.format(obj.domain))
            return self.write("<script>location.href='/';</script>")
        elif operation == 'analysis_cookie':
            text = self.get_argument('cookie_text', None)
            url = self.get_argument('cookie_url', None)
            if not text or not url:
                self.write(
                    '<script language="javascript"> alert("提交内容为空不能解析");'
                    ' </script>')
                return self.write("<script>location.href='/';</script>")
            data = get_text_cookie(url, text)
            feedback = put_cookie(url, data)
            if feedback:
                self.write(
                    '<script language="javascript"> alert("解析域名成功"); </script>')
                return self.write("<script>location.href='/';</script>")
        elif operation == 'chrome_cookie':
            url = self.get_argument('cookie_text', None)
            if not url:
                self.write(
                    '<script language="javascript"> alert("提交内容为空不能获取");'