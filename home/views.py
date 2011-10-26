from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView

class Home(TemplateView):
    template_name = 'home.html'
    
class Wizard(TemplateView):
    template_name = 'wizard.html'



