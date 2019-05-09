import requests as rq
import threading
from bs4 import _s
from queue import Queue
import time

starttime=time.time()
base=r'https://www.jianshu.com/recommendations/users?page='
#headers 用来伪装浏览器的请求头，不然请求会被简书拒绝
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
#把爬取到的结果写到下面的文件里
dest_file=r'C:\names.txt'
#使用的线程数
thread_num=10
q=Queue()
all_name=''
#爬取100页的内容
for i in range(1,100,1):
	q.put(base+str(i))
	
class mth(threading.Thread):
	def __init__(self,q,id):
		threading.Thread.__init__(self)
		self.q=q
		self.id=id
	def run(self):
		while True:
			try:
				u=q.get(block=True,timeout=2)
				crawl(u,threading.current_thread().name)
			except Queue.Empty :
				print("queue is empty!")
				break
			
			
def crawl(ul,t_name):
	res=rq.get(ul,headers=headers)
	soup=_s(res.text, 'lxml')
	all=soup.findAll('h4',class_='name')
	names='\n'.join([a.text.strip() for a in all])
	print(ul,t_name)
	global all_name
	all_name = all_name+names
t_list=[]
for t in range(thread_num):
	t=mth(q,t)
	t_list.append(t)
	t.start()
for tl in t_list:
        tl.join()

print('crawl completed!')
	
with open(dest_file,'a+') as fl:
	fl.write(all_name)
print('end.............')
endtime=time.time()
print(endtime-starttime)
			

    
