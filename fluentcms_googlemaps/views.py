import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.views.generic.detail import BaseDetailView
from .models import Marker


class MarkerDetailView(BaseDetailView):
    """
    Simple view for fetching marker details.
    """
    # TODO: support different object types. Perhaps through django-polymorphic?
    model = Marker
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.
        """
        if queryset is None:
            queryset = self.get_queryset()

        # Take a GET parameter instead of URLConf variable.
        try:
            pk = long(self.request.GET[self.pk_url_kwarg])
        except (KeyError, ValueError):
            raise Http404("Invalid Parameters")
        queryset = queryset.filter(pk=pk)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist as e:
            raise Http404(e)
        return obj

    def render_to_response(self, context):
        return HttpResponse(json.dumps(self.get_json_data(context)), content_type='application/json; charset=utf-8')

    def get_json_data(self, context):
        """
        Generate the JSON data to send back to the client.
        :rtype: dict
        """
        return self.object.to_dict(detailed=True)
