#coding:utf-8
__all__ = ['Scaner']

import os
import time
from logHelper import *   #function log



def WalkByStep(root, fileType):
	"""递归遍历文件夹
	"""
	try:
		allThing = os.listdir(root)
	except Exception as e:
		message = "No such file or directory:"+root
		log("log/Scaner.log",message)
		yield [message, "", ""]
	else:
		dirs = list()
		files = list()
		for thing in allThing:
			path = root+os.sep+thing
			# print "%s is dir: "%path, os.path.isdir(path)
			if os.path.isdir(path):
				dirs.append(thing)
			else:
				if fileType:                                      #如果是我们指定格式的文件，就收录到文件列表
					suffix = os.path.splitext(thing)[-1]   		  #获取文件后缀名
					if suffix in fileType:
						files.append(thing)
				else:
					files.append(thing)
		walkThough = [root, dirs, files]
		yield walkThough
		for path in dirs:
			for walkThough in WalkByStep(root+os.sep+path, fileType):
				yield walkThough





class Scaner(object):

	def __init__(self):
		pass


	@classmethod
	def scan(cls, storages):
		"""扫描指定仓库的文件，分别得到文章列表和资源列表
		"""
		Essays = {}        #文章列表
		EssaysDir = []

		Resources = {}     #资源列表
		ResourcesDir = []
		for storage in storages:
			root = storage.Root   #库的根目录

			EssayType = storage.EssayType
			for essayPath in storage.EssayPath:
				for essayRoot, dirs, files in WalkByStep(root+os.sep+essayPath, EssayType):
					EssaysDir.append(essayRoot)
					Essays[essayRoot] = files

			for resourcePath in storage.ResourcePath:
				for resourceRoot, dirs, files in WalkByStep(root+os.sep+resourcePath, []):
					ResourcesDir.append(resourceRoot)
					Resources[resourceRoot] = files

		return {'Essays':Library('Essays',EssaysDir,Essays), 
				'Resources':Library('Resources',ResourcesDir, Resources)
				}


class Library(object):

	def __init__(self, libType, libDirs, fileDict):
		self.libType = libType      #库的类型，列如 文章库，资源文件库
		self.fileDict = fileDict    #文件字典 {文件夹 ：文件夹中的文件}
		self.directory = libDirs    #文件夹列表

		self.dirNum = len(self.directory)


	def ls(self):
		"""打印库中所有文件的结构
		"""
		print "All %s:"%self.libType
		dirIndex = 0
		for fileDir in self.directory:
			files = self.fileDict[fileDir]
			if not files:
				continue
			
			print "%s.%d (%s)"%(self.libType[0], dirIndex, fileDir)
			dirIndex += 1

			fileIndex = 0
			for _file in files:
				fileName = fileDir+os.sep+_file

				fileSize = os.path.getsize(fileName)
				fileSizeStr =  "%5dB" % fileSize
				if fileSize >= 1000000:
					fileSize = fileSize / 1000000
					fileSizeStr =  "%4dMB" % fileSize
				elif fileSize >= 1000:
					fileSize = fileSize / 1000
					fileSizeStr = "%4dKB" % fileSize

				fileDate = time.strftime("%Y-%m-%d %X",time.localtime(os.path.getmtime(fileName)))

				print "\t%d %s %s %s"%(fileIndex, fileDate, fileSizeStr, _file)
				fileIndex += 1


	def EveryFile(self):
		"""给出库中所有文件的完整路径
		"""
		for fileDir in self.directory:
			files = self.fileDict[fileDir]
			for one in files:
				yield fileDir + os.sep + one


	def EveryFileInDir(self, dirID):
		"""迭代给出库中第N个文件夹中所有文件的完整路径
		"""
		fileDir = self.directory[dirID]
		files = self.fileDict[fileDir]
		for one in files:
			yield fileDir + os.sep + one


	def FilesInDir(self, dirID):
		"""返回含有库中第N个文件夹中所有文件的完整路径的列表
		"""
		fileDir = self.directory[dirID]
		files = self.fileDict[fileDir]
		return [fileDir + os.sep + one for one in files]




if __name__ == "__main__":
	from Storage import *
	# root = os.getcwd()
	# root = '/Users/cjj/Documents'
	# for root, dirs, files in WalkByStep(root, []):
	# 	print \
	# 	"root:%s"\
	# 	"\ndirs:%s"\
	# 	"\nfiles:%s"%(root, "\n".join(dirs), "\n".join(files))

	storages = Storages()
	for lib in Scaner.scan(storages):
		lib.ls()