from django.core.urlresolvers import reverse
from evc.models import Dossier


from djangorestframework.views import View, ListModelView, InstanceModelView
from djangorestframework.mixins import *
from djangorestframework.utils import as_tuple


class ColoView(View):
    def get(self, request):
        return {"resources": 
                [{"kenniscentra":reverse('Kenniscentra') },
                {"competenties":reverse('Competenties') },
                {"componenten":reverse('Componenten') },
                {"dossiers":reverse('Dossiers') },
                {"uitstromen":reverse('Uitstromen') },
                #{"kerntaken":reverse('Kerntaken') },
                ]
                }

class ListView(ListModelView):
    allowed_methods = ('GET',)

    
class DetailView(InstanceModelView):
    allowed_methods = ('GET',)
    
class ListQuickSearchView(ListModelView):
    allowed_methods = ('GET',)
    queryset = None

    def get(self, request, *args, **kwargs):
        model = self.resource.model
        startswith = args[0]
        queryset = self.queryset if self.queryset is not None else model.objects.all()

        if hasattr(self, 'resource'):
            ordering = getattr(self.resource, 'ordering', None)
        else:
            ordering = None

        if ordering:
            args = as_tuple(ordering)
            queryset = queryset.order_by(*args)
        return queryset.filter(title__startswith=startswith)
    
class ListSearchView(ListModelView):
    allowed_methods = ('GET',)
    queryset = None

    def get(self, request, *args, **kwargs):
        model = self.resource.model
        contains = args[0]
        queryset = self.queryset if self.queryset is not None else model.objects.all()

        if hasattr(self, 'resource'):
            ordering = getattr(self.resource, 'ordering', None)
        else:
            ordering = None

        if ordering:
            args = as_tuple(ordering)
            queryset = queryset.order_by(*args)
        return queryset.filter(title__contains=contains)
