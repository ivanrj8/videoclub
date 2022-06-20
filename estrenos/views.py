from django.http import JsonResponse
from django.shortcuts import render, redirect
from estrenos.scrap import descargarIndex, descargarPlataforma, datosPeli, proximosEstrenos
from estrenos.forms import FrmLogin, FrmAddUser
from estrenos.models import Usuario, Pelicula
import json


def home(request):
    listaPelis = descargarIndex()
    pelis = json.dumps(listaPelis)
    return render(request, 'index.html', {"pelis": pelis})


def plataforma(request, plataforma):
    nombrePlataforma = plataforma
    listaPelisPlataforma = descargarPlataforma(nombrePlataforma)
    listaProxEstrenos = proximosEstrenos(nombrePlataforma)
    proxEstrenos = json.dumps(listaProxEstrenos)
    pelisPlataforma = json.dumps(listaPelisPlataforma)
    return render(request, 'plataforma.html', {"pelisPlataforma": pelisPlataforma, "proxEstrenos": proxEstrenos, "nombrePlataforma": nombrePlataforma})


def mostrarDetalles(request):
    if request.method == "GET":
        url = request.GET.get("urlPeli")
        datos = datosPeli(url)
        data = {'response': datos}
        return JsonResponse(data)


def registro(request):
    if 'login' in request.session:
        request.session['login'] = False
    frm_Log = FrmLogin()
    frm_Add = FrmAddUser()
    return render(request, 'login.html', {'form': frm_Log, 'formAdd': frm_Add})


def loginUsuario(request):
    if request.method == 'POST':
        frm_Log = FrmLogin(request.POST)
        if frm_Log.is_valid():
            usuario = buscar_Usuario(frm_Log)
            if usuario is None:
                mensaje = 'No estás registrado. Debes rellenar tus datos'
                frm_Add = FrmAddUser()
                return render(request, 'login.html', {'mensajeLogin': mensaje, 'form': frm_Log, 'formAdd': frm_Add})
            else:
                request.session['login'] = True
                request.session['nombre'] = frm_Log.cleaned_data['usuarioLogin']
                return redirect('contenido')
        else:
            mensaje = 'Hay errores en tu formulario'
            frm_Add = FrmAddUser()
            return render(request, 'login.html', {'mensajeLogin': mensaje, 'form': frm_Log, 'formAdd': frm_Add})
    else:
        return redirect('registro')


def buscar_Usuario(frm: FrmLogin):
    usuario = frm.cleaned_data['usuarioLogin']
    password = frm.cleaned_data['passwordLogin']
    try:
        usuario = Usuario.objects.get(usuario=usuario, password=password)
    except Usuario.DoesNotExist:
        return None
    else:
        return usuario


def addUser(request):
    if request.method == 'POST':
        frm_Add = FrmAddUser(request.POST)
        if frm_Add.is_valid():
            usuario = buscar_UsuarioAdd(frm_Add)
            if usuario is None:
                usuario = frm_Add.cleaned_data['usuario']
                password = frm_Add.cleaned_data['password']
                user = Usuario(usuario=usuario,
                               password=password)
                user.save()
                mensaje = 'Usuario dado de alta. Introduce Login'
                frm_Log = FrmLogin()
                return render(request, 'login.html', {'mensajeAddDone': mensaje, 'form': frm_Log, 'formAdd': frm_Add})
            else:
                mensaje = 'Ese usuario ya existe, debes logearte'
                frm_Log = FrmLogin()
                return render(request, 'login.html', {'mensajeAdd': mensaje, 'form': frm_Log, 'formAdd': frm_Add})
        else:
            mensaje = 'No has rellenado bien los datos'
            frm_Log = FrmLogin()
            return render(request, 'login.html', {'mensajeAdd': mensaje, 'form': frm_Log, 'formAdd': frm_Add})
    else:
        return redirect('registro')


def buscar_UsuarioAdd(frm: FrmAddUser):
    usuario = frm.cleaned_data['usuario']
    #password = frm.cleaned_data['password']
    try:
        usuario = Usuario.objects.get(usuario=usuario)
    except Usuario.DoesNotExist:
        return None
    else:
        return usuario


def contenido(request):
    try:
        logeado = request.session['login']
        if logeado == True:
            nombreUsuario = request.session['nombre']
            user = Usuario.objects.get(usuario=nombreUsuario)
            pelis = Pelicula.objects.filter(usuarios__usuario=nombreUsuario)
            pelisUsu = []
            contadorPelis = 0
            for p in pelis:
                contadorPelis += 1
                pelisUsu.insert(0,
                                [p.link, p.titulo, p.imagen, p.descripcion])  # En orden de pila
                if (contadorPelis == 20):
                    break
            pelisUsuario = json.dumps(pelisUsu)
            return render(request, 'videoteca.html', {'pelisUsuario': pelisUsuario, 'nombreUsuario': nombreUsuario})
        else:
            return redirect('registro')
    except:
        return redirect('registro')


def eliminar(request):
    if request.method == "GET":
        titulo = request.GET.get("titulo")
        nombreUsuario = request.session['nombre']
        user = Usuario.objects.get(usuario=nombreUsuario)
        peli = Pelicula.objects.get(titulo=titulo)
        peli.usuarios.remove(user)
        if (peli.usuarios.count() == 0):
            peli.delete()
        data = {'response': titulo}
        return JsonResponse(data)


def addPeli(request):
    try:
        logeado = request.session['login']
        if logeado == True:
            if request.method == "GET":
                url = request.GET.get("urlPeli")
                datos = datosPeli(url)
                titulo = request.GET.get("tituloPeli")
                imagen = datos[1]
                descripcion = datos[3]
                descripcion = descripcion[0:170]+'...'
                nombreUsuario = request.session['nombre']
                user = Usuario.objects.get(usuario=nombreUsuario)
                try:
                    peliRepetida = peli = Pelicula.objects.get(
                        titulo=titulo, usuarios__usuario=nombreUsuario)
                    datos[3] = "REPETIDA"
                    data = {'response': datos}
                    return JsonResponse(data)
                except:
                    peli = Pelicula(link=url, titulo=titulo, imagen=imagen,
                                    descripcion=descripcion)
                    peli.save()
                    peli.usuarios.add(user)
                    data = {'response': datos}
                    return JsonResponse(data)
        else:
            datos = "NOLOGIN"
            data = {'response': datos}
            return JsonResponse(data)
    except:
        datos = "NOLOGIN"
        data = {'response': datos}
        return JsonResponse(data)
