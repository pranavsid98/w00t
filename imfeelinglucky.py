#! python 3
#lucky.py - opens several Google search results
# uses beautiful soup module

import sys, webbrowser, pyperclip, bs4, requests

print('Googling...')
#check for argument
if len(sys.argv)>1:
    getURL=' '.join(sys.argv[1:])
else:
    #if no argument, use the clipboard text
    getURL=pyperclip.paste()

#go to the desired google search results page
res=requests.get('http://google.com/search?q='+getURL)

#check the status
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' %(exc))

#retrieve top search results
soup=bs4.BeautifulSoup(res.text, "html.parser")

#open browser tab for each result
linkElems=soup.select('.r a') #r class and a element
numOpen=min(5, len(linkElems))
for i in range(numOpen):
    webbrowser.open('http://google.com'+linkElems[i].get('href'))
