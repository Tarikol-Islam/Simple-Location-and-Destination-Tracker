from django import forms
from Measurement.models import Measurement
from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo , get_center_coordinates, get_zoom
import folium
# Create your views here.
def calculate_distance_view(request):
    obj = get_object_or_404(Measurement, id = 1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='Measurement')
    ip = '103.230.106.50'
    S_country , S_city, S_lat ,S_lon = get_geo(ip)
    StartingPoint = (S_lat, S_lon)

    #Folium map part
    M = folium.Map(width=700,height=500, location = get_center_coordinates(S_lat,S_lon), zoom_start = 8)
    #Location marker
    folium.Marker([S_lat,S_lon], tooltip = "Click Here for more",popup=S_city['city'], icon= folium.Icon(color = "purple")).add_to(M)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_= form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        EndingPoint = (destination.latitude, destination.longitude)
        Distance = round(geodesic(StartingPoint,EndingPoint).km,2)
        #Folium map part
        M = folium.Map(width=700,height=500,location = get_center_coordinates(*(StartingPoint+EndingPoint)), zoom_start =get_zoom(Distance))
        #Location marker
        folium.Marker([S_lat,S_lon], tooltip = "Click Here for more",popup=S_city['city'], icon= folium.Icon(color = "purple")).add_to(M)
        #Destination Marker
        folium.Marker(EndingPoint, tooltip = "Click Here for more",popup=destination, icon= folium.Icon(color = "purple")).add_to(M)
        
        instance.location = geolocator.geocode(S_city)
        instance.distance = Distance
        instance.save()
    M = M._repr_html_()
    context= {
        'distance': obj,
        'form' : form,
        'map' : M,
    }

    return render(request, 'Measurement/main.html', context)