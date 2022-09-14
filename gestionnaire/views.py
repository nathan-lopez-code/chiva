import os
from aiohttp.web_fileresponse import FileResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Archive
from utilisateurs.models import Agent
from .forms import FormArchive
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


@login_required
def affichageArchive(request):
    agent = Agent.objects.get(user=request.user)
    archives = agent.archive_set.all()
    context = {
        'user': agent,
        'archives': archives
    }
    return render(request, 'gestionnaire/affichageArhcive.html', context)


def deleteArchive(request, pk):
    user = Agent.objects.get(user=request.user)
    object = None
    try:
        object = Archive.objects.get(pk=pk)
    except:
        return render(request, 'gestionnaire/affichageArhcive.html',
                      {'user': user, 'archives': user.archive_set.all(), 'error': True})
    try:
        fichier_url = object.fichier.url[1:]
        os.remove(os.path.join(settings.BASE_DIR, fichier_url))
    except:
        pass
    c = object.delete()
    return render(request, 'gestionnaire/affichageArhcive.html',
                  {'user': user, 'archives': user.archive_set.all(), 'succes': True})


class DetailArchive(LoginRequiredMixin, DetailView):
    model = Archive
    template_name = "gestionnaire/detailArchive.html"
    context_object_name = 'archive'

    def get_context_data(self, **kwargs):
        user = Agent.objects.get(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['archives'] = user.archive_set.all()
        return context


class ModificationArchive(LoginRequiredMixin, UpdateView):
    model = Archive
    template_name = "gestionnaire/modificationArchive.html"
    template_name_suffix = 'form'
    success_url = reverse_lazy('archive:affichage')
    form_class = FormArchive

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Agent.objects.get(user=self.request.user)
        return context


class CreateArchive(LoginRequiredMixin, CreateView):
    """ creation d'une archive """
    model = Archive
    template_name = "gestionnaire/creationArchive.html"
    success_url = reverse_lazy('archive:affichage')
    form_class = FormArchive

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form,
                       'user': Agent.objects.get(user=self.request.user)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        error = form.errors
        if form.is_valid():
            user = self.request.user
            agent = Agent.objects.get(user=user)
            form.instance.auteur = agent
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name,
                          {'form': form, 'user': Agent.objects.get(user=self.request.user),
                           'form_error': error})


def file_response(request, pk):
    try:
        archive = Archive.objects.get(pk=pk)
        file_url = archive.fichier.url[1:]
        file = open(os.path.join(settings.BASE_DIR, file_url), )
        return FileResponse(archive.fichier.open())
    except:
        pass

