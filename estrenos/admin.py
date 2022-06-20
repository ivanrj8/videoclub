from django.contrib import admin
from estrenos.models import Usuario, Pelicula

# Register your models here.


class PeliculaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "link")
    search_fields = ("titulo", "usuarios__usuario")
    list_filter = ("usuarios__usuario",)


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "password")
    search_fields = ("usuario",)
    list_filter = ("usuario",)


admin.site.register(Pelicula, PeliculaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
