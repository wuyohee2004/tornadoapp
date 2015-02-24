
#coding:utf-8
import re

print re.compile(ur"@([\u4E00-\u9FA5\w-]+)").findall(u"@童鞋们@123 @_abd")