import requests
import colorama
colorama.init()
from bs4 import BeautifulSoup

def req_file_size(req):
	try:
		return int(req.headers['content-length'])
	except:
		return 0
def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)
def get_url_file_name(url,req):
	try:
		if "Content-Disposition" in req.headers.keys():
			name = str(req.headers["Content-Disposition"]).replace('attachment; ','')
			name = name.replace('filename=','').replace('"','')
			return name
		else:
			import urllib
			urlfix = urllib.parse.unquote(url,encoding='utf-8', errors='replace')
			tokens = str(urlfix).split('/');
			return tokens[len(tokens)-1]
	except:
		import urllib
		urlfix = urllib.parse.unquote(url,encoding='utf-8', errors='replace')
		tokens = str(urlfix).split('/');
		return tokens[len(tokens)-1]
	return ''

class Client(object):
	def __init__(self,host='',user='',passw='',session=None):
		self.host = host
		self.user = user
		self.passw = passw
		self.session = requests.session()
		if session:
			self.session=session
	def login(self):
		try:
			resp = self.session.get(self.host + 'login')
			soup = BeautifulSoup(markup=resp.text,features="html.parser")
			csrfToken = soup.find("input",attrs={"name":"csrfToken"})['value']
			url_post = self.host + 'login/signIn'
			payload = {}
			payload['csrfToken'] = csrfToken
			payload['source'] = ''
			payload['username'] = self.user
			payload['password'] = self.passw
			payload['remember'] = '1'
			resp1 = self.session.post(url_post,data=payload)
			url = self.host + 'user/profile'
			resp = self.session.get(url)	
			if resp.url == url:
				print('Login Exito')
				return True
			else:
				print('No se pudo realizar el login, verifique sus credenciales')
				return False
		except:
			return False
	def download(self,url,mode):
		if mode=="1":
			urls = url.split(" ")
			print("Descargando")
			for u in urls:
				try:
					print("\n")
					req = self.session.get(u,stream=True)
					filename = get_url_file_name(u,req)
					filesize = req_file_size(req)
					try:
						file = open(filename,"wb")
					except:
						filename = filename.split(filename[:17:])[1]
						file = open(filename,"wb")
					v = 0
					for chunk in req.iter_content(1024):
						file.write(chunk)
						v+=len(chunk)
						msg = f"\r> [{sizeof_fmt(v)}] {filename}"
						print(colorama.Fore.BLUE +msg+colorama.Style.RESET_ALL, end="")
					file.close()
				except:
					pass
			again = input("\nDesea realizar otra operación? (y/n)\n> ")
			if again=="y":
				Text(session=self.session)
			else:
				print("\rGracias por usar mi servicio\n\n|| Freebootcar ||", end="")
		elif mode=="2":
			txtname = url
			if str(txtname).split('.')[-1]!='txt':
				txtname=txtname+'.txt'
			txt = open(txtname,'r')
			urls = str(txt.read()).split('\n')
			print("Descargando")
			for u in urls:
				try:
					print("\n")
					req = self.session.get(u,stream=True)
					filename = get_url_file_name(u,req)
					filesize = req_file_size(req)
					try:
						file = open(filename,"wb")
					except:
						filename = filename.split(filename[:17:])[1]
						file = open(filename,"wb")
					v = 0
					for chunk in req.iter_content(1024):
						file.write(chunk)
						v+=len(chunk)
						msg = f"\r> [{sizeof_fmt(v)}] {filename}"
						print(colorama.Fore.BLUE +msg+colorama.Style.RESET_ALL, end="")
					file.close()
				except:
					pass
			again = input("\nDesea realizar otra operación? (y/n)\n> ")
			if again=="y":
				Text(session=self.session)
			else:
				print("\rGracias por usar mi servicio\n\n|| Freebootcar ||", end="")
		elif mode=="3":
			resp = requests.get(url,stream=True)
			urls = str(resp.text).split("\n")
			print("Descargando")
			for u in urls:
				try:
					print("\n")
					req = self.session.get(u,stream=True)
					filename = get_url_file_name(u,req)
					filesize = req_file_size(req)
					try:
						file = open(filename,"wb")
					except:
						filename = filename.split(filename[:17:])[1]
						file = open(filename,"wb")
					v = 0
					for chunk in req.iter_content(1024):
						file.write(chunk)
						v+=len(chunk)
						msg = f"\r> [{sizeof_fmt(v)}] {filename}"
						print(colorama.Fore.BLUE +msg+colorama.Style.RESET_ALL, end="")
					file.close()
				except:
					pass
			again = input("\nDesea realizar otra operación? (y/n)\n> ")
			if again=="y":
				Text(session=self.session)
			else:
				print("\rGracias por usar mi servicio\n\n|| Freebootcar ||", end="")
def Text(session=None):
	client=None
	if session:
		client = Client(session=session)
	mode = input("Mánde el número del Método que desea usar:\n\n    (1) Enlaces en secuencia\n    (2) Nombre del txt guardado\n    (3) Enlace del txt [FTL]\n\n=> ")
	if mode=="1":
		datos=''
		if not session:
			datos = input("Mande sus datos en este órden\nhost user passw\n> ")
		urls = input("Mande los enlaces a descargar en secuercia:\n\nhttps://url1 https://url2 https://url3 https://urln\n\n> ")
		verify = input("\nEstos datos son correctos? (y/n)")
		if verify=="y":
			if not client:
				values = datos.split(" ")
				host = values[0]
				user = values[1]
				passw = values[2]
				client = Client(host,user,passw)
				login = client.login()
				if login:
					download =client.download(urls,"1")
			else:
				download =client.download(urls,"1")
		else:
			Text(session=session)
	elif mode=="2":
		datos=''
		if not session:
			datos = input("Mande sus datos en este órden\nhost user passw\n> ")
		urls = input("\nMande el nombre del archivo txt guardado, se descargarán los archivos en esa misma ruta\n> ")
		verify = input("\nEstos datos son correctos? (y/n)")
		if verify=="y":
			if not client:
				values = datos.split(" ")
				host = values[0]
				user = values[1]
				passw = values[2]
				client = Client(host,user,passw)
				login = client.login()
				if login:
					download =client.download(urls,"2")
			else:
				download =client.download(urls,"2")
		else:
			Text(session=session)
	elif mode=="3":
		datos=''
		if not session:
			datos = input("Mande sus datos en este órden\nhost user passw\n> ")
		urls = input("\nEnvíe el enlace del txt antes generado con el FTL\n> ")
		verify = input("\nEstos datos son correctos? (y/n)")
		if verify=="y":
			if not client:
				values = datos.split(" ")
				host = values[0]
				user = values[1]
				passw = values[2]
				client = Client(host,user,passw)
				login = client.login()
				if login:
					download =client.download(urls,"3")
			else:
				download =client.download(urls,"3")
		else:
			Text(session=session)
	else:
		print("Error")
		again = input("Desea realizar otra operación? (y/n)")
		if again=="y":
			Text(session=session)
		else:
			print("\rGracias por usar mi servicio\n\n|| Freebootcar ||", end="")
Text()