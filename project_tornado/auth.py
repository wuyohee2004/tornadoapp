#coding-utf-8
import os
import re
import time
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from pymongo import errors as mongoerr

from settings import db


define("port", default=8888, help="run on the given port", type=int)

def get_tags(content):#tornado default input always encode to utf-8
    r = re.compile(ur"@([\u4E00-\u9FA5\w-]+)")
    return r.findall(content)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class WeiboHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render("weibo_add.html")

    @tornado.web.authenticated
    def post(self):
        result = self.get_argument("content",None)
        print get_tags(result)
        db.weibo.insert({"content":result,"user":self.get_current_user(),"ts":time.time()})
        self.write(result)


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)
        # self.write("<br><br><a href=\"/auth/logout\">Log out</a>")

class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        self.render("userinfo.html" , **{"user":user})

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        account = self.get_argument("account")
        password = self.get_argument("password")
        if account == '' or password == '':
            self.write("Username or Password not filled!")
        elif db.user.find({"account":account}).count() > 0:
            return self.write("<h1>User Already Registered! Don't duplicate apply.</h1>")
        else:
            db.user.insert({"account":account,"password":password})
            self.set_secure_cookie("user",account)
            self.redirect("/user")

class UsersHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # users = db.user.find({"account":{"$ne":self.get_current_user()}})  #ne is str not in result
        followed_users = db.follow.find({"user":self.get_current_user()},{"follow_user":1})
        filter_users = [follow["follow_user"] for follow in followed_users]
        filter_users.append(self.get_current_user())
        users = db.user.find({"account":{"$nin":filter_users}})#nin is not in list
        self.render("user_list.html",**{"users":users})

class FollowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_argument("follow_user",None)
        if not user:
            return self.redirect("/users")
        try:
            db.follow.insert({"follow_user":user,"user":self.get_current_user()})
        except mongoerr.DuplicateKeyError:
            return self.write("Already followed: %s" % user)
        return self.redirect("/followed")

class FollowedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
       followed_users = db.follow.find({"user":self.get_current_user()})
       self.render("followed_user.html",**{"followed_users":followed_users})


# class AuthHandler(BaseHandler, tornado.auth.GoogleMixin):
#     @tornado.web.asynchronous
#     def get(self):
#         if self.get_argument("openid.mode", None):
#             self.get_authenticated_user(self.async_callback(self._on_auth))
#             return
#         self.authenticate_redirect()
#
#     def _on_auth(self, user):
#         if not user:
#             raise tornado.web.HTTPError(500, "Google auth failed")
#         self.set_secure_cookie("user", tornado.escape.json_encode(user))
#         self.redirect("/")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        # self.clear_cookie("user")
        account,password = '',''
        try:
            account = self.get_argument("account")
            password = self.get_argument("password")
        except tornado.web.HTTPError:
            pass
        user = db.user.find_one({"account":account},{"account":1,"password":1})
        print user
        if account =='' or password =='':
            return self.write("password or username not filled!")
        # elif db.user.find({"account":account,"password":password}).count() == 0:
        #     return self.write("password or username invalid! Please input correctly")
        elif not user:
            return self.write("User dosn't existed!")
        elif user['password'] != password:
            return self.write("wrong password!")

        self.set_secure_cookie("user",self.get_argument("account"))
        self.redirect("/user")

settings = {
    "cookie_secret":"32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url":"/login",
    # "xsrf_cookies": True,
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
}

Application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/weibo/add", WeiboHandler),
        (r"/register", RegisterHandler),
        (r"/user", UserInfoHandler),
        (r"/users", UsersHandler),
        (r"/follow", FollowHandler),
        (r"/followed", FollowedHandler),
        ],**settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
    re.compile(ur"@([\u4E00-\u9FA5\w-]+?)")
