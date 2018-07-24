from django.conf.urls import patterns, include, url
import views
from rest_framework import routers, serializers,viewsets


router = routers.DefaultRouter()
router.register(r'configuration' , views.ConfigurationViewSet)
router.register(r'task_center' , views.TaskCenterViewSet)
router.register(r'host_profile' , views.HostProfileViewSet)
#router.register(r'new_task2' , views.new_tasks)
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    (r'monitor_data/$', views.monitor_data),
    (r'graph_data/$', views.graph_data),
    (r'new_tasks/(\d+)/$',views.new_tasks),
    (r'task_result/$',views.task_result),
    
)


