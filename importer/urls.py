from django.conf.urls import url
from . import views

app_name = 'importer'

urlpatterns = [

    # /importer/
    url(r'^$', views.index, name='index'),

    # /importer/person/
    url(r'^sources/persons', views.PersonList.as_view(), name='persons'),

]

#
# # /cda/sources/persons/#
# url(r'^sources/persons/(?P<pk>[0-9]+)/$', views.PersonProfile.as_view(), name='persons_profile'),
#
# # /cda/sources/persons/add/
# url(r'^sources/persons/add/$', views.PersonCreate.as_view(), name='person-add'),
#
# # /cda/sources/persons/update/#
# url(r'^sources/persons/update/(?P<pk>[0-9]+)/$', views.PersonUpdate.as_view(), name='person-update'),
#
# # /cda/sources/persons/#/delete/
# url(r'^sources/persons/(?P<pk>[0-9]+)/delete/$', views.PersonDelete.as_view(), name='person-delete'),
#
# # /cda/map/
# url(r'^map/$', views.MapView.as_view(), name='map_view'),