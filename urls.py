from django.conf.urls import url, include
from django.contrib import admin
from rest import urls as urls_rest

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include(urls_rest)),
    url(r'^', include('snippets.urls')),
]