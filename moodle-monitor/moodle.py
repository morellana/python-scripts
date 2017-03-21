#!/usr/bin/python

# Sistema de alerta de nuevos archivos en plataforma Moodle - Educandus

# estructura curso json
# array ( {"name": name, "entries": entires}, {"name": name, "entries": entries})


import cookielib
import urllib
import urllib2
import re
import json
import pynotify
import time
import datetime
import netifaces
import os.path

INTERVAL_TIME = 20       # minutos
RETRY_TIME    = 10       # minutos
NEXT_RUN = INTERVAL_TIME
INTERFACE     = "wlan0;eth0"

def interface_up(interfaces):
	for interface in interfaces.split(";"):
		if interface in netifaces.interfaces():
			if netifaces.AF_INET in netifaces.ifaddresses(interface):
				return True
	return False


def find_courses_id(content):
	return re.findall(r'data-courseid="(.*?)"', content)


def find_courses_name(content):
	coincidences = re.findall(r'<title>Curso: (.*?) -.*</title>', content)
	if len(coincidences) == 1:
		return coincidences[0]


def find_entries(content):
	return re.findall(r'<span class="instancename">(.*?)<', content)


def notify(entryName, courseName):
	text = "Nueva entrada <b>" + entryName +"</b> en " + courseName
	pynotify.init("markup")
	n = pynotify.Notification("Educandus", text)
	n.show()


def write_entries (content):
	f = open("moodle_info", "w")
	f.write(content)
	f.close()


def read_entries ():
	f = open("moodle_info", "r")
	content = f.read()
	f.close()
	return content


# verdadero si nada ha cambiado
def compare (recentContent):
	oldContent = read_entries()
	oldContent = json.loads(oldContent)
	sameContent = True

	if len(oldContent) == len(recentContent): # misma cantidad de cursos
		for i in range (0, len(recentContent)):
			for entry in recentContent[i]["entries"]:
				if entry not in oldContent[i]["entries"]:
					print "Nueva entrada " + entry + " en " + recentContent[i]["name"]
					notify(entry, recentContent[i]["name"])
					time.sleep(3)
					sameContent = False
	else:
		print "oldContent: " + str(len(oldContent))
		print "recentContent: " + str(len(recentContent))
		sameContent = False

	return sameContent


def check():
	try:
		req = urllib2.Request('http://lms.educandus.cl/login/index.php',data)	
		res = opener.open(req)
		login_html = res.read()

		courses = find_courses_id(login_html)
		array = []

		for course in courses:
			content = opener.open('http://lms.educandus.cl/course/view.php?id='+course).read()
			courseName    = find_courses_name(content)
			print courseName
			courseEntries = find_entries(content)
			array.append({"name": courseName, "entries": courseEntries})

		jsonString = json.dumps(array, separators=(',', ': '))
		recentContent = json.loads(jsonString)

		if os.path.isfile("moodle_info") == False:
			write_entries(jsonString)

		if compare(recentContent) == False:
			print "Nuevas entradas!"
			write_entries(jsonString)
		else:
			print "Nada ha cambiado desde la ultima visita"
		return True
	except:
		print "No se pudo completar el proceso de obtener infomacion"
		return False



cookieJar = cookielib.LWPCookieJar()
opener = urllib2.build_opener(
    urllib2.HTTPCookieProcessor(cookieJar),
    urllib2.HTTPRedirectHandler(),
    urllib2.HTTPHandler(debuglevel=0))

opener.addheaders = [('User-agent', "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36")]

# datos de login
forms = {"username": "<usuario>", "password": "<clave>"}
data = urllib.urlencode(forms)


while True:
	print str(datetime.datetime.now())[0:-7] + "\tEjecutando..."
	if interface_up(INTERFACE) and check():
		NEXT_RUN = INTERVAL_TIME
	else:
		NEXT_RUN = RETRY_TIME
	print "NEXT_RUN: "+str(NEXT_RUN)+" minutos"
	time.sleep(NEXT_RUN * 60)
