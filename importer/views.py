from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Evidence, Person


class EvidenceList(ListView):
    template_name = 'evidences.html'
    context_object_name = 'all_evidences'

    def get_queryset(self):
        return Evidence.objects.all()


class PersonList(ListView):
    template_name = 'persons.html'
    context_object_name = 'all_persons'

    def get_queryset(self):
        return Person.objects.all()

def index(request):
    return render(request, 'index.html')
