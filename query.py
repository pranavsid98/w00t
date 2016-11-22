import json
my_dict = {}
p = {}
query = input('enter query:  ')

with open('pagerankdatabase.json') as f:
	p = json.load(f)

with open('urldatabase.json') as f:
	my_dict = json.load(f)

for key in my_dict:
   if query.lower() in my_dict[key]:
        print((str(key)+" : "+ str(p[key]) + " : " + str(my_dict[key][query.lower()])).encode('utf-8'))

