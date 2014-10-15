# -*- coding: utf8 -*-

#Загружаем стандартные библиотеки
import sys, logging, configparser
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

#Загружаем самописные модули
import webmon

#Создаем приложение
app = Flask(__name__)
app.config.from_object(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')

def load_config():
	config = configparser.ConfigParser()
	config.read('webmon.cfg')
	default = config['DEFAULT']
	return default['IP'], default['PORT'], default['DEBUG'], default['URL'], default['HOSTS'], default['PAGE_PARAMETERS']

def load_template(param):
	config = configparser.ConfigParser()
	config.read('webmon.cfg')
	template = config['TEMPLATES']
	return template[param]

@app.route('/')
def main_page():
	return redirect(url_for('main'))

@app.route('/main', methods=['GET', 'POST'])
def main():
	""" Главная странийа, на которой будет выбираться конфигурация загружаемой """
	page = webmon.webmon()
	global url, hosts
	link = url + hosts
	host_list = page.parse_main_page(url = link)
	global param_page
	param = page.params(param_page)
	if request.method == 'POST':
		page_hosts = []
		for host in host_list:
			if request.form.get(host) == None:
				pass
			else:
				page_hosts.append(request.form.get(host))
		global page_hosts
		param_image = request.form['param']
		global param_image
		duration = request.form['duration']
		global duration
		width = int(request.form['width'])
		global width
		height = int(request.form['height'])
		global height
		return redirect(url_for('images'))
	return render_template('main.html', sort = sorted(host_list), param = param)

@app.route('/images')
def images():
	""" Страница отображения графиков """
	page = webmon.webmon()
	global url, hosts
	link = url + hosts
	host_list = page.parse_main_page(url = link)
	template = load_template(param_image)
	images = {}
	for host in page_hosts:
		tmp = template % host
		link_tmp = url + tmp
		images.update(page.parse_param_page(host, url, link_tmp, duration))
	return render_template('show_images.html', sort = sorted(page_hosts), images = images, param_image = param_image, \
		duration = duration, width = width, height = height, page_ids = page_hosts)

if __name__ == '__main__':
	ip, port, debug, url, hosts, param_page = load_config()
	app.run(host = str(ip), port = int(port), debug = str(debug))