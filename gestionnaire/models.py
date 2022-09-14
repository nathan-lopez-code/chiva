from django.db import models
from utilisateurs.models import Agent
from django.shortcuts import reverse
from datetime import date


def today():
    return str(date.today())


class Archive(models.Model):
    """ table archive """
    CONFIDENCE = (
        ('p', 'moi uniquement'),
        ('d', 'les membres du department'),
        ('t', 'tout le système'),
    )

    TYPE_FICHIER = (
        ('pdf', 'fichier pdf'),
        ('word', 'fichier word'),
        ('excel', 'fichier excel'),
        ('video', 'fichier video'),
        ('image', 'fichier image'),
        ('texte', 'fichier texte'),
    )

    titre = models.CharField(max_length=100, verbose_name="titre de l'archive")
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name='description')
    confidence = models.CharField(verbose_name="Qui peut voir cet archive", max_length=2, choices=CONFIDENCE, default="p")

    Date_creation = models.DateField(auto_now=True, verbose_name="date de création")
    Date_peremtion = models.DateField(null=True, blank=True, verbose_name="date de péremption")
    Date_modification = models.DateField(null=True, blank=True, verbose_name="date de la dernière modification"
                                         , default=today())

    nom = models.CharField(verbose_name="nom du fichier", max_length=100, null=True, blank=True)
    type = models.CharField(verbose_name='type du fichier', choices=TYPE_FICHIER, max_length=50,
                            null=True, blank=True, default="pdf")
    fichier = models.FileField(upload_to="archive/fichiers/", verbose_name="fichier annexe", blank=True, null=True)

    auteur = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return "{}\nauteur : {}".format(self.titre, self.auteur)

    def get_absolute_url(self):
        return reverse('archive:consultation', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['Date_creation', 'Date_modification']
