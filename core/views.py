# Create your views here.
from django.shortcuts import render_to_response

def base(request, template="core/base.html"):
    return render_to_response(template)
