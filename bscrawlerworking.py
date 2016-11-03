from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
import json, sys

sys.setrecursionlimit(10000)

url = input('enter url ')
d = {}
d_2 = {}
l = []
templ = []
url_base = url
count = 0

def f(url):
    global count
    global templ
    if count <= 100:
        print("count: " + str(count))
        print('now looking into: '+url+'\n')
        count += 1
        l.append(url)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        d[count] = soup
        tags = soup('a')

        for tag in tags:
            meow = tag.get('href',None)
            
            if (urljoin(url, meow) in l):
                print("Skipping this one: " + urljoin(url,meow))
            elif "mailto" in urljoin(url,meow):
                print("Skipping this one with a mailer")    
            elif meow == None:
                print("skipping 'None'")
            elif '#' in meow:
                print("Skipping Within-page elements")    
            elif meow.startswith('http') == False:
                templ.append(urljoin(url, meow))    
            else:
                templ.append(meow)
        tempurl = templ[0]
        templ.pop(0)
        f(tempurl)

    else:
        return


f(url)
print('\n\n\n\n\n')
print('Scrapping Completed')
print('\n\n\n\n\n')

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
with open('urldatabase.json', 'w') as f:
    json.dump(d_2, f)

print("Database written")


