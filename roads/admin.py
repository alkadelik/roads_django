from django.contrib import admin
from .models import Segment, Route, Addresses

admin.site.register(Segment)
admin.site.register(Route)

class AddressesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Addresses, AddressesAdmin)


