from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'calc.views.index', name='home'),
    url(r'^add/$', 'calc.views.add', name='add'),
    #url(r'^add/(\d+)/(\d+)/$', 'calc.views.add2', name='add2'),
    url(r'^add/(\d+)/(\d+)/$','calc.views.old_add2_redirect'),
    url(r'^new_add/(\d+)/(\d+)/$','calc.views.add2',name='add2'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
