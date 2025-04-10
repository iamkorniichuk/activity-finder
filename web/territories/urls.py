from django.urls import path

from .views import TerritoryAutocompleteView


app_name = "territories"

urlpatterns = [
    path("autocomplete/", TerritoryAutocompleteView.as_view(), name="autocomplete"),
]
