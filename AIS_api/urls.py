from django.conf.urls import url
from django.contrib import admin

from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/metrics$', views.metrics_route, name='metrics_route'),
    url(r'^api/v1/metrics/post/(?P<pk>[-\w]+)/(?P<irri>[-\w]+)$', views.metrics_post, name='metrics_post'),
    url(r'^api/v1/feedbacks$', views.feedbacks_route, name='feedbacks_route'),
    url(r'^api/v1/triggers$', views.triggers_route, name='triggers_route'),
    url(r'^api/v1/triggers/startlearning$', views.start_learning, name='start_learning'),
    url(r'^api/v1/crops$', views.crops_route, name='crops_route'),
    url(r'^api/v1/users$', views.users_route, name='users_route'),
    url(r'^api/v1/users/(?P<pk>[-\w]+)$', views.user_update, name='user_update')
]
