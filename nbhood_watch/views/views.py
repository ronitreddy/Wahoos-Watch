from django.shortcuts import render
from django.views import generic
from nbhood_watch.models import *

# Maybe use this as a "central controller" somehow? Seems a little obsolete rn

class IndexView(generic.View):
    model = Submission
    template_name = 'nbhood_watch/index.html'

    def get(self, request, *args, **kwargs):
        context = {'message': 'Hello from MyView!'}
        return render(request, 'nbhood_watch/index.html', context)

