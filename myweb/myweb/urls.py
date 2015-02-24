from django.conf.urls import patterns, include, url
from django.contrib import admin

from blog.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myweb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^add/$',add),
    url(r'^list/$',list),
    url(r'^blog/topic_(?P<id>[\d|\w]+?)$',blog),
    url(r'^comment/add/$',comment_add),
    (r'^.*$',home),

)
