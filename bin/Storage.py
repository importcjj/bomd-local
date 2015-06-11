#coding:utf-8

__all__ = ['Storages']

import xml.etree.ElementTree as ET
import time

from logHelper import *   #function log

def Storages():
    tree = ET.parse("../storage.xml")
    root = tree.getroot()
    StoragesInfo = list()  #仓库列表
    Storages = [storage for storage in root.iter('Storage')]
    Storage_list = []
    for storage in Storages:
        info = dict()
        info['essayType'] = []
        info['essayPath'] = []
        info['resourcePath'] = []
        try:
            info['root'] = storage.find('root').text
            if info['root'] not in Storage_list:         #防止storage.xml中重复的仓库
                Storage_list.append(info['root'])
            else:
                continue
            info['essayType'] = storage.find('essays').attrib['type'].split('|')
            info['essayPath'] = [directory.text for directory in storage.find('essays').iter('dir') if directory.text]
            info['resourcePath'] = [directory.text for directory in storage.find('resources').iter('dir') if directory.text]
        except Exception as e:
            log('log/storage.log', e.message)
        finally:
            if info['root']:
                StoragesInfo.append(StorageObj(info))    
    return StoragesInfo

class StorageObj(object):

    def __init__(self, storage):
        self.Root = storage["root"]
        self.EssayPath = storage["essayPath"]
        self.EssayType = storage["essayType"]
        self.ResourcePath = storage["resourcePath"]

    def __str__(self):
        return \
        "Root==%s"\
        "\nEssayType: \n|-%s"\
        "\nEssayPath: \n|-%s"\
        "\nResourcePath: \n|-%s"%(
                              self.Root, 
            "\n|-".join(self.EssayType), 
            "\n|-".join(self.EssayPath), 
            "\n|-".join(self.ResourcePath))


if __name__ == "__main__":
    for StorageObj in Storages():
        print StorageObj

