from django.contrib import admin
from .models import Roads, Route, Addresses

admin.site.register(Roads)
admin.site.register(Route)

class AddressesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Addresses, AddressesAdmin)


