from django.core.urlresolvers import reverse
from djangorestframework.resources import ModelResource, Resource
from evc.models import KBB, Competence, Component, Vaardigheid, Dossier, Kerntaak, Werkproces, Uitstroom, Uitstroom_Kerntaak, Uitstroom_Werkproces, Uitstroom_Competentie, Uitstroom_Component, Uitstroom_Vaardigheid
from colo.views import ListView, DetailView, ListSearchView, ListQuickSearchView

class ListDetailsResource(ModelResource):
    def __init__(self, view):

        super(ModelResource, self).__init__(view)

        self.model = getattr(view, 'model', None) or self.model
        
        if self.view.__class__ == ListView:
            self.fields = getattr(self, 'list_fields', None) or self.fields
        elif self.view.__class__ == ListSearchView:
            self.fields = getattr(self, 'search_fields', None) or self.fields
        elif self.view.__class__ == ListQuickSearchView:
            self.fields = getattr(self, 'search_fields', None) or self.fields
        elif self.view.__class__ == DetailView:
            self.fields = getattr(self, 'detail_fields', None) or self.fields
        else:
            self.fields = self.fields


class KenniscentrumResource(ListDetailsResource):
    model = KBB
    list_fields = ('name', 'nr', 'url')
    detail_fields = ('name', 'nr', 'description','dossiers')
    def dossiers(self, instance):
        doss = Dossier.objects.filter(kenniscentra=instance.nr)
        dosslist = []
        for dos in doss:
            dosdict = {}
            dosdict['title'] = dos.title
            dosdict['nr'] = dos.nr
            dosdict['url'] = reverse('Dossier', kwargs={'pk':dos.nr})
            dosslist.append(dosdict)
        return dosslist
    
    
class CompetentieResource(ListDetailsResource):
    model = Competence
    list_fields = ('name', 'nr', 'code', 'url')
    detail_fields = ('name', 'nr', 'code', 'components')
    def components(self, instance):
        comps = Component.objects.filter(competence=instance.nr)
        complist = []
        for comp in comps:
            compdict = {}
            compdict['nr'] = comp.nr
            compdict['title'] = comp.name
            compdict['url'] = reverse('Component', kwargs={'pk':comp.nr})
            complist.append(compdict)
        return complist

    
class ComponentResource(ListDetailsResource):
    model = Component
    list_fields = ('name', 'nr', 'url')
    detail_fields = ('name', 'nr', 'competence')
    def competence(self, instance):
        return reverse('Competentie', kwargs={'pk':instance.competence.nr})

   
class DossierResource(ListDetailsResource):
    model = Dossier
    list_fields = ('nr','title','url')
    search_fields = ('nr', 'title','url')
    exclude = ('tenant',)
    detail_fields = ('nr', 'title', 'contact', 'kenniscentra', 'inleiding','branche', 'cohort', 'sector', 'uitstromen')
    def uitstromen(self, instance):
        uitstr = Uitstroom.objects.filter(deelb=instance.deelb)
        uitstrlist = []
        for uit in uitstr:
            uitdict = {}
            uitdict['nr'] = uit.nr
            uitdict['title'] = uit.title
            uitdict['niveau'] = uit.niveau
            uitdict['url'] = reverse('Uitstroom', kwargs={'pk':uit.nr})
            uitstrlist.append(uitdict)
        return uitstrlist
    
class KerntaakResource(ListDetailsResource):
    model = Kerntaak
    list_fields = ('nr', 'title', 'url')
    detail_fields = ('nr', 'title', 'omschrijving', 'volgnummer', 'dossier', '__unicode__')
    def dossier(self, instance):
        return reverse('Dossier', kwargs={'pk':instance.dossier.nr})
    
class WerkprocesResource(ListDetailsResource):
    model = Werkproces
    list_fields = ('nr', 'title', 'url')
    detail_fields = ('nr', 'title', 'volgnummer', 'kerntaak', '__unicode__')
    def kerntaak(self, instance):
        #return reverse('kerntaak', kwargs={'pk':instance.kerntaak.nr})
        return {}
    
class VaardigheidResource(ListDetailsResource):
    model = Vaardigheid
    list_fields = ('nr', 'title', 'url')
    detail_fields = ('nr', 'title', 'dossier', '__unicode__')
    def dossier(self, instance):
        return reverse('Dossier', kwargs={'pk':instance.dossier.nr})
    
class Uitstroom_KerntaakResource(ListDetailsResource):
    model = Uitstroom_Kerntaak
    list_fields = ('id', 'title','volgnummer', 'url')
    detail_fields = ('id', 'title','volgnummer', 'referentie', '__unicode__')
    def referentie(self, instance):
        url = reverse('Kerntaak', kwargs={'pk':instance.referentie.nr})
        return {'nr':instance.referentie.nr, 'url':url}
    
class Uitstroom_WerkprocesResource(ListDetailsResource):
    model = Uitstroom_Werkproces
    list_fields = ('id', 'title','volgnummer', 'url')
    detail_fields = ('id', 'title','volgnummer', 'referentie', '__unicode__', 'beschrijving', 'resultaat', 'competenties')
    def referentie(self, instance):
        url = reverse('Werkproces', kwargs={'pk':instance.referentie.nr})
        return {'nr':instance.referentie.nr, 'url':url}
    def competenties(self, instance):
        comps = Uitstroom_Competentie.objects.filter(werkproces=instance.id)
        complist = []
        for comp in comps:
            compdict = {}
            compdict['title'] = comp.title
            compdict['code'] = comp.code
            compdict['url'] = reverse('Uitstroom-Competentie', kwargs={'pk':comp.id})
            complist.append(compdict)
        return complist

    
class Uitstroom_CompetentieResource(ListDetailsResource):
    model = Uitstroom_Competentie
    list_fields = ('id','title', 'code', 'url')
    detail_fields = ('id','title', 'code', 'indicator', 'referentie', 'vaardigheden', 'componenten')
    def referentie(self, instance):
        url = reverse('Competentie', kwargs={'pk':instance.referentie.nr})
        return {'nr':instance.referentie.nr, 'url':url}
    def vaardigheden(self, instance):
        vaarn = Uitstroom_Vaardigheid.objects.filter(competentie=instance.id)
        vaarlist = []
        for vaar in vaarn:
            vaardict = {}
            vaardict['title'] = vaar.title
            vaardict['url'] = reverse('Uitstroom-Vaardigheid', kwargs={'pk':vaar.id})
            vaarlist.append(vaardict)
        return vaarlist
    def componenten(self, instance):
        comps = Uitstroom_Component.objects.filter(competentie=instance.id)
        complist = []
        for comp in comps:
            compdict ={}
            compdict['title'] = comp.title
            compdict['url'] = reverse('Uitstroom-Component', kwargs={'pk':comp.id})
            complist.append(compdict)
        return complist

class Uitstroom_VaardigheidResource(ListDetailsResource):
    model = Uitstroom_Vaardigheid
    list_fields = ('id','title', 'url')
    detail_fields = ('id','title','referentie')
    def referentie(self, instance):
        url = reverse('Vaardigheid', kwargs={'pk':instance.referentie.nr})
        return {'nr':instance.referentie.nr, 'url':url}

class Uitstroom_ComponentResource(ListDetailsResource):
    model = Uitstroom_Component
    list_fields = ('id','title', 'url')
    detail_fields = ('id','title','referentie')
    def referentie(self, instance):
        url = reverse('Component', kwargs={'pk':instance.referentie.nr})
        return {'nr':instance.referentie.nr, 'url':url}

class UitstroomResource(ListDetailsResource):
    model = Uitstroom
    list_fields = ('nr', 'title', 'crebo','url')
    search_fields = ('nr', 'title','url')
    detail_fields = ('nr', 'title','niveau', 'crebo', 'contextvandeuitstroom', 'rolenverantwoordelijkheden', 'typerendeberoepshouding', 'complexiteit', 'kerntaken' )
    exclude = ('tenant',)
    ordering = ('title',)
    
    def kerntaken(self, instance):
        ktaken = Uitstroom_Kerntaak.objects.filter(uitstroom=instance.nr)
        ktaaklist = []

        for kt in ktaken:
            ktaakdict = {}
            ktaakdict['volgnummer'] = kt.volgnummer
            ktaakdict['title'] = kt.title
            ktaakdict['url'] = reverse('Kerntaak', kwargs={'pk':kt.referentie.nr})
            werkprocessen = Uitstroom_Werkproces.objects.filter(kerntaak = kt.id)
            wplist = []
            for wp in werkprocessen:
                wpdict = {}
                wpdict['volgnummer'] = wp.volgnummer
                wpdict['title'] = wp.title
                wpdict['referentie'] = reverse('Werkproces', kwargs={'pk':wp.referentie.nr})
                wpdict['url'] = reverse('Uitstroom-Werkproces', kwargs={'pk':wp.id})
                wplist.append(wpdict)
                
                
            ktaakdict['werkprocessen'] = wplist   
            ktaaklist.append(ktaakdict)

            
        return ktaaklist
