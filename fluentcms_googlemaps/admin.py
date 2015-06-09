from django.contrib import admin
from .models import MarkerGroup, Marker


class MarkerGroupAdmin(admin.ModelAdmin):
    """
    Admin for creating collections of markers.
    """


class MarkerAdmin(admin.ModelAdmin):
    """
    Admin for markers.
    """
    list_display = ('title', 'group',)
    list_filter = ('group',)
    list_select_related = True


admin.site.register(MarkerGroup, MarkerGroupAdmin)
admin.site.register(Marker, MarkerAdmin)
