#coding:utf-8

__all__ = ['CmdParser']

import sys
from PushManager import *

options = ["--all", "-a", "-E", "-R"]

operate_doc ={                 #相关操作和参数文档
	"push": 											#圆括号中的参数是必须的
"""push [--all | -a | -E [dir_id] [fileIds] | -R [dir_id] [fileIds]]  [-l password] 
*Notice: argument in parentheses is necessary
arguments:
--all       : push all the things to the web server
-a          : same with --all 
-E          : just push all the essays to web server
-R          : just push all the resources files to web server
-dir_id     : push all the file in the dir with dir_id in [essays|resources]lib 
-fileIds    : is a list of files.
              push those file in the dir with file_id in [essays|resources]lib
-l password : use to push a essay which has a lock""",

	"fresh":""""""
} 

error_doc ={  #错误列表
	"Error[1]":                          #未指定操作
	"""Error[1]: No select a operate.
You may use those:""",
	
	"Error[2]":							#指定不存在的操作
	"""Error[2]: No such a operate: %s
You may use those operates:""",

	"Error[3]":							#接收错误参数
	"""Error[3]: Not receive option
usage: %s""",

	"Error[4]":
	"""Error[4]: No such a option: %s
usage: %s""",

	"Error[5]":
	"""Error[5]: Too much arguments	""",

	"Error[6]":
	"""Error[5]: argument dir_id error: %s 
It should be a int number""",
	
	"Error[7]":
	"""Error[5]: argument fileIds error: %s 
It should be a list of int numbers"""
}



def CmdParser():
	"""解析用户输入的指令
	需要改进
	"""

	argc = len(sys.argv)  #参数数量
	argv = sys.argv

	# print sys.argv
	if argc > 5:
		print error_doc["Error[5]"]
		operate = ""
		command = []
		return operate, command

	for _ in range(5-len(sys.argv)):
		argv.append("")

	operate = argv[1]
	option  = argv[2]
	dir_id = argv[3]
	fileIds = argv[4]
	arguments = [option, dir_id, fileIds]

	

	

	if not operate:
		print error_doc["Error[1]"],operate_doc.keys()
		operate = None
		arguments = None

	elif operate not in operate_doc:
		print error_doc["Error[2]"]%operate, operate_doc.keys()
		operate = None
		arguments = None

	else:
		if not option:
			print error_doc["Error[3]"]%operate_doc[operate]
			option = None

		elif option not in options:
			print error_doc["Error[4]"]%(option,options)
			arguments = None

		if dir_id:
			try:
				dir_id = int(dir_id)
				arguments[1] = dir_id
			except ValueError:
				print error_doc["Error[6]"]%dir_id
				arguments = None
			else:
				if fileIds:
					try:
						exec('fileIds = %s'%fileIds )
						for file_id in fileIds:
							if not isinstance(file_id, int):
								raise ValueError
						arguments[2] = fileIds
					except Exception:
						print error_doc["Error[7]"]%fileIds
						arguments = None
	
	return operate, arguments

	



if __name__ == "__main__":

	# print CmdParser()
 	operate, command = CmdParser()
 	print operate, command
 	if operate == 'push' and command:
 		PushManager.Push(command)
 	elif operate == 'fresh':
 		PushManager.refresh()

