from django.contrib.gis import admin

from .models import Advertising

admin.site.register(Advertising, admin.OSMGeoAdmin)

# class ProfileAdmin(admin.OSMGeoAdmin):
#     default_lon = 4422232
#     default_lat = 5985350
#     default_zoom = 12

#     model = Advertising

#     # fields = '__all__'

# admin.site.register(ProfileAdmin)