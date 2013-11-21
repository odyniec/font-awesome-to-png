import sys
import BeautifulSoup
# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

c = open("cheatsheet.html").read()
b = BeautifulSoup.BeautifulSoup(c)
d = {}
for i in b.findAll("div"):
    if 1 == len(i.findAll("i")):
        if "&amp;#" in i.text:
            sp = i.text.split("fa")
            code = sp[0].replace("&#xf", "")
            name = "fa"+sp[1].split("(")[0]

            #d[name] = unichr(int(eval("0x"+code)))
            #print code, eval("0x"+code)

            print '"'+name+'": ' + 'u("\uf' + code + '"),'


            #"
