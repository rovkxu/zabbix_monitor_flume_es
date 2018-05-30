#!/usr/bin/env python
#-*-coding:utf-8-*-

#author=

import sys,json
import urllib2

NAME = sys.argv[1]
TYPE = sys.argv[2]
KEY = None

if NAME == "cluster":
	s_data = urllib2.Request('http://localhost:9200/_cluster/stats')
else:
	s_data = urllib2.Request('http://localhost:9200/_nodes/stats')
	Node = sys.argv[3]

response = urllib2.urlopen(s_data).read()
#print(type(response))
object_data = json.loads(response)

def zbx_fail():
	print("ZABBIX NOTSUPPORTED")
	sys.exit(2)
#��ȡ��Ⱥ��node����

def fetch_name():
	
	NodeName = []

	NodeId = object_data['nodes'].keys()
#	print(NodeId)
	for k in NodeId:
#		print(k)
		temp_nodename = object_data['nodes'][k]['name']
#		print(temp_nodename)

		NodeName.append(temp_nodename)
#	print(NodeName)

	return NodeName,NodeId


if NAME ==  "node":
#----->xxxxxNodeNamexxxx
	NodeName,NodeId = fetch_name()
#	print(NodeId,"------NodeName",NodeName)
	object_data = object_data['nodes']
#----->xxxxx
	if Node and Node in NodeName:
		for Id in NodeId:
#---->xxxx
			if object_data[Id]['name'] == Node:
#��Ⱥ������ȡ����		
				if TYPE == "index_total":
					KEY = object_data[Id]['indices']['indexing']['index_total']
#jvm heap��С
				elif TYPE == 'heap_used_in_bytes':
					KEY = object_data[Id]['jvm']['mem']['heap_used_in_bytes']
				#jvm gc young����	
				elif TYPE == 'young_collection_count':
					KEY =  object_data[Id]['jvm']['gc']['collectors']['young']['collection_count']

				#jvm gc old ����
				elif TYPE == 'old_collection_count':
					KEY = object_data[Id]['jvm']['gc']['collectors']['old']['collection_count']



elif NAME == "cluster":
	#��Ⱥ״̬
	if TYPE == 'status':
		KEY = object_data['status']
	#��Ⱥ�ڵ�����
	elif TYPE == 'node_total':
		KEY = object_data['nodes']['count']['total']
	elif TYPE == 'docs_count':
		KEY = object_data['indices']['docs']['count']


if __name__ == '__main__':

	if KEY != None:
		print(KEY)
	else:
		zbx_fail()
