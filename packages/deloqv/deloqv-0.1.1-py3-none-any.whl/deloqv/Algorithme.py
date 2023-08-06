#%%
import numpy as np
import pandas as pd
from download import download
import os
from ipywidgets import interact



#%%

ur1 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/coordonnees_clean.csv'
path = os.path.join(os.getcwd(),'coordonnees_clean.csv')
download(ur1, path, replace=True)
df = pd.read_csv('./coordonnees_clean.csv')

ur2 = 'https://raw.githubusercontent.com/ELKHMISSI/Project/main/data/prices_clean.csv'
path = os.path.join(os.getcwd(),'prices_clean.csv')
download(ur2, path, replace=True)
dp = pd.read_csv('./prices_clean.csv')

Cities = df.NOMGARE.unique()

#%%
#Partitionnement des routes
p1 = df.iloc[0:10,:]
P1 = p1.sort_index(axis=0,ascending = False)
P1 = P1.reset_index()

P2 = df.iloc[10:16,:]
P2 = P2.reset_index()

P3 = df.iloc[16:22,:]
P3 = P3.reset_index()

P4 = df.iloc[22:26,:]
P4 = P4.reset_index()

P5 = df.iloc[26:36,:]
P5 = P5.reset_index()

#%%
#Exemple de partitionnement
P5


#%%
#Groupement des partitions
V1 = pd.concat([P1,P2])
V2 = P3
V3 = pd.concat([P4,P5])

#%%
#Exemple de groupe
V3

#%%
#Associe la gare a sa partition
def partition_gare(i):
    if i>=0 and i<=9 :
        return P1
    if i>=10 and i<=15 :
        return P2
    if i>=16 and i<=21 :
        return P3
    if i>=22 and i<=25 :
        return P4
    if i>=26 and i<=35 :
        return P5

#%%
#test 
partition_gare(35)

#%%
#Associe la gare au nom de sa partition
def nom_partition_gare(i):
    if i>35 :
        return ("Choisissez un numéro entre 0 et 36")
    else:
        if i>=0 and i<=9 :
            return "P1"
        if i>=10 and i<=15 :
            return "P2"
        if i>=16 and i<=21 :
            return "P3"
        if i>=22 and i<=25 :
            return "P4"
        if i>=26 and i<=35 :
            return "P5"

#%%
nom_partition_gare(35)

#%%
#Associe la partition a son groupement
def groupe_de_la_partition(i):
    if i>35 :
        return ("Choisissez un numéro entre 0 et 36")
    else:
        if nom_partition_gare(i) == "P1" or nom_partition_gare(i) == "P2" :
            return V1
        if nom_partition_gare(i) == "P4" or nom_partition_gare(i) == "P5" :
            return V3
        if nom_partition_gare(i)== "P3":
            return V2

#%%
groupe_de_la_partition(35)

#%%
#Associe la partition au nom de son groupement
def nom_groupe_partition(i):
    if i>35 :
        return ("Choisissez un numéro entre 0 et 36")
    else:
        if nom_partition_gare(i) == "P1" or nom_partition_gare(i) == "P2" :
            return "V1"
        if nom_partition_gare(i) == "P4" or nom_partition_gare(i) == "P5" :
            return "V3"
        else :
            return "V2"

#%%
nom_groupe_partition(35)


#%%
#Renvoie le nombre de gare par partition
def nb_de_gare_partition(i):
    if i>35 :
        return ("Choisissez un numéro entre 0 et 36")
    else:
        return len(partition_gare(i))

#%%
nb_de_gare_partition(35)



#%%
#Renvoie le nombre de gare presente sur le trajet entre la gare i et la gare j
def nb_de_gare_sur_trajet(i,j):
    if i>35 or j>35:
        return ("Choisissez des numéros entre 0 et 36")
    else:
        if nom_partition_gare(i)== nom_partition_gare(j) :
            if i==j or abs(i-j)==1 :
                return 0
            return (abs(i-j)-1)
        else :
            if nom_groupe_partition(i)==nom_groupe_partition(j) :
                if partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] == partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] == 0:
                    return 0
                else :
                    return partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] + partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]
            else :
                if (nom_groupe_partition(i)!= "V2") and (nom_groupe_partition(j)!= "V2") :
                    if partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] == partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] == 0:
                        return nb_de_gare_partition(23)
                    else :
                        return partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] + partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] + nb_de_gare_partition(23) 
                else :
                    if nom_groupe_partition(i)=="V2" :
                        if partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] == partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] == 0  or  partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]-5 == partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] == 0:
                            return 0
                        else : 
                            if nom_groupe_partition(j)=="V1":
                                return partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] + partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]
                            if nom_groupe_partition(j)=="V3":
                                return (partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]-nb_de_gare_partition(23)) + partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]
                    if nom_groupe_partition(j)=="V2":
                        if partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] == partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0] == 0  or  partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]-5 == partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] == 0:
                            return 0
                        else : 
                            if nom_groupe_partition(i)=="V1":
                                return partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0] + partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]
                            if nom_groupe_partition(i)=="V3":
                                return (partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]-nb_de_gare_partition(23)) + partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]
                    
#%%
nb_de_gare_sur_trajet(35,3)




# %%
#Renvoie le dataframe ordonnée des gares entre la gare i et j du trajet (i,j)
def tab_algo(i,j):
    if i>35 :
        return ("Choisissez des numéros entre 0 et 36")
    else:
        if nom_partition_gare(i)== nom_partition_gare(j) :
            if i==j :
                return "Veuiller entrer deux chiffre différents"
            else :
                if i<j :
                    df1 = df.iloc[i:j+1,:]
                    return df1
                else :
                    df1 = df.iloc[j:i+1,:]
                    DF1 = df1.sort_index(axis=0,ascending = False)
                    return DF1
        
        else :
            
            if nom_groupe_partition(i)==nom_groupe_partition(j) :
                df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                df2 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                DF2 = df2.sort_index(axis=0,ascending = False)
                return pd.concat([DF2,df1])
                
            else :
                if (nom_groupe_partition(i)!= "V2") and (nom_groupe_partition(j)!= "V2") :
                    if nom_groupe_partition(i)=="V1":
                        df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                        df2 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                        DF2 = df2.sort_index(axis=0,ascending = False)
                        return pd.concat([DF2,V2,df1])
                    else :
                        df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                        df2 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                        DF2 = df2.sort_index(axis=0,ascending = False)
                        DV2 = V2.sort_index(axis=0,ascending=False)
                        return pd.concat([DF2,DV2,df1])
                    
                else :
                    if nom_groupe_partition(i)=="V2" :
                        if nom_groupe_partition(j)=="V1":
                            df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                            df2 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                            DF2 = df2.sort_index(axis=0,ascending = False)
                            return pd.concat([DF2,df1])
                        
                        else :
                            df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                            df2 = partition_gare(i).iloc[partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1:nb_de_gare_partition(23),:]
                            DF2 = df2.sort_index(axis=0,ascending = False)
                            return pd.concat([DF2,df1])
                    
                    
                    if nom_groupe_partition(j)=="V2":
                        if nom_groupe_partition(i)=="V1":
                            df1 = partition_gare(j).iloc[0:partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1,:]
                            df2 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                            DF2 = df2.sort_index(axis=0,ascending = False)
                            return pd.concat([DF2,df1])
                        
                        else :
                            df1 = partition_gare(i).iloc[0:partition_gare(i)[partition_gare(i)['index']==i].index.values.astype(int)[0]+1,:]
                            df2 = partition_gare(j).iloc[partition_gare(j)[partition_gare(j)['index']==j].index.values.astype(int)[0]+1:nb_de_gare_partition(23),:]
                            DF1 = df1.sort_index(axis=0,ascending = False)
                            return pd.concat([DF1,df2])

#%%
tab_algo(3,35)


#%%
def index_gare(dataframe,gare):
    data_gare = dataframe[dataframe["NOMGARE"]==gare]
    index = int(data_gare["index"])
    return index

#%%
index_gare(df,'Vendargues')



#%%
#renvoi le nom de la gare en fonction de son index
def nom_gare(dataframe,i):
    if i>35 :
        return ("Choisissez un numéro entre 0 et 36")
    else:
        return str(dataframe["NOMGARE"][i])  

#%%
nom_gare(df,35)


#%%
def Le_Trajet(dataframe):
    tab = dataframe[["index","ROUTE","NOMGARE","X","Y"]]
    tab = tab.reset_index()
    return tab

#%%
Le_Trajet(tab_algo(3,35))

#%%
tab = Le_Trajet(tab_algo(3,35))
gare = nom_gare(df,35)
index_gare(tab,gare)
index_gare(Le_Trajet(tab_algo(6,7)),nom_gare(df,7))


#%%
#renvoi le cout minimum entre pour le trajet de i a j
def cout_minimum(tab_ord_gares,dep,arr) :

    min_cout=float(dp[nom_gare(tab_ord_gares,dep)][index_gare(df,nom_gare(tab_ord_gares,arr))])

    for l in range(arr):
        
        cout = float(dp[nom_gare(tab_ord_gares,dep)][index_gare(df,nom_gare(tab_ord_gares,l))]) + float(dp[nom_gare(tab_ord_gares,l)][index_gare(df,nom_gare(tab_ord_gares,arr))])

        if cout < min_cout :
            min_cout = cout
            sortie = nom_gare(tab_ord_gares,l)
    economie = round(float(dp[nom_gare(tab_ord_gares,dep)][index_gare(df,nom_gare(tab_ord_gares,arr))]) - min_cout,2)          
    return "Si vous sortez a " + sortie + " votre trajet vous coutera " + str(round(min_cout,2)) + " €. Vous aurez ainsi fait une economie de " + str(economie) + " € sur le coût des péages." 

#%%
cout_minimum(df,3,9)
#%%
cout_minimum(Le_Trajet(tab_algo(3,35)),0,16)



#%%
def arrangements_v1(p,n): 
  
    if p>n:  
        return 
  
    indices=list(range(p)) # on initialise la liste des indices [0,1,2,..,p-1] 
    yield tuple(indices) # ordre pour générer le tuple  
  
    i=p-1 # on part de la fin de la liste des indices 
    k=p # variable utilisé pour incrémenter ou initialiser les indices 
  
    while i!=-1: # on parcourt les indices de la droite vers la gauche : p-1 -> 0 
        if k < n: # si la valeur d'indice maxi n'a pas été dépassée 
            if k not in indices[:i]: # si l'indice k n'est pas présent parmi les indices précédant indices[i] 
                indices[i]=k # on incrémente indices[i] avec la valeur de k 
                k=0;j=i+1 # on met k à 0 pour ensuite initialiser les prochains indices : nouveau cycle (ex. : 0,1,2,..). 
                while (j < p): # on parcourt les prochains indices  
                    if k not in indices[:i+1]: # si l'indice k n'est pas présent parmi les indices précédant indices[i+1] 
                        indices[j]=k # on initialise indices[j] avec la valeur de k 
                        j+=1 # prochain indice 
                    k+=1 
                yield tuple(indices) # ordre pour générer le tuple 
                i=p-1 # on revient sur le dernier indice à incrémenter  
                k=indices[i] 
            k+=1 # on incrémente k 
        else: # sinon 
            i-=1 # on remonte les indices vers la gauche 
            k=indices[i]+1 # on met à jour k pour le prochain indice 
  
    return 

#%%
def liste_des_tuples(p,n):
    iterator = arrangements_v1(p,n) 
    list_tuple = []
    for a in iterator: 
        b = sorted(a)
        if b == list(a) and b[len(a)-1]== n-1 and b[0]==0:
            list_tuple.extend([a])
    return list_tuple



#%%

def suite_de_trajet(p,n):
    list_tuples = liste_des_tuples(p,n)
    suite_tuple = []
    for l in range(len(list_tuples)):
        tuple = list_tuples[l]
        trajet = []
        for a in range(len(tuple)-1):
            i = tuple[a]
            j = tuple[a+1]
            trajet.extend([(i,j)])
        suite_tuple.extend([trajet])
    
    return suite_tuple



# %%
def cout_minimum_tuple(i,j,k,tab_ord_gares) :
    n = nb_de_gare_sur_trajet(i,j)+2
    trajets = suite_de_trajet(k+2,n)
    min_cout=float(dp[nom_gare(tab_ord_gares,i)][index_gare(df,nom_gare(tab_ord_gares,j))])

    for l in range(len(trajets)):
        
        t = trajets[l]
        cout_t = 0
        sorties = []
        
        for a in range(len(t)):
            
            s = t[a]
            cout1 = float(dp[nom_gare(tab_ord_gares,s[0])][index_gare(df,nom_gare(tab_ord_gares,s[1]))]) 
            cout_t = cout_t + cout1 
            
            if a < (len(t)-1):
                gare = [nom_gare(tab_ord_gares,s[1])]
                sorties.extend(gare)
            
        les_sorties = sorties
        
        if cout_t < min_cout :
            min_cout = cout_t
            x = les_sorties


    economie = round(float(dp[nom_gare(tab_ord_gares,i)][index_gare(df,nom_gare(tab_ord_gares,j))]) - min_cout,2)          
    print( "Si vous sortez aux gares :\n(" + ','.join(x) + "), votre trajet vous coutera " + str(round(min_cout,2)) + " €.\nVous aurez ainsi fait une economie de " + str(economie) + " € sur le coût des péages." )

#%%

# %%
#Renvoi le parcours le moins cher pour le trajet de la gare i a j

def chemin_moins_cher(Depart,arrivee,Nb_sortie):
    nb_de_noeuds_possible = nb_de_gare_sur_trajet(Depart,arrivee)
    nb_de_noeuds_souhaite = Nb_sortie

    if nb_de_noeuds_possible  < nb_de_noeuds_souhaite :
        return "Choisissez un nombre de noeuds inferieur ou egal a : " + str(nb_de_noeuds_possible) 

    else :
        
        data = tab_algo(Depart,arrivee)
        trajet = Le_Trajet(data)
        
        depart_index = 0
        arrivee_index = len(trajet) - 1
        
        if nb_de_noeuds_souhaite == 0 :
            return "Le prix de votre trajet est de : " + str(dp[nom_gare(trajet,depart_index)][index_gare(df,nom_gare(trajet,arrivee_index))]) + " €"

        if nb_de_noeuds_souhaite == 1 :
            return cout_minimum(trajet,depart_index,arrivee_index)
        
        else :
            return cout_minimum_tuple(depart_index,arrivee_index,nb_de_noeuds_souhaite,trajet)


# %%
interact(chemin_moins_cher, Depart=list(range(0,36)),arrivee=list(range(0,36)),Nb_sortie=list(range(0,22)))

#%%
chemin_moins_cher(3,15,3)


# %%
