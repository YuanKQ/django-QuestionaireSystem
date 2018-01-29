from django.conf.urls import url

from . import views

urlpatterns = [
    # eg. /polls/
    url(r'^$', views.index, name='index'),
    # eg. /polls/1
    url(r'^questionnaire/(?P<page>[0-9]+)/$', views.questionaire, name='questionaire'),
    url(r'^thanks/(?P<page>[0-9]+)/(?P<type>[0-2]+)/$', views.thanks, name='thanks'),
    # url(r'^thanks/#/$', views.thanks, name='thanks'),
    # url(r'^toBeFinish/$', views.toBeFinish, name='toBeFinish'),
    #just try
    # url(r'^tryvote/(?P<question_id>[0-9]+)/$', views.tryvote, name='tryvote')
    # url(r'^(?P<warning>.+)/results/$', views.results, name='results'),
]