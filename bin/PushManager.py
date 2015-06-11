#coding:utf-8

__all__ = ['PushManager']

import sys
from Scaner import *
from Storage import *
from local2server import *


def Markdown2Html():
	"""将文章从markdown形式转成Html形式
	"""
	pass


def Essay2Server():
	"""将文章主体推送至服务器端
	"""
	pass

def Resource2Server():
	pass


def HtmlHandler():
	"""获取html文件中的主体部分
	"""



class PushManager(object):

	storages = Storages()
	librarys = Scaner.scan(storages)
		
	@classmethod
	def refresh(cls):
		import os
		os.system('clear')

		cls.__print()


	@classmethod
	def __print(cls):
		for lib in cls.librarys.values():
			lib.ls()


	@classmethod
	def Push(cls, command):
		option, arg_1, arg_2 = command
		if option == '-a' or option == '--all':
			print "if you want to push Everything?(y/n)" 
			if "y" ==raw_input():
				for lib in cls.librarys.values():
					for one in lib.EveryFile():
						print one

		elif option == '-E':

			if not arg_1 and arg_1 != 0:
				print "if you want to push Everything in Essay library?[y/n]"
				if "y" ==raw_input():
					lib = cls.librarys["Essays"]
					for one in lib.EveryFile():
						print one
			elif arg_1 >= cls.librarys["Essays"].dirNum:
				print "Essay library has no directory with id %d"%arg_1
			else:
				if not arg_2:
					print "if you want to push Everything in Essay library directory %s?[y/n]"%arg_1
					if "y" ==raw_input():
						lib = cls.librarys["Essays"]
						for one in lib.EveryFileInDir(arg_1):
							print one
				else: #if arg_2
					print "if you want to push file",arg_2,"in Essay library directory %s?[y/n]"%(arg_1)
					if "y" ==raw_input():
						lib = cls.librarys["Essays"]
						files = lib.FilesInDir(arg_1)
						for one in files:
							if files.index(one) in arg_2:
								print one
								print Essay2server(one)

		else: #if option == "-R"

			if not arg_1 and arg_1 != 0:
				print "if you want to push Everything in Resource library?[y/n]"
			else: #if arg_1
				if not arg_2:
					print "if you want to push Everything in Resource library directory %s?[y/n]"%arg_1
				else: #if arg_2
					print "if you want to push file",arg_2,"in Resource library directory %s?[y/n]"%(arg_1)
					if "y" ==raw_input():
						lib = cls.librarys["Resources"]
						files = lib.FilesInDir(arg_1)
						for one in files:
							if files.index(one) in arg_2:
								print one
								print File2server(one)

		
		raw_input("回车确认")
		cls.refresh()


if __name__ == "__main__":
	PushManager.refresh()