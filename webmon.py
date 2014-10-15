# -*- coding: utf8 -*-

import urllib2, sys, logging
import lxml.html as html 
from grab import Grab

class webmon:
#	def load_page(self, url):
#		""" Получаем страницу """
#		self.url = Grab()
#		self.url.go(url)
		#print response.read()
		#return self.response

	def parse_main_page(self, url):
		""" Парсим страницу на наличие ссылок"""
		self.url = Grab()
		self.url.go(url)
		host_list = {}
		for elem in self.url.xpath_list('//a'):
			#print elem.text
			text = elem.text
			if "None" in str(text):
				pass
			elif "Reestr" in text:
				pass
			elif "Config" in text:
				pass
			elif "MIBs" in text:
				pass
			elif "History" in text:
				pass
			elif "Hosts list" in text:
				pass
			elif text[0] == 'i':
				pass
			else:
				#print text, elem.get('href')
				host_list[text] = elem.get('href')
		return host_list

	def parse_param_page(self, host, url, link_tmp, duration):
		""" Парсим страничку необходимых параметров """
		self.url.go(link_tmp)
		image = {}
		for elem in self.url.xpath_list('//a'):
			if elem.text == 'Hour' and 'height' in elem.get('href'):
				#print elem.text, elem.get('href')
				""" Получаем ссылку на картинку необходимой длительности """
				link = elem.get('href')
				link = link.split('&')
				link[2] = link[2].split('=')[0] + '=' + str(duration)
				tmp = ''
				for i in link:
					tmp += i + '&'
				image[host] = url + tmp[:-1]
		return image
		
	def params(self, param_page):
		""" Получаем список параметров, которые можно посмотреть """
		param = []
		self.url.go(param_page)
		for elem in self.url.xpath_list('//a'):
			elem = str(elem.text)
			if "None" in elem:
				pass
			elif 'svc' in elem:
				param.append(elem)
			elif 'sys' in elem:
				param.append(elem)
		return param


	def __del__(self):
		print "Страница удалена."

