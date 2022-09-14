import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfilForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Agent
from gestionnaire.models import Archive


class Checkprofile(LoginRequiredMixin, DetailView):
    model = Agent
    template_name = 'utilisateurs/checkprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = Agent.objects.get(user=self.request.user)
        return context




@login_required
def dashboard(request):
    """ vue pour la page d'accueil, le tableau de bord """

    try:
        user = Agent.objects.get(user=request.user)
        archives = user.archive_set.all()
    except:
       agent = Agent()
       agent.departement = 'direction'
       agent.user = request.user
       agent.save()

    user = Agent.objects.get(user=request.user)
    archives = user.archive_set.all()
    archives_ = []
    for i in Archive.objects.filter(confidence__exact="t"):
        archives_.append(i)
    for ii in Archive.objects.filter(confidence__exact='d'):
        if user.departement == ii.auteur.departement:
            archives_.append(ii)


    context = {
        'user': user,
        'archives': archives,
        'archives_': archives_
    }
    return render(request, 'utilisateurs/dashboard.html', context)


@login_required
def profile(request):
    """ affichage du profile et modification """
    user = request.user
    agent = Agent.objects.get(user=user)
    archives = list(agent.archive_set.all())

    nbr = len(archives)
    context = {
       'user': Agent.objects.get(user=user),
        'nbr': nbr,
    }

    if request.method == "POST":
        form = EditProfilForm(request.POST, request.FILES)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            prenom = form.cleaned_data.get('prenom')
            email = form.cleaned_data.get('email')
            image = form.cleaned_data.get('image')
            user.first_name = nom
            user.last_name = prenom
            user.email = email
            user.save()

            if agent.photo:
                file_url = agent.photo.url
                os.remove(os.path.join(settings.BASE_DIR, file_url[1:]))

            agent.photo = image
            agent.save()
            return redirect('utilisateurs:dashboard')

        else:
            context['form'] = EditProfilForm()
            context["error"] = "une erreur s'est produit"
            return render(request, 'utilisateurs/profile.html', context)

    else:
        context['form'] = EditProfilForm()
        return render(request, 'utilisateurs/profile.html', context)
