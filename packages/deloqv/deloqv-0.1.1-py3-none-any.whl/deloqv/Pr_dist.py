#%%
import openrouteservice as ors
from openrouteservice import convert
client = ors.Client(key='5b3ce3597851110001cf6248ec32a01981c344289c76bd7dbc72c78d')
import folium

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import widgets, interact, interactive, fixed , interact_manual

from download import download  # download data / avoid re-downloading
from IPython import get_ipython

pd.options.display.max_rows = 8


#%%
#Importation du tableau des coordonnées des gares de péages

ur1 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/coordonnees_clean.csv'
path = os.path.join(os.getcwd(),'coordonnees_clean.csv')
download(ur1, path, replace=True)
df = pd.read_csv('./coordonnees_clean.csv')

#Importation du tableau des prix entre chaque gares de péages

ur2 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/prices_clean.csv'
path = os.path.join(os.getcwd(),'prices_clean.csv')
download(ur2, path, replace=True)
dp = pd.read_csv('./prices_clean.csv')
Cities = df.NOMGARE.unique()


#%%
#Fonction qui renvoi le nom de la i_eme gare de péage 
def nom_gare(df,i):
    if isinstance(i,int)== True and 0<=i<=35:
        
        return str(df["NOMGARE"][i])  
    
    else: 
        return "veuillez inserer un entier entre 0 et 42"


#%%
def distance(i,j,df):
    coords = ((df["X"][i],df["Y"][i]),(df["X"][j],df["Y"][j]))
    res = client.directions(coords, preference="fastest")
    dist=float(round(res['routes'][0]['summary']['distance']/1000,1))
    return dist


#%% 
def prices_distribution(i,j,bw):
    
    n_bins = 24
    alpha = 0.25
    density = False

    vector = []  
    noms = []
    for k in range(j-1):
        vector.extend([float(dp[nom_gare(df,i+k)][i+k+1])/float(distance(i+k,i+k+1,df))])
        noms.extend(nom_gare(df,i+k))
    A = np.asarray(vector)
    noms.extend(nom_gare(df,j))

    sns.kdeplot(A, bw_adjust=bw, shade=True, cut=0)
    plt.title("Distribution des prix entre " + str(nom_gare(df,i)) + " et " + str(nom_gare(df,j)))
    plt.xlabel("Prix/km")
    plt.ylabel("Niveau de densité")
    plt.tight_layout()
    plt.show()
    
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.hist(A, density=density, bins=n_bins, alpha=alpha)  # standardization
    plt.title("Distribution des prix entre " + str(nom_gare(df,i)) + " et " + str(nom_gare(df,j)))
    plt.xlabel("Prix/km")
    plt.ylabel("Niveau de densité")
    plt.tight_layout()
    plt.show()
    
#%%
prices_distribution(3,9,0.5)



# %%

# %%

# %%
