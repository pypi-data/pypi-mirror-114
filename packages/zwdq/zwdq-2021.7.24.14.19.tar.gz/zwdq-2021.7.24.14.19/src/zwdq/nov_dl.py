# -*- coding:UTF-8 -*-
# pyinstaller -F -w biqukan/biqukan.py
from bs4 import BeautifulSoup
import requests, sys
import json
import tkinter 
import tkinter.ttk
import threading
import time
import re
import os
"""
类说明:下载《笔趣看》网小说各类小说
Parameters:
	无
Returns:
	无
Modify:
	2017-09-13
"""

s = requests.session()
s.keep_alive = False

# 建立目录
def mkdir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

class nov_dl(object):
	def __init__(self):
		self.server = r'http://www.biqukan.com/'
		'''
		with open('biqukan/url.json', 'r', encoding = 'utf-8') as f:
			self.url_data = json.load(f)
		'''
		self.url_data = dict()
		self.book_name = ""
		self.save_path = r"G:\\nextcloud\\小说\\爬虫下载\\"
		#self.save_path = "/Users/qiuqiandong/Documents/mycode/novel/"
		self.target = []
		self.names = []			#存放章节名
		self.urls = []			#存放章节链接
		self.nums = 0			#章节数
	"""
	函数说明:获取下载链接
	Parameters:
		无
	Returns:
		无
	Modify:
		2017-09-13
	"""
	def get_download_url(self):
		headers = { 'Accept':'application/json, text/plain, */*', 'Accept-Language':'zh-CN,zh;q=0.8', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36' }
		proxies={
			'http':'127.0.0.1:8080'
			}
		req = requests.get(
			url = self.target,
			headers=headers,
			#proxies = proxies,
			#verify=False
			)
		req.encoding = "gbk"
		html = req.text
		div_bf = BeautifulSoup(html)
		div = div_bf.find_all('div', class_ = 'listmain')
		a_bf = BeautifulSoup(str(div[0]))
		a = a_bf.find_all('a')
		self.nums = len(a[12:])								
		#剔除不必要的章节，并统计章节数
		for each in a[12:]:
			self.names.append(each.string)
			self.urls.append(self.server + each.get('href'))

	"""
	函数说明:获取章节内容
	Parameters:
		target - 下载连接(string)
	Returns:
		texts - 章节内容(string)
	Modify:
		2017-09-13
	"""
	def get_contents(self, target):
		req = requests.get(url = target)
		html = req.text
		bf = BeautifulSoup(html)
		texts = bf.find_all('div', class_ = 'showtxt')
		texts = texts[0].text.replace('\xa0'*8,'\n\n')
		return texts

	def search(self,search_name):
		self.author_search_list = [] 		#搜索用
		self.book_search_list = [] 			#搜索用
		self.url_search_list = []		 	#搜索用
		search_target = "https://so.biqusoso.com/s.php?ie=utf-8&siteid=biqukan.com&q=" + search_name
		req = requests.get(url = search_target)
		html = req.text
		bf = BeautifulSoup(html)
		# 搜索显示的作者名单
		author_texts = bf.find_all('span', class_ = 's4')
		for each in author_texts[1:]:
			self.author_search_list.append(each.string)
		# 搜索显示的作品名单
		book_texts = bf.find_all('span', class_ = 's2')
		for each in book_texts[1:]:
			self.book_search_list.append(each.string)
		# 给作品名单 + 作品
		for i in range(len(self.book_search_list)):
			self.book_search_list[i] += ("-" + self.author_search_list[i])
		# 搜索显示的作品url名单
		for each in book_texts[1:]:
			url = re.findall('''.*href="(.*)" target=.*''',str(each))
			self.url_search_list.extend(url)
		# 覆盖json数据
		self.url_data = {k: v for k, v in zip(self.book_search_list, self.url_search_list)}
		

		

	"""
	函数说明:将爬取的文章内容写入文件
	Parameters:
		name - 章节名称(string)
		path - 当前路径下,小说保存名称(string)
		text - 章节内容(string)
	Returns:
		无
	Modify:
		2017-09-13
	"""
	def writer(self, name, path, text):
		write_flag = True
		with open(path, 'a', encoding='utf-8') as f:
			f.write(name + '\n')
			f.writelines(text)
			f.write('\n\n')

		
	# 可视化界面
	def tkinter(self):
		window = tkinter.Tk()
		window.title("qqd小说爬虫")
		#画组件
		tkinter.Label(window, text="小说名称").grid(row=0)
		tkinter.Label(window, text="搜索").grid(row=1)
		tkinter.Label(window, text="下载路径：").grid(row=2)
		tkinter.Label(window, text="下载进度：").grid(row=3)
		#e1 = tkinter.Entry(window)
		e1 = tkinter.ttk.Combobox(window)
		e2 = tkinter.Entry(window)
		#e2 = tkinter.ttk.Combobox(window)
		e3 = tkinter.Entry(window)
		e4 = tkinter.Entry(window)
		e1.grid(row=0, column=1, padx=10, pady=5)
		e2.grid(row=1, column=1, padx=10, pady=5)
		e3.grid(row=2, column=1, padx=10, pady=5)
		e4.grid(row=3, column=1, padx=10, pady=5)
		e1["values"] = list(self.url_data.keys())
		#e1.set(list(self.url_data.keys())[0])
		e1.set("")
		#e2["values"] = ["暂无","暂无"]
		#e2.set("暂无")
		e2.insert(0, "")
		e3.insert(0, self.save_path)
		e4.insert(0, "尚未开始下载 ")

		# 防卡死，打包进线程
		def thread_it(func):
			# 创建
			t = threading.Thread(target=func) 
			# 守护 !!!
			t.setDaemon(True) 
			# 启动
			t.start()
			# 阻塞--卡死界面！
			# t.join()
			
        # 按钮"聚类算法"
		def button1():
			self.target = []
			self.names = []			#存放章节名
			self.urls = []			#存放章节链接
			self.nums = 0			#章节数
			self.book_name = str(e1.get())
			self.target = self.url_data[self.book_name]
			self.save_path = str(e3.get())
			mkdir(self.save_path)
			novel_download.get_download_url(self)

			#model.novel_save()
			book_save_path = self.save_path + f'{self.book_name}.txt'
			if os.path.exists(book_save_path):
				# 大于100kb的不要删，直接关闭
				if os.path.getsize(book_save_path)/1024 > 100 : 
					e4.delete(0, "end")
					e4.insert(0, f'已存在{self.book_name}，中止爬虫')
					return
				else:
					os.remove(book_save_path)
			e4.delete(0, "end")
			e4.insert(0, f'《{self.book_name}》开始下载')
			for i in range(self.nums):
				#time.sleep(1)
				novel_download.writer(self, self.names[i], self.save_path + f'{self.book_name}.txt', novel_download.get_contents(self, self.urls[i]))
				#sys.stdout.write("  已下载:%.3f%%" %  float(i/model.nums*100) + '\r')
				#sys.stdout.flush()	
				e4.delete(0, "end")
				e4.insert(0, "%.2f%%" %  float((i+1)/self.nums*100))
			print(f"{self.book_name}下载完成")
			

		# 按钮"搜索" 
		def button2():
			search_name = str(e2.get())
			novel_download.search(self, search_name)
			if len(self.url_data) == 0:
				e2.delete(0, "end")
				e2.insert(0, "未搜索到书名")
			e1["values"] = list(self.url_data.keys())
			e1.set(list(self.url_data.keys())[0])
			

		tkinter.Button(window, text="下载", width=10, command=lambda :thread_it(button1)).grid(row=4, column=1, sticky="w", padx=10, pady=5)
		tkinter.Button(window, text="搜索", width=10, command=button2).grid(row=4, column=0, sticky="w", padx=10, pady=5)
		tkinter.Button(window, text="退出", width=10, command=window.quit).grid(row=4, column=1, sticky="e", padx=10, pady=5)
		window.mainloop()

if __name__ == "__main__":
	#book_name = input()
	model = novel_download()
	model.tkinter()

	'''
	model.get_download_url()
	print(f'《{model.book_name}》开始下载：')
	for i in range(model.nums):
		model.writer(model.names[i], model.save_path + f'{model.book_name}.txt', model.get_contents(model.urls[i]))
		sys.stdout.write("  已下载:%.3f%%" %  float(i/model.nums*100) + '\r')
		sys.stdout.flush()
	print(f'《{model.book_name}》下载完成')
	'''
