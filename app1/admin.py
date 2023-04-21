from django.contrib import admin
from .models import Ticket, Comentario, Estado, Prioridad

class TicketAdmin(admin.ModelAdmin):
    # readonly_fields = ("fecha_creacion", "fecha_actualizacion",)
    readonly_fields = ("fecha_creacion",)

# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comentario)
admin.site.register(Estado)
admin.site.register(Prioridad)