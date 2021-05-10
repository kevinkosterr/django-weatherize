from django.forms import CharField
from django import forms


class SearchForm(forms.Form):
    city = CharField(
        widget=forms.TextInput(
            attrs={
                "class": "search-input",
                "placeholder": "What's the weather like in...?",
                "id": "search-input",
            }
        )
    )
