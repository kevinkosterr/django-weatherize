from django.shortcuts import render, redirect
from django.contrib.gis.geoip2 import GeoIP2

from geoip2.errors import AddressNotFoundError

from .forms import SearchForm

import requests

from .settings import (
    GEOIP_PATH,
    ACCUWEATHER_URL,
    FALLBACK_IP
)


def index(request, *args, **kwargs):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # replacing all of the spaces with '+' because the query string in URLS doesn't support spaces.
            city = form.cleaned_data["city"].replace(" ", "+")
            url = ACCUWEATHER_URL + f"&q={city}"
            response = requests.post(url=url)
            current_weather = response.json()

    else:
        form = SearchForm()
        # get the IPv4 address where the request is coming from.
        # we will use geoip2 to find out where in the world the request is coming from.
        request_ip = request.META.get("REMOTE_ADDR", None)
        if request_ip:
            # GEOIP_PATH is defined in settings, this is /geoip from the root directory by default.
            g = GeoIP2(path=GEOIP_PATH)
            try:
                city = g.city(request_ip)["city"]
            except AddressNotFoundError:
                # this usually happens when you're running the application on localhost, thus when developing.
                # FALLBACK_IP will be google.com by default.
                city = g.city(FALLBACK_IP)["city"]
            current_weather = requests.post(url=ACCUWEATHER_URL + f"&q={city}").json()

    context = dict(current_weather=current_weather, form=form)

    return render(request, "index.html", context=context)
