from django.conf.urls import patterns, include, url
from django.contrib import admin
from app01 import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'day12django.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^userlist/(?P<id>\d*)', views.List),
    url(r'^adminstrator/', include(admin.site.urls)),
    url(r'^index/', views.Model),
    url(r'^temp/', views.Temp),
    url(r'^loop/', views.ModelLoop),
    url(r'^login/', views.Login),
    url(r'^son/', views.Son),
)
