#%%
import numpy as np
import pandas as pd
from download import download
import csv
import os


#%%
ur1 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/coordonnees_algo.csv'
path = os.path.join(os.getcwd(),'coordonnees_algo.csv')
download(ur1, path, replace=True)
df = pd.read_csv('./coordonnees_algo.csv',sep=",")

ur2 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/price_algo.csv'
path = os.path.join(os.getcwd(),'price_algo.csv')
download(ur2, path, replace=True)
dp = pd.read_csv('./price_algo.csv',sep=";")


#%%
########### Data Cleaning du dataframe des coordonnees ###########
# %%
df.drop([5,8,17,18,28,32,34],0,inplace=True)
# %%
df = df.reset_index()
# %%
df['index'] = df.index
# %%
del df["level_0"]

#%%
########### Data Cleaning du dataframe des prix ###########
# %%
dp.drop([5,8,17,18,28,32,34],0,inplace=True)
#%%
columns = ["Peage de Montpellier St-Jean","Peage de Beziers-Cabrials","Peage du Perthus","Le Boulou (peage sys ouvert)","Peage de pamiers","Peage de Toulouse sud/ouest","Peage de Toulouse sud/est"]
dp.drop(columns,axis = 1,inplace=True)

#%%
dp = dp.reset_index()
# %%
dp['index'] = dp.index
# %%
del dp["index"]
# %%
########### Enregistrement des dataframes cleaned ###########
#%%
df.to_csv('coordonnees_clean.csv',index=False)
#%%
dp.to_csv('prices_clean.csv',index=False)



# %%
