from django.forms import ModelForm
from gestionnaire.models import Archive


class FormArchive(ModelForm):



    class Meta:
        model = Archive
        fields = [
            'titre', 'description', 'confidence',
            'Date_peremtion', 'Date_modification',
            'nom', 'type', 'fichier'
        ]
