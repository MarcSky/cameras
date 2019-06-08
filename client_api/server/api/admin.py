from django.contrib.gis import admin

from .models import Advertising, Buildings, Green, Ntopoly

class AdvertisingAdmin(admin.OSMGeoAdmin):
    default_lon = 4422232
    default_lat = 5985350
    default_zoom = 12

    model = Advertising
    
class BuildingsAdmin(admin.OSMGeoAdmin):
    default_lon = 4422232
    default_lat = 5985350
    default_zoom = 12

    model = Buildings

class GreenAdmin(admin.OSMGeoAdmin):
    default_lon = 4422232
    default_lat = 5985350
    default_zoom = 12

    model = Green

class NtopolyAdmin(admin.OSMGeoAdmin):
    default_lon = 4422232
    default_lat = 5985350
    default_zoom = 12

    model = Ntopoly


admin.site.register(Advertising, AdvertisingAdmin)
admin.site.register(Buildings, BuildingsAdmin)
admin.site.register(Green, GreenAdmin)
admin.site.register(Ntopoly, NtopolyAdmin)

# class ProfileAdmin(admin.OSMGeoAdmin):
#     default_lon = 4422232
#     default_lat = 5985350
#     default_zoom = 12

#     model = Advertising

#     # fields = '__all__'

# admin.site.register(ProfileAdmin)