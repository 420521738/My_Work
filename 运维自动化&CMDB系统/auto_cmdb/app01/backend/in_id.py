

asset = file('in_asset.id')
server = file('in_server.id')


asset_list = []
server_list = []
for i in asset.readlines():
  asset_list.append(i.strip('\n'))

for i in server.readlines():
  server_list.append(i.strip('\n'))


lack_list = []
for id in asset_list:
  if id not in server_list:
	lack_list.append(id)

print lack_list
