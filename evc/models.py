from django.db import models
from django.conf import settings
from django.utils.html import strip_tags

##### specific for Dutch EVC procedures #####

class KBB(models.Model): #kenniscentrum
    nr = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "Kenniscentra"
        ordering = ['name']
        
class KBBContact(models.Model):
    kenniscentrum = models.ForeignKey(KBB)
    tav = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    message = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.attn
    
    class Meta:
        verbose_name_plural = "Kenniscentrum contactpersonen"
        ordering = ['tav']

class Competence(models.Model):
    nr = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    code = models.CharField(default="",blank=True, null=True, max_length=30)
    
    def __unicode__(self):
        #return self.name.decode('utf8')
        return str(self.nr) + ": " + self.name

    class Meta:
        verbose_name_plural = "Competenties"
        
        
class Component(models.Model):
    nr = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    competence = models.ForeignKey(Competence, blank=True, null=True, related_name='components')
    
    def __unicode__(self):
        return self.name

                
class Dossier(models.Model):
    nr = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    #do we need this?
    status = models.CharField(max_length=30, null=True, blank=True)
    vastgesteld_OCW_LNV = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=60, null=True, blank=True)
    cohort = models.CharField(max_length=30, null=True, blank=True)
    wettelijkeberoepsvereisten = models.CharField(max_length=30, null=True, blank=True)
    wettelijkebranchevereisten = models.CharField(max_length=30, null=True, blank=True)
    positief_advies_coordinatiepunt = models.CharField(max_length=30, null=True, blank=True)
    codecoordinatiepunt = models.CharField(max_length=30, null=True, blank=True)
    sector = models.TextField(null=True, blank=True)
    branche = models.TextField(null=True, blank=True)
    inleiding = models.TextField(null=True, blank=True)
    kenniscentra = models.ManyToManyField(KBB)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return str(self.nr) + ": " + self.title


class DeelA(models.Model):
    dossier = models.OneToOneField(Dossier, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, default="Deel A: Beeld van de beroepengroep")
    omschrijving = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.title


class DeelB(models.Model):
    dossier = models.OneToOneField(Dossier, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, default="Deel B: De kwalificaties")
    inleiding = models.TextField(null=True, blank=True)
    loopbaanperspectief = models.TextField(null=True, blank=True)
    beschrijvinguitstromen = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return  str(self.dossier.nr) + ": " + self.dossier.title + ">" + self.title

        
class Uitstroom(models.Model):
    nr = models.IntegerField(primary_key=True)
    deelb = models.ForeignKey(DeelB, null=True, blank=True )
    title = models.CharField(max_length=255)
    niveau = models.IntegerField(default=2)
    contextvandeuitstroom = models.TextField(null=True, blank=True)
    typerendeberoepshouding = models.TextField(null=True, blank=True)
    rolenverantwoordelijkheden = models.TextField(null=True, blank=True)
    complexiteit = models.TextField(null=True, blank=True)
    wettelijkeberoepsvereisten = models.CharField(max_length=8, null=True, blank=True)
    toelichtingwettelijkeberoepsvereisten = models.TextField(null=True, blank=True)
    branchevereisten = models.CharField(max_length=8, null=True, blank=True)
    toelichtingbranchevereisten = models.TextField(null=True, blank=True)
    crebo = models.CharField(max_length=32)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    
    def __unicode__(self):
        return str(self.deelb.dossier.nr) + ": " + self.deelb.dossier.title + "> " + self.title + " (crebo: " + self.crebo + ")"

    class Meta:
        verbose_name_plural = "Uitstromen"
        ordering = ['crebo']
        
class Kerntaak(models.Model):
    nr = models.IntegerField(primary_key=True)
    dossier = models.ForeignKey(Dossier)
    volgnummer = models.IntegerField(default=0)
    title = models.CharField(max_length=255)
    omschrijving = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return str(self.dossier.nr) +": " + self.dossier.title + ">" + self.title

        
    class Meta:
        verbose_name_plural = "Kerntaken"
        
class Werkproces(models.Model):
    nr = models.IntegerField(primary_key=True)
    kerntaak = models.ForeignKey(Kerntaak)
    volgnummer = models.IntegerField(default=0)
    title = models.TextField()
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return str(self.kerntaak.dossier.nr) + ": " + self.kerntaak.dossier.title + ">" + self.kerntaak.title + ">" + self.title

    class Meta:
        verbose_name_plural = "Werkprocessen"
        
class Vaardigheid(models.Model):
    nr = models.IntegerField(primary_key=True)
    title = models.TextField()
    dossier = models.ForeignKey(Dossier)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.title


class Diploma(models.Model):
    title = models.CharField(max_length=255)
    dossier = models.ForeignKey(Dossier)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return self.title

        
class Uitstroom_Kerntaak(models.Model):
    volgnummer = models.IntegerField(default=0)
    uitstroom = models.ForeignKey(Uitstroom, related_name='kerntaken')
    title = models.CharField(max_length=255)
    referentie = models.ForeignKey(Kerntaak)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return str(self.uitstroom.nr) + ": " + self.uitstroom.title + ">" + self.title
        

class Uitstroom_Werkproces(models.Model):
    volgnummer = models.IntegerField(default=0)
    kerntaak = models.ForeignKey(Uitstroom_Kerntaak, related_name='werkprocessen')
    title = models.TextField()
    referentie = models.ForeignKey(Werkproces)
    beschrijving = models.TextField(null=True, blank=True)
    resultaat = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    
    def __unicode__(self):
        return str(self.kerntaak.uitstroom.nr) + ": " + self.kerntaak.uitstroom.title + ">" + self.kerntaak.title + ">" + self.title

    
class Uitstroom_Competentie(models.Model):
    title = models.CharField(max_length=255)
    werkproces = models.ForeignKey(Uitstroom_Werkproces)
    code = models.CharField(default="",blank=True, null=True, max_length=30)
    referentie = models.ForeignKey(Competence)
    indicator = models.TextField(null=True, blank=True)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    def __unicode__(self):
        return  self.werkproces.kerntaak.title + ">" + self.werkproces.title + ">" + self.title


class Uitstroom_Component(models.Model):
    title = models.CharField(max_length=255)
    referentie = models.ForeignKey(Component)
    competentie = models.ForeignKey(Uitstroom_Competentie)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    def __unicode__(self):
        return  self.competentie.title + ">" + self.title

        
class Uitstroom_Vaardigheid(models.Model):
    title = models.TextField()
    referentie = models.ForeignKey(Vaardigheid)
    competentie = models.ForeignKey(Uitstroom_Competentie)
    tenant = models.IntegerField(default=0,blank=True, null=True)
    def __unicode__(self):
        return  self.competentie.title + ">" + self.title
    
class Uitstroom_Ervaringstest(models.Model):
    choices = (
               ('0','Nee'),
               ('1','Ja'),
               )
    uuid = models.CharField(primary_key=True, max_length=36)
    session_key = models.CharField(max_length=32)
    uitstroom = models.ForeignKey(Uitstroom, related_name='ervaringstesten')
    remote_ip = models.IPAddressField(blank=True, null=True)
    remote_host = models.CharField(max_length=255, null=True, blank=True)
    referer = models.URLField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=120, null=True, blank=True)
    zipcode = models.CharField(max_length=16, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    evp = models.CharField(max_length=2, choices=choices, blank=True, null=True)
    evc = models.CharField(max_length=2, choices=choices, blank=True, null=True)
    coach = models.CharField(max_length=2, choices=choices, blank=True, null=True)
    motivatie = models.TextField(null=True, blank=True)
    
    
    def __unicode__(self):
        return  self.uuid +": " + self.uitstroom.title
    
    def name(self):
        return  str(self.uitstroom.title)
    
    def omschrijving(self):
        return strip_tags(self.uitstroom.contextvandeuitstroom)
    

class Uitstroom_ErvaringstestWerkproces(models.Model):
    scores = (
             ('1','Geen'),
             ('2','Weinig'),
             ('3','Gemiddeld'),
             ('4','Meer dan gemiddeld'),
             ('5','Veel'),
             )
    uitstroom_ervaringstest = models.ForeignKey(Uitstroom_Ervaringstest)
    uitstroom_werkproces = models.ForeignKey(Uitstroom_Werkproces)
    score = models.CharField(max_length=2, choices=scores, blank=True, null=True)

    

    
    
    
