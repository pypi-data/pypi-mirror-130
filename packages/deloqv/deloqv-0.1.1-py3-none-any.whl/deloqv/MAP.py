#%%
import pandas as pd
import folium
import osmnx as ox
from openrouteservice import convert
import openrouteservice
import json
from ipywidgets import interact
import os
from download import download

from pandas.core.indexes.base import Index

#%% Dataframe of the prices and the GPS coordinates of th cities
ur1 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/coordonnees_clean.csv'
path = os.path.join(os.getcwd(),'coordonnees_clean.csv')
download(ur1, path, replace=True)
Coordinate = pd.read_csv('./coordonnees_clean.csv')

ur2 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/prices_clean.csv'
path = os.path.join(os.getcwd(),'prices_clean.csv')
download(ur2, path, replace=True)
price = pd.read_csv('./prices_clean.csv')

#%% Creating a list contains the name of each city in the database
Cities = Coordinate.NOMGARE.unique()

#%%
class map:
    def __init__(self) -> None:
        pass

    def index(Nom):
     for k in range (36):
        if Cities[k] == Nom:
            return k

    def road(DEPART, ARRIVEE):
        i = Coordinate[Coordinate['NOMGARE'] == DEPART].index[0]
        j = Coordinate[Coordinate['NOMGARE'] == ARRIVEE].index[0]

        x = [Coordinate['X'][i],
            Coordinate['Y'][i]]
        y = [Coordinate['X'][j],
            Coordinate['Y'][j]]
        m = folium.Map(
                            location=[43.1837661, 3.0042121],
                            zoom_start=10,
                            control_scale=True)
        client = openrouteservice.Client(key='5b3ce3597851110001cf62486f5564a064e34f3895221e5a0d9a2405')


        #problem solving of different outward and return distances
        
        if i < j:

            cor = [x, y]
            

            for i in range(0, len(cor)-1):
                crd = cor[i], cor[i+1]
                crr = client.directions(crd)

                with(open('test.json', '+w')) as f:
                    f.write(json.dumps(crr, indent=4, sort_keys=True))

                    geometry = client.directions(crd)['routes'][0]['geometry']
                    decoded = convert.decode_polyline(geometry)

                    Dis_tx = "<h4> Distance :&nbsp" + "<strong>"+str(round(crr['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
                    Pr_tx = "<h4> Prix :&nbsp" + "<strong>" + str(price[DEPART][j]) + " € </strong>" + "</h4></b>"

                    folium.GeoJson(decoded).add_child(folium.Popup(Dis_tx+Pr_tx, max_width=300)).add_to(m)

                    folium.Marker(
                                crd[0][::-1],
                                popup=DEPART,
                                icon=folium.Icon(color='red', icon='car', prefix='fa')
                                ).add_to(m)

                    folium.Marker(
                                crd[1][::-1],
                                popup=ARRIVEE,
                                icon=folium.Icon(color='blue', icon='car', prefix='fa')
                                ).add_to(m)
            return m

        elif i > j:

            cor = [y, x]

            for i in range(0, len(cor)-1):
                crd = cor[i], cor[i+1]
                crr = client.directions(crd)

                with(open('test.json', '+w')) as f:
                    f.write(json.dumps(crr, indent=4, sort_keys=True))

                    geometry = client.directions(crd)['routes'][0]['geometry']
                    decoded = convert.decode_polyline(geometry)

                    Dis_tx = "<h4> Distance :&nbsp" + "<strong>"+str(round(crr['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
                    Pr_tx = "<h4> Prix :&nbsp" + "<strong>"+str(price[DEPART][j]) + " € </strong>" + "</h4></b>"

                    folium.GeoJson(decoded).add_child(folium.Popup(Dis_tx+Pr_tx, max_width=300)).add_to(m)

                    folium.Marker(
                                crd[0][::-1],
                                popup=DEPART,
                                icon=folium.Icon(color='red', icon='car', prefix='fa')
                                ).add_to(m)

                    folium.Marker(
                                crd[1][::-1],
                                popup=ARRIVEE,
                                icon=folium.Icon(color='blue', icon='car', prefix='fa')
                                ).add_to(m)
            return m

        else:
            print("Choisissez deux villes différentes")
            
        
interact(map.road, DEPART=Cities, ARRIVEE=Cities)




# %%
