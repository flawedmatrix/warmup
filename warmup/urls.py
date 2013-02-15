from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup.views.home', name='home'),
    # url(r'^warmup/', include('warmup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    url(r'^TESTAPI/resetFixture$', 'users.views.TESTAPI_resetFixture'),
    url(r'^TESTAPI/unitTests$', 'users.views.TESTAPI_unitTests'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/flawedmatrix/Desktop/projects/warmup/static'}),
)
