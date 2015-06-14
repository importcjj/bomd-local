# coding:utf8
import sys
import os
import time
import shutil
from Communicator import Communicator 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class StorageMonitor(object):

    def __init__(self, storage_path):
        
        self.storage_path = storage_path

        if not 'backup' in os.listdir(self.storage_path):
            os.mkdir(self.storage_path+os.sep+'backup')
            os.mkdir(self.storage_path+os.sep+'backup'+os.sep+'articles')
            os.mkdir(self.storage_path+os.sep+'backup'+os.sep+'resources')


    def Watching(self):
        """监视仓库文件夹
        """

        self.event_handler = CreatedEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.storage_path, recursive=False)
        self.observer.start()
        print 'Watching...'
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


    def set_path(self, new_storage_path):
        """重新设定仓库路径
        """

        self.observer.stop()
        self.storage_path = new_storage_path



class CreatedEventHandler(FileSystemEventHandler):
 
    def __init__(self):
        FileSystemEventHandler.__init__(self)
 
 
    def on_created(handler,event):
        """发现新文件,推送至服务器
        """

        absolute_file_name = event.src_path
        absolute_dir_path = os.sep.join(absolute_file_name.split(os.sep)[0:-1])
        file_name = absolute_file_name.split(os.sep)[-1]

        date = time.strftime("%Y-%m-%d-%X", time.localtime())

        print absolute_file_name
        print absolute_dir_path
        

        if absolute_file_name.endswith('.html'):
            name = file_name.split('.')
            file_name = name[0]+'.'+name[3]
            essayLock = name[1]
            essayTag = name[2]
            print Communicator.Essay2server(absolute_file_name, essayLock, essayTag)
            absolute_bak_path = absolute_dir_path+os.sep+"backup"+os.sep+"articles"+os.sep+date+file_name
        else:
            print file_name
            print "资源上传慢一点哦."
            print Communicator.Resource2server(absolute_file_name)
            absolute_bak_path = absolute_dir_path+os.sep+"backup"+os.sep+"resources"+os.sep+date+file_name

        shutil.move(absolute_file_name, absolute_bak_path)


    # def on_deleted(self, event):
        # pass

    # def on_modified(self, event):
        # pass

    # def on_moved(self, event):
        # pass


if __name__ == "__main__":
    absolute_path = "/Users/cjj/Documents"
    sm = StorageMonitor(absolute_path)
    sm.Watching()