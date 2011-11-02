from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import render_to_response
#from coffin.shortcuts import render_to_response
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template import RequestContext, Context
from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

from evc.models import Uitstroom, Uitstroom_Kerntaak, Uitstroom_Werkproces, Uitstroom_Ervaringstest, Uitstroom_ErvaringstestWerkproces
try: import simplejson as json
except ImportError: import json

import uuid


class Home(TemplateView):
    template_name = 'home.html'

    
class Wizard(TemplateView):
    template_name = 'wizard.html'


class Step(View):
    def get(self, request):
        return HttpResponseForbidden
    
    def post(self, request):
        #uitstroom_nr = request.session['uitstroom_nr']
        nr = request.POST.get('step_number')
        template = 'step'+str(nr)+'.html'
        uitstroom_nr = request.session.get('uitstroom_nr',None)
       
        if uitstroom_nr:
            if nr == '1':
                return render(request, template)
            elif nr == '2':
                
                uitstroom_nr = request.session['uitstroom_nr']
                uitstroom = Uitstroom.objects.get(pk=uitstroom_nr)            
                ktaken = Uitstroom_Kerntaak.objects.filter(uitstroom=uitstroom_nr)
                try:
                    test = Uitstroom_Ervaringstest.objects.get(pk=request.session['test_id'])
                except Uitstroom_Ervaringstest.DoesNotExist:
                    test = None
                
                ktaaklist = []
                
                for kt in ktaken:
                    ktaakdict = {}
                    ktaakdict['volgnummer'] = kt.volgnummer
                    ktaakdict['title'] = kt.title
                    werkprocessen = Uitstroom_Werkproces.objects.filter(kerntaak = kt.id)
                    wplist = []
                    for wp in werkprocessen:
                        wpdict = {}
                        wpdict['volgnummer'] = wp.volgnummer
                        wpdict['title'] = wp.title
                        wpdict['id'] = wp.id
                        
                        if test:
                            try:
                                testwp = Uitstroom_ErvaringstestWerkproces.objects.get(uitstroom_ervaringstest=test, uitstroom_werkproces= Uitstroom_Werkproces.objects.get(pk=wp.id))
                            except Uitstroom_ErvaringstestWerkproces.DoesNotExist:
                                testwp = None
                            
                            if testwp:
                                wpdict['score'] = testwp.score
                    
                        wplist.append(wpdict)
                    
                    ktaakdict['werkprocessen'] = wplist 
                    ktaaklist.append(ktaakdict)

                    c = {"uitstroom_nr": uitstroom_nr, "uitstroom_title": uitstroom.title, "kerntaken": ktaaklist}
                return render(request, template, c)
            elif nr == '3':
                try:
                    test = Uitstroom_Ervaringstest.objects.get(pk=request.session['test_id'])
                    c = {"evp": test.evp, "evc": test.evc, "coach": test.coach, "motivatie": test.motivatie}
                except Uitstroom_Ervaringstest.DoesNotExist:
                    test = None
                    c = {"evp": "", "evc": "", "coach": "", "motivatie": ""}

                return render(request, template, c)
            
            elif nr == '4':
                try:
                    test = Uitstroom_Ervaringstest.objects.get(pk=request.session['test_id'])
                    c = {"first_name": test.first_name, "last_name": test.last_name, "email": test.email, "zipcode": test.zipcode, "phone": test.phone}
                except Uitstroom_Ervaringstest.DoesNotExist:
                    test = None
                    c = {"first_name": "", "last_name": "", "email": "", "zipcode": "", "phone": ""}
                    
                return render(request, template, c)
                    
            else:
                return HttpResponse(request.session['uitstroom_nr'])
        else:
            return render(request, template)
        
        
class StoreSelection(View):
    def get(self, request):
        return HttpResponseForbidden
    
    def post(self, request):
        uitstroom_nr = request.POST.get('uitstroom_nr')
        test_id = str(uuid.uuid1())
        request.session['test_id'] = test_id
        request.session['uitstroom_nr'] = uitstroom_nr
        resp = {'test_id':request.session['test_id'],'status':'OK', 'uitstroom_nr':request.session['uitstroom_nr']}
        data = json.dumps(resp)
        return HttpResponse(data)
    
class ProcessTest(View):
    def get(self, request):
        return HttpResponseForbidden
    
    def post(self, request):
        testdata = request.POST
        cgi = request.META
        uitstroom_nr = request.session['uitstroom_nr']
        uitstroom = Uitstroom.objects.get(pk=uitstroom_nr)
        test, created = Uitstroom_Ervaringstest.objects.get_or_create(
                                                                      pk=request.session['test_id'], 
                                                                      uitstroom=uitstroom, 
                                                                      session_key=request.session.session_key,
                                                                      remote_ip = cgi.get('REMOTE_ADDR',''),
                                                                      remote_host = cgi.get('REMOTE_HOST',''),
                                                                      referer = cgi.get('HTTP_REFERER',''),
                                                                      user_agent = cgi.get('HTTP_USER_AGENT')
                                                                      )

        test.save()
        
        for k,v in testdata.iteritems():
            testwp, created = Uitstroom_ErvaringstestWerkproces.objects.get_or_create(uitstroom_ervaringstest=test,uitstroom_werkproces= Uitstroom_Werkproces.objects.get(pk=k))
            testwp.score = v
            testwp.save()
            
        resp = {'test_id':request.session['test_id'],'status':'OK', 'uitstroom_nr':request.session['uitstroom_nr'], 'werkprocessen':testdata}
        data = json.dumps(resp)
        return HttpResponse(data)
    
class  ProcessStep3(View):
    def get(self, request):
        return HttpResponseForbidden
        
    def post(self, request):
        data = request.POST
        test = Uitstroom_Ervaringstest.objects.get(pk=request.session['test_id'])
        request.session.get('uitstroom_nr', None)
        test.evp = data.get('evp', test.evp)
        test.evc = data.get('evc', test.evc)
        test.coach = data.get('loopbaancoach', test.coach)
        test.motivatie = data.get('motivatie', test.motivatie)
        test.save()
        return HttpResponse("OK")

    
class SubmitTest(View):
    def get(self, request):
        return HttpResponseForbidden
        
    def post(self, request):
        data = request.POST
        test = Uitstroom_Ervaringstest.objects.get(pk=request.session['test_id'])
        test.first_name = data.get('voornaam', test.first_name)
        test.last_name = data.get('achternaam', test.last_name)
        test.email = data.get('email', test.email)
        test.zipcode = data.get('postcode', test.zipcode)
        test.phone = data.get('telefoon', test.phone)
        test.save()
        textt = get_template('email.txt')
        htmlt= get_template('email.html')
        
        # build list of workprocessen
        uitstroom_nr = request.session['uitstroom_nr']
        uitstroom = Uitstroom.objects.get(pk=uitstroom_nr)            
        ktaken = Uitstroom_Kerntaak.objects.filter(uitstroom=uitstroom_nr)
                
        ktaaklist = []
                
        for kt in ktaken:
            ktaakdict = {}
            ktaakdict['volgnummer'] = kt.volgnummer
            ktaakdict['title'] = kt.title
            werkprocessen = Uitstroom_Werkproces.objects.filter(kerntaak = kt.id)
            wplist = []
            for wp in werkprocessen:
                wpdict = {}
                wpdict['volgnummer'] = wp.volgnummer
                wpdict['title'] = wp.title
                wpdict['id'] = wp.id
                        
                if test:
                    try:
                        testwp = Uitstroom_ErvaringstestWerkproces.objects.get(uitstroom_ervaringstest=test, uitstroom_werkproces= Uitstroom_Werkproces.objects.get(pk=wp.id))
                    except Uitstroom_ErvaringstestWerkproces.DoesNotExist:
                        testwp = None
                            
                    if testwp:
                        wpdict['score'] = testwp.score
                    
                wplist.append(wpdict)
                    
            ktaakdict['werkprocessen'] = wplist 
            ktaaklist.append(ktaakdict)

        c = Context({"title":test.name(), "omschrijving":test.omschrijving(), "kerntaken": ktaaklist, "evp": test.evp, "evc": test.evc, "coach": test.coach, "motivatie": test.motivatie })
        text_body = textt.render(c)
        html_body = htmlt.render(c)
        recipients = [test.email, 'info@rapasso.nl']
        #recipients = ['henk@x2user.com']
        subject = "Jouw ervaring getest voor: " + test.name()
        email = EmailMultiAlternatives(subject, text_body, 'test@testmijnervaring.nl', recipients)
        email.attach_alternative(html_body, "text/html")
        email.send()
        
        return HttpResponse("OK")
        
