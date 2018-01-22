from django.conf.urls import url, include
from django.contrib import admin

import fluentcms_googlemaps.urls

urlpatterns = [
    url('^admin/', admin.site.urls),
    url(r'^api/googlemaps/', include(fluentcms_googlemaps.urls)),
]
