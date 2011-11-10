from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from home.views import Home, Wizard, Step, StoreSelection, ProcessTest, ProcessStep3, SubmitTest, ThankYou, IE7Test #,ThankYouIE7


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', TemplateView.as_view(template_name="home.html")),
    (r'^$', Home.as_view()),
    (r'^startwizard', Wizard.as_view()),
    #(r'^wizard', 'home.views.step'),
    (r'^wizard', Step.as_view()),
    (r'^storeselection', StoreSelection.as_view()),
    (r'^processtest', ProcessTest.as_view()),
    (r'^processtoekomst', ProcessStep3.as_view()),
    (r'^submittest', SubmitTest.as_view()),
    (r'^thankyou', ThankYou.as_view()),
    (r'^colo', include('colo.urls')),
    ('^ie7test', IE7Test.as_view()),
    #('^ie7thankyou', ThankYouIE7.as_view()),
    # Examples:
    # url(r'^$', 'testmijnervaring.views.home', name='home'),
    # url(r'^testmijnervaring/', include('testmijnervaring.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
