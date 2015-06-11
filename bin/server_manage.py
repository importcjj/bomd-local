#coding:utf-8


import urllib
import urllib2


MANAGER_URL = "http://2.bomd.sinaapp.com/manage"
USERNAME = "cjj"
PASSWORD = "cjj"



def ServerMange(command, manage_url=MANAGER_URL, username=USERNAME, password=PASSWORD):
	"""
	"""

	data = {
		'command':command,
		'username':username,
		'password':password
	}
	post_data = urllib.urlencode(data)

	manage_req = urllib2.Request(manage_url)
	manage_req.add_data(post_data)

	try:
		return urllib2.urlopen(manage_req).read()
	except urllib2.URLError as e:
		return "网络问题"




if __name__ == "__main__":
	while True:
		command = raw_input("Input cmd: ")
		print ServerMange(command)