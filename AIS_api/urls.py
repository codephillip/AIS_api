from django.conf.urls import url
from django.contrib import admin

from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/metrics$', views.metrics_route, name='metrics_route'),
]
