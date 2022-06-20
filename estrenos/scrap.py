import urllib
import urllib.request
import urllib.error
import re
from bs4 import BeautifulSoup

# Prompt inicial
print('Web scrapping de la web filmaffinity.com')

# Definición de función de descarga de la URL


def download(url, user_agent="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", num_retries=1):
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url=url, headers=headers)
    try:
        html = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        print("Download error:", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # Reintento para errores HTTP 5XX
                return download(url, user_agent, num_retries - 1)
    return html

# Definición de la función que comprueba qué peliculas descargar y hace la llamada a download


def descargarIndex():

    # Contador de películas descargadas
    contadorPelisTotales = 0

    # Listado que contendrá las caracteristicas de las películas
    pelisTotales = []

    url = "https://www.filmaffinity.com/es/main.html"
    page = download(url)

    if page is None:
        print("Page does not exist")
    else:
        linkPlataforma = download(url)
        soup = BeautifulSoup(linkPlataforma, 'html.parser')
        # extraigo caracteristicas
        divEscogidos = soup.find_all(
            'div', attrs={'class': 'catrd-container'})
        for d in divEscogidos[2:8]:
            pelisPlataforma = d.find_all(
                'div', attrs={'class': 'padding-movie-catrd'})
            for p in pelisPlataforma[0:8]:
                contadorPelisTotales += 1
                link = p.a["href"]
                titulo = p.a.img["alt"]
                imagen = p.a.img["src"]
                fecha = p.a.findChildren()[2].contents[2]
                fecha = fecha.replace('(', '').replace(')', '')
                pelisTotales.append([link, titulo, imagen, fecha])
            # print(pelisTotales)
    print('Terminado. Películas descargadas: ', contadorPelisTotales)
    return pelisTotales

# descargarIndex()


def descargarPlataforma(nombrePlataforma):

    contadorPelisTotales = 0

    pelisTotales = []

    nombresPlataformas = ["NETFLIX", "HBO-MAX",
                          "PRIME-VIDEO", "DISNEY-PLUS", "MOVISTAR-PLUS", "FILMIN"]
    plataformas = ["new_netflix", "new_hbo_es", "new_amazon_es",
                   "disneyplus", "new_movistar_f", "new_filmin"]

    posicion = nombresPlataformas.index(nombrePlataforma)

    url = "https://www.filmaffinity.com/es/category.php?id=" + \
        plataformas[posicion]

    page = download(url)

    if page is None:
        print("Page does not exist")
    else:
        linkPlataforma = download(url)
        soup = BeautifulSoup(linkPlataforma, 'html.parser')
        divEscogidos = soup.find_all(
            'div', attrs={'class': 'movie-poster'})
        contadorPelisPlataforma = 0
        for d in divEscogidos:
            contadorPelisPlataforma += 1
            contadorPelisTotales += 1
            link = d.a["href"]
            titulo = d.a["title"]
            imagen = d.a.img["src"]
            f = d.a.findChildren()[1].contents[0:3:2]
            fecha = ' de '.join(f)
            pelisTotales.append([link, titulo, imagen, fecha])
            if (contadorPelisPlataforma == 20):
                break
    # print(pelisTotales)
    print('Terminado. Películas descargadas: ', contadorPelisTotales)
    return pelisTotales


# descargarPlataforma("NETFLIX")

def proximosEstrenos(nombrePlataforma):

    contadorPelisTotales = 0

    pelisTotales = []

    nombresPlataformas = ["NETFLIX", "HBO-MAX",
                          "PRIME-VIDEO", "DISNEY-PLUS", "MOVISTAR-PLUS", "FILMIN"]
    plataformas = ["netflix", "hbo_es", "amazon_es",
                   "disneyplus", "movistar_f", "filmin"]

    posicion = nombresPlataformas.index(nombrePlataforma)

    url = "https://www.filmaffinity.com/es/rdcat.php?id=upc_" + \
        plataformas[posicion]

    page = download(url)

    if page is None:
        print("Page does not exist")
    else:
        linkPlataforma = download(url)
        soup = BeautifulSoup(linkPlataforma, 'html.parser')
        # extraemos link, titulo e imagen
        divEscogidos = soup.find_all(
            'div', attrs={'class': 'top-movie'})
        contadorPelisPlataforma = 0

        for d in divEscogidos:
            izquierda = d.find(
                'div', attrs={'class': 'mc-left'})
            derecha = d.find(
                'div', attrs={'class': 'mc-right'})
            contadorPelisPlataforma += 1
            contadorPelisTotales += 1
            link = derecha.a["href"]
            titulo = derecha.a["title"]
            # sinopsis = derecha.findChildren(
            #    'a', attrs={'class': 'synop-text'})[0].get_text()
            imagen = izquierda.a.img["src"]
            fecha = d.findChildren(
                'span', attrs={'class': 'date'})[0].get_text()
            pelisTotales.append([link, titulo, imagen, fecha])
            if (contadorPelisPlataforma == 20):
                break

    print('Terminado. Películas descargadas: ', contadorPelisTotales)
    return pelisTotales

# proximosEstrenos("NETFLIX")


def datosPeli(urlPeli):

    page = download(urlPeli)

    if page is None:
        print("Page does not exist")
    else:
        linkPlataforma = download(urlPeli)
        soup = BeautifulSoup(linkPlataforma, 'html.parser')
        # extraemos link, titulo e imagen
        izquierda = soup.find(
            'div', attrs={'id': 'left-column'})
        derecha = soup.find(
            'div', attrs={'id': 'right-column'})
        try:
            titulo = izquierda.findChildren("dd")[0].get_text()
        except:
            titulo = " - "
        try:
            imagen = derecha.a["href"]
        except:
            imagen = " - "
        try:
            anio = izquierda.findChildren(
                'dd', attrs={'itemprop': 'datePublished'})[0].get_text()
        except:
            anio = ""
        try:
            duracion = izquierda.findChildren(
                'dd', attrs={'itemprop': 'duration'})[0].get_text()
        except:
            duracion = ""
        try:
            sinopsis = izquierda.findChildren(
                'dd', attrs={'itemprop': 'description'})[0].get_text()
        except:
            sinopsis = "No disnponible"
        try:
            pais = izquierda.find(
                'img', attrs={'class': 'nflag'})["alt"]
        except:
            pais = "No disponible"
        try:
            genero = izquierda.find(
                'dd', attrs={'class': 'card-genres'}).find_all('a')
            generos = []
            for g in genero:
                generos.append(g.get_text())
        except:
            generos = "No disponible"
        try:
            director = izquierda.find(
                'dd', attrs={'class': 'directors'}).div.find_all('span', attrs={'itemprop': 'name'})
            directores = []
            for d in director:
                directores.append(d.get_text())
        except:
            directores = "Información no disponible"
        try:
            reparto = izquierda.find(
                'dd', attrs={'class': 'card-cast'}).div.find_all('span', attrs={'itemprop': 'name'})
            actores = []
            for r in reparto:
                actores.append(r.get_text())
        except:
            actores = "Información no disponible"
        try:
            link = derecha.findChildren(
                'div', attrs={'id': 'stream-wrapper'})[0].a["href"]
        except:
            link = "404"

        datos = [titulo, imagen, duracion, sinopsis,
                 pais, generos, directores, actores, link, anio]

    return datos

# datosPeli("")
