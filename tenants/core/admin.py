
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import (User, Inquilino, Garante, Lugar, Contrato, Direccion, Pago)

# Register your models here.

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy


class MyAdminSite(AdminSite):

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Admin')
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Ofelia')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Administración de Ofelia')


admin_site = MyAdminSite()

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)


class LugarAdmin(admin.ModelAdmin):
    list_display = ('direccion_ciudad', 'direccion', 'nota')

    def nota(self, obj):
        nota = ''
        if obj.departamento:
            nota += "Dpto {}".format(obj.departamento)
        if obj.descripcion:
            nota += obj.descripcion
        return nota

    def direccion_ciudad(self, obj):
        return obj.direccion.ciudad

    direccion_ciudad.admin_order_field = 'direccion__ciudad'
    direccion_ciudad.short_description = 'Ciudad'


class DireccionAdmin(admin.ModelAdmin):
    list_display = ('ciudad', 'calle', 'altura')


class ContratoAdmin(admin.ModelAdmin):
    list_display = ('lugar', 'inquilino', 'fecha_firma', 'activo', 'firmado')


class GaranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'contratos', 'activo')

    def nombre(self, obj):
        return "{}, {}".format(obj.last_name.title(), obj.first_name.title())
    nombre.short_description = 'Nombre'

    def documento(self, obj):
        return "{}: {} ({})".format(obj.tipo_documento,
                                    obj.documento_numero,
                                    obj.pais_nacimiento)

    def contratos(self, obj):
        filter = Contrato.objects.filter(garantes=obj) \
                                 .values_list('fecha_firma__year',
                                              'lugar__direccion__calle') \
                                 .order_by('-fecha_firma')
        if not filter.exists():
            return None

        return ["{} - {}".format(contrato[0], contrato[1].title()) for contrato in filter]

    contratos.empty_value_display = "Sin Contrato"


class PagoAdmin(admin.ModelAdmin):
    list_display = ('inquilino', 'origen', 'monto_formato')

    def monto_formato(self, obj):
        return '$ %.2f' % obj.monto


class InquilinoAdmin(admin.ModelAdmin):

    list_display = ('nombre', 'contratos', 'activo', 'documento', 'CBU')

    def nombre(self, obj):
        return "{}, {}".format(obj.last_name.title(), obj.first_name.title())
    nombre.short_description = 'Nombre'

    def documento(self, obj):
        return "{}: {} ({})".format(obj.tipo_documento,
                                    obj.documento_numero,
                                    obj.pais_nacimiento)

    def contratos(self, obj):
        filter = Contrato.objects.filter(inquilino=obj) \
                                 .values_list('fecha_firma__year',
                                              'lugar__direccion__calle') \
                                 .order_by('-fecha_firma')
        if not filter.exists():
            return None

        return ["{} - {}".format(contrato[0], contrato[1].title()) for contrato in filter]

    contratos.empty_value_display = "Sin Contrato"

admin_site.register(Direccion, DireccionAdmin)
admin_site.register(Lugar, LugarAdmin)
admin_site.register(Inquilino, InquilinoAdmin)
admin_site.register(Garante, GaranteAdmin)
admin_site.register(Contrato, ContratoAdmin)
admin_site.register(Pago, PagoAdmin)

