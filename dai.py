#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import web
from web import form
from web.contrib.template import render_mako
import pymongo
#from bson.objectid import ObjectId
#from pymongo import Connection
#from pymongo.errors import ConnectionFailure
from lxml import etree
import sys
import urllib
import feedparser	
import tweepy
import time


urls = (
	'/css/(.*)', 'sirve_css',
	'/imagenes/(.*)', 'sirve_img',
	'/fonts/(.*)', 'sirve_font',
	'/login', 'sirve_login',
	'/registro', 'sirve_registro',
	'/modificar', 'sirve_modificacion',
	'/busqueda', 'busqueda',
	'/logout', 'logout',
	'/rss', 'noticias',
	'/grafica','highcharts',
	'/mapa','googlemaps',
	'/twitter','twitter',
	'/mashup','mashup',
	'/', 'index',
	'/(.*)', 'error'
)

web.config.debug = True

app = web.application(urls, globals(), autoreload=True)

#Inicializamos la variable session a cadena vacía porque inicialmente no hay ningún usuario que haya iniciado sesion
ses = web.session.Session(app, 
	web.session.DiskStore('sessions'), 
	initializer={'usuario': ""})
	
def session_hook():
	web.ctx.session=ses

app.add_processor(web.loadhook(session_hook))

plantillas = render_mako(
	directories=['templates'],
	input_encoding='utf-8',
	output_encoding='utf-8'
)

#Formularios:
login = form.Form(
	form.Textbox('username',form.notnull),
	form.Password('password',form.notnull),
	form.Button('Login'),
)

charts = form.Form(
	form.Textbox('Anio'),
	form.Textbox('Enero', form.notnull),
	form.Textbox('Febrero', form.notnull),
	form.Textbox('Marzo', form.notnull),
	form.Textbox('Abril', form.notnull),				
	form.Textbox('Mayo', form.notnull),
	form.Textbox('Junio', form.notnull),
	form.Textbox('Julio', form.notnull),
	form.Textbox('Agosto', form.notnull),
	form.Textbox('Septiembre', form.notnull),
	form.Textbox('Octubre', form.notnull),
	form.Textbox('Noviembre', form.notnull),
	form.Textbox('Diciembre', form.notnull),
	form.Button('Enviar'),
)

buscar = form.Form(#busqeda
	form.Textbox('mashup', form.notnull, description = 'Introduce la palabra clave a analizar'),
	form.Button('Buscar'),
)

# registro
vpass = form.regexp(r".{7,20}$", 'debe de tener mas de 7 caracteres y menos de 20')
vemail = form.regexp(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", "Introduzca un email valido")
vvisa = form.regexp(r"([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})|([0-9]{4})-([0-9]{4})-([0-9]{4})-([0-9]{4})", "Introduzca una VISA valida")
vname = form.regexp(r"..*", 'Introduzca su Nombre porfavor')
vapellido = form.regexp(r"..*", 'Introduzca su Apellido porfavor')
vdireccion = form.regexp(r".{4}.*", 'Introduzca su Direccion porfavor')

registro = form.Form(
	form.Textbox('Nombre',vname),
	form.Textbox('Apellidos',vapellido),
	form.Textbox('Correo Electronico',vemail),
	form.Textbox('N. VISA',vvisa),
	form.Dropdown('Fecha De Nacimiento dia',range(1,32)),
	form.Dropdown('Fecha De Nacimiento MES',range(1,13)),
	form.Dropdown('Fecha De Nacimiento ANIO',range(1980,2010)),
	form.Textarea('Direccion',vdireccion),
	form.Password('Contrasenia',vpass),
	form.Password('Verificacion',vpass),
	form.Radio('Forma de pago', [('visa','VISA'), ('reembolso', 'Contra reembolso')], form.notnull),
	form.Checkbox('Acepto Las Clausulas De Proteccion De Datos',form.Validator("Acepta las clausulas", lambda i: i == 'true'),value='true'),
	form.Button('Registro'),
	
	validators = [
		form.Validator("Las contrasenias no coinciden", lambda i: i.Contrasenia == i.Verificacion)]
	)

class index:
	def GET(self):
		form = login()
		ses =web.ctx.session
		
		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", nombre=ses.get('usuario'))

		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
		
class sirve_img:     
	def GET(self, archivo):
		try:
			paginacss = open("/home/marquina/practica4/a/contenidoEstatico/imagenes/"+archivo, "r")
			ces =paginacss.read()
			return ces
		except:
			return 'error'

class sirve_font:     
	def GET(self, archivo):
		try:
			paginafont = open("/home/marquina/practica4/a/contenidoEstatico/fonts/"+archivo, "r")
			font =paginacss.read()
			return font
		except:
			return 'error'

class sirve_css:    
	def GET(self, archivo):
		try:
			paginacss = open("/home/marquina/practica4/a/contenidoEstatico/css/"+archivo, "r")
			ces =paginacss.read()
			return ces
		except:
			return 'error'

class sirve_login:
	def GET(self):
		form = login()
		ses =web.ctx.session
		if ses.get('usuario', True):
			return plantillas.index(title="practica 4(a)", asignatura="Iniciar Sesion", nombre=ses.get('usuario'))
			
		return plantillas.index(title="practica 4(a)", asignatura="Iniciar Sesion", form=form)
					
	def POST (self):
		form =login()
		ses =web.ctx.session
		if not form.validates():
			return plantillas.index(title="practica 4(a)", asignatura="Iniciar Sesion", form=form)
		else:
			usuario = form.d.username
			passwd = form.d.password
			
			conn=pymongo.MongoClient()
			db=conn.mydb
			usuarios=db.usuarios
			us=usuarios.find_one({"Nombre":usuario,"Contrasenia": passwd})	#buscamos al usuario	
			if(str(us) == "None"):
				form.password.set_value("")
				return plantillas.index(title="practica 4(a)", asignatura="Iniciar Sesion", form=form)
			else:
				ses.usuario=usuario
				return plantillas.index(title="practica 4(a)", asignatura="Iniciar Sesion", nombre=ses.get('usuario'))

class logout:
	def GET(self):
		ses=web.ctx.session
		ses.kill()
		raise web.seeother('/')	
			
class sirve_registro:
	def GET(self):
		form = registro()
		ses =web.ctx.session
		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="Sesion iniciada no SE PUEDE REGISTRAR", nombre=ses.get('usuario'))
		
		return plantillas.index(title="BIENVENIDO", asignatura="REGISTRARSE,,,", form=form, regis="si")
		
	def POST(self):
		form = registro()
		ses =web.ctx.session			
		if not form.validates():    
			return plantillas.index(title="BIENVENIDO", asignatura="Registro no valido", form=form, regis="si")
		else:
			conn=pymongo.MongoClient()
			db=conn.mydb
			usuarios=db.usuarios           
			usuario={
			"Nombre":form['Nombre'].value,
			"Contrasenia":form['Contrasenia'].value,
			"Apellidos":form['Apellidos'].value,
			"dia":form['Fecha De Nacimiento dia'].value,
			"mes":form['Fecha De Nacimiento MES'].value,
			"anio":form['Fecha De Nacimiento ANIO'].value,
			"email":form['Correo Electronico'].value,
			"Direccion":str(form['Direccion'].value),
			"Forma de pago":form['Forma de pago'].value,
			"visa":form['N. VISA'].value}
			#Insertamos el usuario
			usuarios.insert(usuario)
			ses.usuario=form['Nombre'].value
			conn.close()
			return plantillas.index(title="practica 4(a)", asignatura="Registro realizado!!", nombre=ses.get('usuario'))
			
class sirve_modificacion:
	def GET(self):
		form = registro()
		ses =web.ctx.session
		if ses.get('usuario', True):			
			conn=pymongo.MongoClient()
			db=conn.mydb
			usuarios=db.usuarios
			us=usuarios.find_one({"Nombre":ses.get('usuario')})		
			form['Nombre'].set_value(us[u'Nombre'])
			form['Contrasenia'].set_value(us['Contrasenia'])
			form['Apellidos'].set_value(us['Apellidos'])
			form['Fecha De Nacimiento dia'].set_value(int(us['dia']))
			form['Fecha De Nacimiento MES'].set_value(int(us['mes']))
			form['Fecha De Nacimiento ANIO'].set_value(int(us['anio']))
			form['Correo Electronico'].set_value(us['email'])
			form['Direccion'].set_value(str(us['Direccion']))
			form['Forma de pago'].set_value(us['Forma de pago'])
			form['N. VISA'].set_value(us['visa'])
			conn.close()			
			return plantillas.index(title="Introduzca los nuevos datos", asignatura="Iniciar MODIFICACION",modif="/modif",form=form,nombre=ses.get('usuario'))
		
		form=login()
		return plantillas.index(title="practica 4(a)", asignatura="No puedes modificar los datos si no estas logeado", form=form)
		
	def POST(self):
		form = registro()
		ses =web.ctx.session
		if not form.validates():
			return plantillas.index(title="Modificando ejercicio4.2", asignatura="Iniciando MODIFICACION ponga bien los datos",mofi="/modif" ,form=form,nombre=ses.get('usuario'))
		else:		
			conn=pymongo.MongoClient()
			db=conn.mydb
			usuarios=db.usuarios           
			usuario={
			"Nombre":form['Nombre'].value,
			"Contrasenia":form['Contrasenia'].value,
			"Apellidos":form['Apellidos'].value,
			"dia":form['Fecha De Nacimiento dia'].value,
			"mes":form['Fecha De Nacimiento MES'].value,
			"anio":form['Fecha De Nacimiento ANIO'].value,
			"email":form['Correo Electronico'].value,
			"Direccion":str(form['Direccion'].value),
			"Forma de pago":form['Forma de pago'].value,
			"visa":form['N. VISA'].value}
			
			#Remuevo el antiguo ses.get('usuario') 			usuarios.remove({"usuario":ses.usuario})
			usuarios.remove({"Nombre":ses.get('usuario')})
			
			#Inserto el nuevo
			usuarios.insert(usuario)
			ses.usuario=form['Nombre'].value
			conn.close()
			return plantillas.index(title="practica 4(a)", asignatura="Modificacion realizada!!", nombre=ses.get('usuario'))

class MiClase:
	def __init__(self, noticias, enlaces,contador):
		self.noticiastitulo= noticias
		self.noticiasenlaces = enlaces
		self.tam=contador
	
class noticias:
	def GET(self):
		form = login()
		ses =web.ctx.session
	
		url='http://ep00.epimg.net/rss/elpais/portada.xml'
		urllib.urlretrieve(url, "portada.xml")

		d = feedparser.parse('portada.xml')

		tamanio = len(d.entries)
		noticias=[]
		enlaces=[]
		contador = 0

		while contador < tamanio:
			noticias.insert(contador, d.entries[contador].title)  # para mostrar los titulares
			aux=contador+1
			enlaces.insert(aux, d.entries[contador].link)
			contador +=2
			
		noticiasa=MiClase(noticias,enlaces,(contador-1)/2)

		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", nombre=ses.get('usuario'), noticias=noticiasa)

		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form, noticias=noticiasa)
		
class highcharts:
	def GET(self):
		ses =web.ctx.session
		form=charts()
		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="Introduzca datos para poder realizar la grafica", nombre=ses.get('usuario'),form=form,grafica1= "si")

		#web.header('Content-Type', 'text/html; charset=utf-8')
		form=login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
		#return plantillas.formulario_charts(form=f,mensaje='')
	def POST(self):
		ses =web.ctx.session
		form = charts()
		if ses.get('usuario', True):
			if not form.validates():
				return plantillas.index(title="BIENVENIDO",asignatura='Introducir datos correctamente',form=form, nombre=ses.get('usuario'),grafica1= "si")
			else:
			#web.header('Content-Type', 'text/html; charset=utf-8')
				Ingresos=[]			
				Ingresos.insert(1,form['Enero'].value)
				Ingresos.insert(2,form['Febrero'].value)
				Ingresos.insert(3,form['Marzo'].value)
				Ingresos.insert(4,form['Abril'].value)
				Ingresos.insert(5,form['Mayo'].value)
				Ingresos.insert(6,form['Junio'].value)
				Ingresos.insert(7,form['Julio'].value)
				Ingresos.insert(8,form['Agosto'].value)
				Ingresos.insert(9,form['Septiembre'].value)
				Ingresos.insert(10,form['Octubre'].value)
				Ingresos.insert(11,form['Noviembre'].value)
				Ingresos.insert(12,form['Diciembre'].value)
				Ingresos.insert(13,form['Anio'].value)
				return plantillas.index(title="BIENVENIDO",asignatura='Grafica realizada con EXITO',nombre=ses.get('usuario'),grafica=Ingresos)

		form = login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
		
class googlemaps:
	def GET(self):#			script.src = 'http://maps.googleapis.com/maps/api/js?key=AIzaSyBhPbHgeGp3rxriZ8Nnj6Ycm-T7jL-07Qw&sensor=TRUE&' + 'callback=initialize'; 				  script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp&' + 'callback=initialize';
		ses =web.ctx.session
		form=charts()
		if ses.get('usuario', True):
			return plantillas.index(title="Mapeando", asignatura="El mapa esta centrado en su geolocalizacion", nombre=ses.get('usuario'),mapa= "si")

		#web.header('Content-Type', 'text/html; charset=utf-8')
		form=login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
		
class Datostwitter:
	def __init__(self, fecha, autor,texto,busqueda,tam):
		self.fecha= fecha
		self.texto = texto
		self.autor=autor
		self.clave=busqueda
		self.tamanio=tam
		
class twitter:
	def GET(self):
		ses =web.ctx.session
		form=buscar()
		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="Introduzca datos para buscar tweets", nombre=ses.get('usuario'),form=form,twitter1= "si")

		#web.header('Content-Type', 'text/html; charset=utf-8')
		form=login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
	def POST(self):
		ses =web.ctx.session
		form = buscar()
		if ses.get('usuario', True):
			if not form.validates():
				return plantillas.index(title="BIENVENIDO",asignatura='Introducir datos correctamente para buscar tweets',form=form, nombre=ses.get('usuario'),twitter1= "si")
			else:
				#web.header('Content-Type', 'text/html; charset=utf-8')
				creado=[]
				texto=[]
				autor=[]
				consumer_key = '8WCVKxZMuLarti1uiPL71VHCX'
				consumer_secret = 'aRehFSGOTdTuUaDXGgGlTVSd2SdnmRFBCneuZlHkvDhBXDkk0U'
				access_token = '490393219-LTGxoqDmWciKFLBxMOaGSog2j20dSPngrQkuoMP1'
				access_token_secret = 'iTyEHiqWe72GvJtD946F5PJpOJh3eUrXCo2Nl3S59a1aH'
				# OAuth process, using the keys and tokens
				auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
				auth.set_access_token(access_token, access_token_secret)
				# Creation of the actual interface, using authentication
				api = tweepy.API(auth)
				# https://dev.twitter.com/docs/api/1.1/get/search/tweets
				contador=0
				for tweets in api.search(q=form['mashup'].value,count=10, result_type='recent'):
					creado.insert(contador,tweets.created_at)
					autor.insert(contador,tweets.user.screen_name)
					texto.insert(contador,tweets.text)
					contador=contador+1
					
				datos=Datostwitter(creado,autor,texto,form['mashup'].value,contador)
					
				return plantillas.index(title="BIENVENIDO",asignatura='Busqueda realizada con EXITO',nombre=ses.get('usuario'),twitterdata=datos,twitter="si")

		form = login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)

	
def dia(day):
	dias = ['Lunes','Martes','Miercoles','Jueves', 'Viernes', 'Sabado', 'Domingo']
	return dias[day]
	
def buscarnumdia(num_day_orig,num_orig,num_new):
	diferencia=abs((num_orig+1)-(num_new+1))
	if(num_orig>=num_new):
		numero=num_day_orig-diferencia
	else:
		numero=num_day_orig+diferencia
	return numero
	
class mashup:
	def GET(self):
		ses =web.ctx.session
		form=buscar()
		if ses.get('usuario', True):
			return plantillas.index(title="BIENVENIDO", asignatura="Introduzca datos para Analizar con el mashup", nombre=ses.get('usuario'),form=form,mashup1= "si")

		#web.header('Content-Type', 'text/html; charset=utf-8')
		form=login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)
	def POST(self):
		ses =web.ctx.session
		form = buscar()
		if ses.get('usuario', True):
			if not form.validates():
				return plantillas.index(title="BIENVENIDO",asignatura='Introducir datos correctamente para analizar con el mashup',form=form, nombre=ses.get('usuario'),mashup1= "si")
			else:
				#web.header('Content-Type', 'text/html; charset=utf-8')
				datos=[] #0cadena a buscar,1 anio,2mes,numero 3dia y 4nombre 5valor,6-7-8 igual...
				laFecha = time.localtime(time.time())
				datos.insert(0,form['mashup'].value)
				datos.insert(1,laFecha[0])#anio
				datos.insert(2,laFecha[1])#mes
				consumer_key = '8WCVKxZMuLarti1uiPL71VHCX'
				consumer_secret = 'aRehFSGOTdTuUaDXGgGlTVSd2SdnmRFBCneuZlHkvDhBXDkk0U'
				access_token = '490393219-LTGxoqDmWciKFLBxMOaGSog2j20dSPngrQkuoMP1'
				access_token_secret = 'iTyEHiqWe72GvJtD946F5PJpOJh3eUrXCo2Nl3S59a1aH'
				# OAuth process, using the keys and tokens
				auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
				auth.set_access_token(access_token, access_token_secret)
				# Creation of the actual interface, using authentication
				api = tweepy.API(auth)
				# https://dev.twitter.com/docs/api/1.1/get/search/tweets
				contador=1
				while contador < 8:
					name_dia=dia(contador-1)
					num_dia=buscarnumdia(laFecha[2],laFecha[6],contador-1)
					datos.insert(3*contador,num_dia)#numero de dia  que corresponde
					datos.insert(3*contador+1,name_dia)#nombre al qe corresponde
					cadena='''%s-%s-%s'''%(laFecha[0],laFecha[1],num_dia)
					cadena1='''%s-%s-%s'''%(laFecha[0],laFecha[1],num_dia+1)
					cuenta=0
					for tweets in api.search(q=datos[0], since=cadena,until=cadena1):
						cuenta=cuenta+1
					datos.insert(3*contador+2,cuenta)#numero de tweets			
					contador=contador+1
		
				return plantillas.index(title="BIENVENIDO",asignatura='mashup realizada con EXITO',nombre=ses.get('usuario'),mashupdata=datos,mashup="si")

		form = login()
		return plantillas.index(title="BIENVENIDO", asignatura="PRACTICA 4(A)", form=form)


		
if __name__ == "__main__":
	app.run()