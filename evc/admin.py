from django.contrib import admin
from evc.models import *
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    
class KBBContactInline(admin.TabularInline):
    model = KBBContact
    extra = 1

class KBBAdmin(admin.ModelAdmin):
    model = KBB
    inlines = [
        KBBContactInline,
    ]

class ComponentInline(admin.TabularInline):
    model = Component
    extra = 0
    
class CompetenceAdmin(admin.ModelAdmin):
    model = Competence
    inlines = [
        ComponentInline,
    ]
    
class VaardigheidInline(admin.TabularInline):
    model = Vaardigheid
    extra = 0
    
class DeelaInline(admin.StackedInline):
    model = DeelA
    extra = 0
    
class DeelbInline(admin.StackedInline):
    model = DeelB
    extra = 0
    
class Uitstroom_KerntaakInline(admin.TabularInline):
    model = Uitstroom_Kerntaak
    extra = 0
    
class UitstroomAdmin(admin.ModelAdmin):
    model = Uitstroom
    inlines = [
        Uitstroom_KerntaakInline,
    ]
    
class Uitstroom_CompetentieInline(admin.StackedInline):
    model = Uitstroom_Competentie
    extra = 0
    
class Uitstroom_VaardigheidInline(admin.TabularInline):
    model = Uitstroom_Vaardigheid
    extra = 0
    
class Uitstroom_ComponentInline(admin.TabularInline):
    model = Uitstroom_Component
    extra = 0
    
    
class Uitstroom_WerkprocesAdmin(admin.ModelAdmin):
    model = Uitstroom_Werkproces
    inlines = [
        Uitstroom_CompetentieInline,
    ]
    
class Uitstroom_CompetentieAdmin(admin.ModelAdmin):
    model = Uitstroom_Competentie
    inlines = [
        Uitstroom_VaardigheidInline,
        Uitstroom_ComponentInline
    ]

    
class KerntaakInline(admin.StackedInline):
    model = Kerntaak
    extra = 0
    
class DossierAdmin(admin.ModelAdmin):
    model = Dossier
    inlines = [
        DeelaInline,
        DeelbInline,
        KerntaakInline,
        VaardigheidInline,
        
    ]
    
class WerkprocesInline(admin.TabularInline):
    model = Werkproces
    extra = 0

class KerntaakAdmin(admin.ModelAdmin):
    model = Kerntaak
    inlines = [
        WerkprocesInline,
    ]
    

admin.site.register(Session, SessionAdmin)
admin.site.register(KBB, KBBAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Uitstroom, UitstroomAdmin)
admin.site.register(Kerntaak, KerntaakAdmin)
admin.site.register(Uitstroom_Werkproces, Uitstroom_WerkprocesAdmin)
