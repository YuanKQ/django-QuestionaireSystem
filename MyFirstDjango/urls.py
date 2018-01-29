"""MyFirstDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import survey1

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^polls/', include('survey1.urls', namespace="survey1")),
    url(r'^accounts/login/$', survey1.views.myLogin),
    # #url(r'^questions/$', survey_views_1.questionInfo),
    # url(r'^polls/(?P<question_page>[0-9]+)/$', survey_views_1.questionaire, name='questionaire'),
]
