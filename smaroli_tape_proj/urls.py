'''
Created on Apr 30, 2018

@author: marol
'''
from django.conf.urls import url
from smaroli_tape_proj import views

urlpatterns = [
    url(r'^$',views.home,name='home'),
    url(r'^final/$',views.final,name='final')
    ]