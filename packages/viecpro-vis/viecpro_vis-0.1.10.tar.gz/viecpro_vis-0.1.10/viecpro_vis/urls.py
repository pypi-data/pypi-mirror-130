from viecpro_vis.views import StartView, autocomplete_view
from viecpro_vis.api_views import method_dispatcher

from django.conf.urls import url
from django.urls import path

app_name = "viecpro_vis"

urlpatterns = [
    url(r"^start/$", StartView.as_view(), name="start_view"),
    url(r"^entityautocomplete/$", autocomplete_view, name="entity_autocomplete"),
    path(r"api/<entity_type>/<pk>/<graph_option>/<direction>", method_dispatcher, name="method_dispatcher"),]


