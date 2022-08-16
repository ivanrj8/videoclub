# Videoclub Online

> Acceso Directo: https://videoclub-estrenos.herokuapp.com

## Índice
- [Descripción](#descripcion)
- [Tecnologías](#tecnologias)
- [Requisitos Previos](#requisitos-previos)
- [Ejecución](#ejecucion)

------------------------------------------------
------------------------------------------------

<a id="descripcion">
<h2>Descripción</h2>
</a>

Éste es el repositorio del proyecto sobre un videoclub online que centraliza los últimos estrenos de las principales plataformas de streaming españolas.
Se ha creado en Django sobre el lenguaje de Python en la parte de backend, utilizando en el front HTML, CSS, Javascript, JQuery y Bootstrap. Ajax para realizar la conexión asíncrona entre ambas partes. También PostgreSQL como sistema de gestión de bases de datos relacional. 
La utilidad de esta aplicación es la de conocer los últimos estrenos semanales y ser capaz de añadir a una videoteca personal tus estrenos deseados. 
Por medio de la interfaz se podrá visualizar una tabla general en forma de estanterías con los estrenos de cada plataforma.
También, desde las pestañas superiores del menú se podrá acceder a las plataformas de forma independiente y conocer estrenos próximos, además del espacio personal con tus estrenos favoritos, siendo capaz de modificarlos e iniciar y cerrar sesión.

<a id="tecnologias">
<h2>Tecnologías</h2>
</a>

- Backend: Python + Django 
- Frontend: HTML y CSS + Javascript + JQuery + Bootstrap + Ajax 
- BBDD: PostreSQL

<a id="requisitos-previos">
<h2>Requisitos previos</h2>
</a>

- Django version 4 o superior. 
- Other requirements: Pillow (5.0.0), django-ckeditor (5.4.0), bs4 (0.0.1), gunicorn (20.1.0), whitenoise (6.1.0), psycopg2 (2.9.3)

<a id="ejecucion">
<h2>Ejecución</h2>
</a>

Para ejecutar la aplicación es necesario ejecutar el siguiente comando: "python manage.py runserver".

Si se ejecuta directamente a través de la aplicación alojada en el servidor Heroku tan sólo hay que pinchar en el enlace <a> https://videoclub-estrenos.herokuapp.com </a> pudiendo tardar unos segundos al ser de alojamiento gratuito.
