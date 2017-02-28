import urllib
import urllib2
import re
from Tkinter import *

class BBS:
	def __init__(self,index):
		self.pageindex=index
		self.url='http://bbs.seu.edu.cn/bbscon.php?bid=373&id='
		self.user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/2010    0101 Firefox/44.0'
		self.header={'User-Agent' : self.user_agent}
		self.pageCode=""
	def getLink(self):
		try:
			request=urllib2.Request(self.url+str(self.pageindex),headers=self.header)
			response=urllib2.urlopen(request)
			self.pageCode=response.read().decode('gb2312')
		except urllib2.URLError,e:
			return 0
		return 1
	def getTitle(self):
		string=re.compile('<title>.*</title>')
		items=re.findall(string,self.pageCode)
		for item in items:
			return item
		return "error"
	def getContent(self):
		string=re.compile('prints.*SBBS')
		items=re.findall(string,self.pageCode)
		for item in items:
			remove=re.compile(r"prints..")
			item=re.sub(remove,"<content>",item).strip()
			remove=re.compile(r"\\n")
			item=re.sub(remove,"\r\n",item).strip()
			return item
		return "error"
	def getnext(self):
		self.pageindex+=1
		return self.url

class Application(Frame):
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self.pack()
		self.bbs=BBS(13000)
		self.bbs.getLink()
		self.createWidgets(self.bbs.getTitle(),self.bbs.getContent())
	def createWidgets(self,title,content):
		self.nextbutton=Button(self,text="nextinfo",command=self.nextinfo)
		self.nextbutton.pack()
		self.titlelabel=Label(self,text=title)
		self.titlelabel.pack()
		self.contentlabel=Label(self,text=content,\
		wraplength=1000)
		self.contentlabel.pack()
	def nextinfo(self):
		self.bbs.getnext()
		while self.bbs.getLink()==0:
			tmptxt="connect error"+self.bbs.getnext()
			self.contentlabel.config(text=tmptxt)
		self.titlelabel.config(text=self.bbs.getTitle())
		self.contentlabel.config(text=self.bbs.getContent())

app=Application()
app.mainloop()
