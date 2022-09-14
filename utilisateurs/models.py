from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Agent(models.Model):
    """ Extension du model utilisateur de django """

    DEPARTEMENT = (
        ("direction", "direction"),
        ("secretariat", "secretariat"),
        ("marketing", "marketing"),
        ("gestion comptable", "gestion comptable"),
        ("vendeur", "vendeur")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100, choices=DEPARTEMENT)
    poste = models.CharField(verbose_name="poste occupé", max_length=100, default="aucun")
    photo = models.ImageField(verbose_name="photo de profile", upload_to="utilisateur/profile/", null=True, blank=True)

    def __str__(self):
        return "{} \ndépartement : {}\nposte".format(self.user.username, self.departement, self.poste)

    def get_absolute_url(self):
        return reverse('utilisateurs:checkprofile', kwargs={'id': str(self.id)})
