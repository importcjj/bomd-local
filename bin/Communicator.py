#coding:utf-8

__all__ = ['File2server', 'Essay2server']

import sys
try:
	import poster
except ImportError:
	print "Please install module poster first.."
	sys.exit()

import os
import time
import urllib
import urllib2
from logHelper import *

# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
 
# 在 urllib2 上注册 http 流处理句柄
# register_openers()
 
# # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
# # "image1" 是参数的名字，一般通过 HTML 中的 <input> 标签的 name 参数设置
 
# # headers 包含必须的 Content-Type 和 Content-Length
# # datagen 是一个生成器对象，返回编码过后的参数
# datagen, headers = multipart_encode({"image1": open("DSC0001.jpg", "rb")})
 
# # 创建请求对象
# request = urllib2.Request("http://localhost:5000/upload_image", datagen, headers)
# # 实际执行请求并取得返回
# print urllib2.urlopen(request).read()

class Communicator(object):

	UPLOAD_URL = "http://2.bomd.sinaapp.com/upload"
	USERNAME = "cjj"
	PASWORD = "cjj"

	@classmethod
	def __upload(cls, params):
		"""基本的上传函数
		"""

		opener = poster.streaminghttp.register_openers()
		datagen, headers = poster.encode.multipart_encode(params)
		request = urllib2.Request(cls.UPLOAD_URL, datagen, headers)
		try:
			result = urllib2.urlopen(request).read()
		except urllib2.URLError as e:
			return "网络问题"
		return result


	@classmethod
	def Resource2server(cls, resourcePath):
		"""把资源文件推送至服务器
		"""
	
		params = {'file': open(resourcePath, "rb"),
			'file_name':resourcePath.split(os.sep)[-1],
			'username': cls.USERNAME,
			'password':cls.PASWORD,
			'upload_type':'Resources'}

		return cls.__upload(params)


	@classmethod
	def Essay2server(cls, essayPath, essayLock="", essayTag="普通"):
		"""把文章推送至服务器
		"""

		params = {'essay_body':open(essayPath, "rb+"),
			'essay_title':essayPath.split(os.sep)[-1][:-5],#.strip('.html')
			'essay_date': time.strftime("%Y-%m-%d %X",time.localtime(os.path.getmtime(essayPath))),
			'username':cls.USERNAME, 
			'password':cls.PASWORD, 
			'essay_lock':essayLock,
			'essay_tag':essayTag,
			'upload_type':'Essays'}

		return cls.__upload(params)



# def upload(upload_url, params):
# 	"""基本的上传函数
# 	"""
# 	opener = poster.streaminghttp.register_openers()
# 	datagen, headers = poster.encode.multipart_encode(params)
# 	request = urllib2.Request(upload_url, datagen, headers)
# 	return urllib2.urlopen(request).read()
# 	try:
# 		result = urllib2.urlopen(request).read()
# 	except urllib2.URLError as e:
# 		return "网络问题"
# 	return result



# def File2server(resourcePath, upload_url=UPLOAD_URL, username=USERNAME, password=PASWORD):
# 	"""把资源文件推送至服务器
# 	"""
	
# 	params = {'file': open(resourcePath, "rb"),
# 		'file_name':resourcePath.split(os.sep)[-1],
# 		'username': username,
# 		'password':password,
# 		'upload_type':'Resources'}

# 	return upload(upload_url, params)




# def Essay2server(essayPath, essayLock="", upload_url=UPLOAD_URL, username=USERNAME, password=PASWORD):
# 	"""把文本推送至服务器
# 	"""
# 	params = {'essay_body':open(essayPath, "rb+"),
# 		'essay_title':essayPath.split(os.sep)[-1][:-5],#.strip('.html')
# 		'essay_date': time.strftime("%Y-%m-%d %X",time.localtime(os.path.getmtime(essayPath))),
# 		'username':username, 
# 		'password':password, 
# 		'essay_lock':essayLock,
# 		'upload_type':'Essays'}

# 	return upload(upload_url, params)



if __name__ == "__main__":

	if len(sys.argv) > 1:
		filepath = sys.argv[1]
		print File2server(os.getcwd()+os.sep+filepath)
		sys.exit()


	upload_url = "http://localhost:5000/upload"
	filePath1 = "/Users/cjj/Documents/软件属性需求.html"
	filePath2 = "/Users/cjj/Documents/使用mac_os_x的终端来解压缩rar文件.html"
	username = "cjj"
	password = "cjj"
	# print Essay2server(upload_url, username, password, filePath1, '123')
	print Essay2server(filePath2)
	# print File2server(filePath1)