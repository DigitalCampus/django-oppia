# oppia/media/views.py
import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render,render_to_response, get_object_or_404
from django.template import RequestContext


    
    
    