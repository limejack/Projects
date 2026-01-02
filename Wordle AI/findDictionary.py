from urllib.request import urlopen
from html.parser import HTMLParser
import json

class MyHTMLParser(HTMLParser):
    words = []
    def handle_starttag(self, tag, attrs):
        if len(attrs) == 1 and attrs[0][0] == 'href' and len(attrs[0][1]) == 5:
            self.words.append(attrs[0][1])

page = urlopen('https://raw.githubusercontent.com/lynn/hello-wordl/main/src/dictionary.json').read().decode()
dic = json.loads(page)
out = []
for word in dic:
    if len(word) == 5:
        out.append(word)
with open('dictionary.txt','w') as file:
    file.write('\n'.join(out))
    
