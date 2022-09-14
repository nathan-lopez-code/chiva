from django.urls import path
from .views import CreateArchive, DetailArchive, ModificationArchive, affichageArchive, deleteArchive, file_response

app_name = "archive"

urlpatterns = [
    path("creation/", CreateArchive.as_view(), name="creation"),
    path("consultation/<int:pk>", DetailArchive.as_view(), name="consultation"),
    path("modification/<int:pk>", ModificationArchive.as_view(), name="modification"),
    path("affichage/", affichageArchive, name="affichage"),
    path("supprimer/<int:pk>", deleteArchive, name="suppression"),
    path("fihcier/<int:pk>", file_response, name="download")
]
