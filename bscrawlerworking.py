from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import json, sys
import urllib.request

sys.setrecursionlimit(10000)

url = input('enter url ')
d = {}
d_2 = {}
d_3 = {}
c = {}
p = {}
l = []
templ = []
url_base = url
count = 0
d_3[url] = []
d_3[url].append(url)
def f(url):
    global count
    global templ
    if count <= 5000:
        print("count: " + str(count))
        print('now looking into: '+url+'\n')
        count += 1
        l.append(url)
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html, "html.parser")
            d[count] = soup
            tags = soup('a')
            counter = 0
            for tag in tags:
                meow = tag.get('href',None)
                
                if "mailto" in urljoin(url,meow):
                    print("Skipping this one with a mailer")    
                elif meow == None:
                    print("skipping 'None'")
                elif '#' in meow:
                    print("Skipping Within-page elements")
                elif meow.startswith('javascript') == True:
                    print("Skippin JS elements")     
                elif (urljoin(url, meow) in l):
                    counter += 1
                    d_3[urljoin(url, meow)].append(url)
                    print("Skipping this one: " + urljoin(url,meow))    
                elif meow.startswith('http') == False:
                    templ.append(urljoin(url, meow))
                    d_3[urljoin(url,meow)] = []
                    d_3[urljoin(url,meow)].append(url)
                    counter += 1    
                else:
                    templ.append(meow)
                    d_3[meow] = []
                    d_3[meow].append(url)
                    counter += 1
            c[url] = counter
            tempurl = templ[0]
            templ.pop(0)
            f(tempurl)
        
        except urllib.error.HTTPError as err:
            print(err.code)
            tempurl = templ[0]
            templ.pop(0)
            count -= 1
            f(tempurl)

        except KeyboardInterrupt:
            print('Interrupted')



    else:
        return


f(url)
print('\n\n\n\n\n')
print('Scrapping Completed')
print('\n\n\n\n\n')

for key in d_3:
    d_3[key] = list(set(d_3[key]))

for key in d_3:
    if key in d_3[key]:
        d_3[key].remove(key)            

#print(d_3['http://bitsnewslite.pythonanywhere.com/1/'])
#print(str(c['http://bitsnewslite.pythonanywhere.com/1/']))
# for a small check, i have printed the 8th index of the list, and played around with the 8th index soup object stored in the dictionary. perfect.
#print(l[10])
#dtags = d[10]('a')
#for dtag in dtags:
#    print(dtag.get('href',None))

ctr = 0
for key in d:
    d_2[l[ctr]] = {}
    # kill all script and style elements
    for script in d[key](["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = d[key].get_text()
    text = text.lower()
    #strip all \n
    text = text.replace("\n", "")
    #replace . by " "
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    text = text.replace('"', "")
    text = text.replace(",", "")
    #stripping whitespaces
    text=text.split()

    stopwords = ['as','what','who','is','a','at','is','he','the','for','to','and','whether','or','not','by','this','no','than','himself','him','of','in','our','we','us','can','on','she','her','lot','it','their','every','from','which','that','an','his','into','its','have','all']

    resultwords  = [word for word in text if word.lower() not in stopwords]
    

    for tword in resultwords:
        if tword not in d_2[l[ctr]]:
            d_2[l[ctr]][tword] = 0
        d_2[l[ctr]][tword] += 1   
    ctr = ctr + 1    


#trial
#for key in d_2:
#    if 'Oasis' in d_2[key]:
#        print((str(key)+" : "+str(d_2[key]['Oasis'])).encode('utf-8'))
print("Writing database")

with open('urldatabase.json') as json_file:
    try:
        json_decoded = json.load(json_file)
    except ValueError:
        json_decoded = {}

for key in d_2:
    json_decoded[key] = d_2[key]

with open('urldatabase.json', 'w') as f:
    json.dump(json_decoded, f)

with open('urldatabase2.json') as json_file:
    try:
        json_decoded1 = json.load(json_file)
    except ValueError:
        json_decoded1 = {}

for key in d_3:
    json_decoded1[key] = d_3[key]

with open('urldatabase2.json', 'w') as f:
    json.dump(json_decoded1, f)

with open('pagerankdatabase.json') as json_file:
    try:
        json_decoded2 = json.load(json_file)
    except ValueError:
        json_decoded2= {}    


  

with open('cdatabase.json') as json_file:
    try:
        json_decoded3 = json.load(json_file)
    except ValueError:
        json_decoded3 = {}    

for key in c:
    json_decoded3[key] = c[key]

with open('cdatabase.json', 'w') as f:
    json.dump(json_decoded3, f)              


isize = (1/len(json_decoded))

for turl in json_decoded1:
    json_decoded2[turl] = isize

def pagerank(url):
    
    sumpr = 0
    for temurl in json_decoded1[url]:
        sumpr += (isize/json_decoded3[temurl])
    sumpr *= 0.85
    sumpr += 0.15
    json_decoded2[url] = sumpr

print("Page ranking started")

for turl in json_decoded1:
    pagerank(turl)
    
print("Page ranking done")    
#print(p['http://bitsnewslite.pythonanywhere.com/aboutus/'])   

with open('pagerankdatabase.json', 'w') as f:
    json.dump(json_decoded2, f) 

print("Database written")









