import json
my_dict = {}

query = input('enter query:  ')

with open('urldatabase.json') as f:
	my_dict = json.load(f)

for key in my_dict:
   if query in my_dict[key]:
        print((str(key)+" : "+str(my_dict[key][query])).encode('utf-8'))
