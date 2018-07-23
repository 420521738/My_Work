from django.conf.urls import patterns, include, url
import views
from rest_framework import routers, serializers,viewsets


router = routers.DefaultRouter()
router.register(r'configuration' , views.ConfigurationViewSet)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    (r'monitor_data/$', views.monitor_data),
    (r'graph_data/$', views.graph_data)
    
)


