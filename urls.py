from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from home.views import Home, Wizard


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', TemplateView.as_view(template_name="home.html")),
    (r'^$', Home.as_view()),
    (r'^startwizard', Wizard.as_view()),
    # Examples:
    # url(r'^$', 'testmijnervaring.views.home', name='home'),
    # url(r'^testmijnervaring/', include('testmijnervaring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
