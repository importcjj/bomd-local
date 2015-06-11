#coding:utf-8


from PushManager import *
import os

if __name__ == "__main__":

	PushManager.refresh()
	while True:
		cmd_input = raw_input("client>>>")
		if cmd_input:
			os.system("python CmdParser.py %s"%cmd_input)
