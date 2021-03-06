"""bitcoin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from demo import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^initnet$', views.initnet, name='initnet'),
    url(r'^initcircle$', views.initcircle, name='initcircle'),
    url(r'^inittree$', views.inittree, name='inittree'),
    url(r'^initpow$', views.initpow, name='initpow'),
    url(r'^initBGP$', views.initBGP, name='initBGP'),
    url(r'^initdouble$', views.initdouble, name='initdouble'),
    url(r'^BGPattack$', views.BGPattack, name='BGPattack'),
    url(r'^PBFT$', views.PBFT, name='PBFT'),
    url(r'^initpos$', views.initpos, name='initpos'),
    url(r'^initPBFT$', views.initPBFT, name='initPBFT'),
    url(r'^close$', views.close, name='close'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^index$', views.index, name='index'),
    url(r'^get_node_info$', views.get_node_info, name='get_node_info'),
    url(r'^mine$', views.mine, name='mine'),
    url(r'^send_tx$', views.send_tx, name='send_tx'),
]
