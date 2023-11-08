import json
import pdb
import datetime

br = pdb.set_trace


fn = '../download-230414/conversations.json'
f = open(fn)
content = f.read()
f.close()

chats = json.loads(content)
chat = chats[6]
print(chat['title'])

mapping = chat['mapping']
key = list(mapping.keys())[0]
value = mapping[key]


#json_data = json.dumps(chat, indent=4)
#print(json_data)
#br()

for guid, msg in chat['mapping'].items():
	print('')
	print('guid = %s' % guid)
	message = msg['message']
	if message == None:
		continue

	create_time = message['create_time']
	date = datetime.datetime.fromtimestamp(create_time)
	date_str = date.strftime("%Y-%m-%d %H:%M:%S")
	print('date_str = %s' % date_str)

	author = message['author']
	print('role = %s' % author['role'])
	content = message['content']
	parts = content['parts']
	for part in parts:
		print(part)
		print('')




