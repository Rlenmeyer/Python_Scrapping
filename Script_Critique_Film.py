#!/usr/bin/env python
# coding: utf-8

# # Script Critique de film 
# 
# - Déclarer des listes pour stocker les informations 
# - Préparer l'écran d'affichage de la boucle 
# - Ecrire une boucle qui fait varier le paramètre release_date de l'URL avec les valeurs de la liste years_url
# - Faire une requête GET sur la boucle des pages
# - Faire pauser la boucle avec des intervalles de 8 à 15 sec 
# - Afficher à l'écran le temps de requete
# - Ajouter un warning pour tout code status différent de 200 
# - Arreter la boucle si le nombre de requete est supérieur à celui attendu (72 pages)
# - Convertir le contenu HTML en contenu BeautifulSoup
# - Ecrire une boucle qui parcours tout les containers 
# - Extraire les infos de tous les containers si une note Metascore est présente

# In[9]:


# Import des librairies nécessaires 
from requests import get
from bs4 import BeautifulSoup 
import pandas as pd
from time import sleep
from random import randint 
from time import time 
from IPython.display import clear_output
from warnings import warn

# Déclarations des listes pour l'URL 
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

# On crée des listes vides pour toutes nos informations 
names = []
years= []
imdb_ratings = []
metascores = []
votes = []

start_time = time() # On fixe le temps de début 
requests=0 # La variable requests va compter le nombre de requete

# Boucle sur l'année 
for year_url in years_url: 
    
    for page in pages:
        
        requests +=1

        # On ajoute l'année dans l'URL
        url='https://www.imdb.com/search/title/?release_date={}&sort=num_votes,desc&page={}'.format(year_url, page)

        # Télécharger la page et assigner le résultat à la variable response
        response=get(url)

        sleep(randint(8,15)) # Pause de 8 à 15 sec
        elapse_time=time()-start_time # On calcule le temps écoulé
        print('Requests : {} : Frequency : {} requests/s'.format(requests,requests/elapse_time))
        clear_output(wait=True)

        if response.status_code != 200: 
            warn('Attention ERROR CODE 200')
        if requests>72:
            warn('Attention nombre de requetes trop important')
            break
        
        # Extraire le code HTML
        html_soup=BeautifulSoup(response.content,'html.parser')
        # Utiliser la méthode find_all pour extraire les films
        movie_containers=html_soup.find_all('div', class_='lister-item mode-advanced')

        # On reprend movie_containers pour y extraire l'informations 
        for container in movie_containers: 

            # Si le film a une note metascore on l'extrait 
            if container.find('div',class_='ratings-metascore') is not None: 
                
                # Liste des noms de films
                name=container.h3.a.text
                names.append(name) 
                
                # Liste des années de sortie
                year=container.h3.find(class_='lister-item-year text-muted unbold').text
                years.append(year)
                
                # Liste des notes imdb
                imdb_rating=float(container.strong.text)
                imdb_ratings.append(imdb_rating)

                # Liste des notes metascore
                metascore= int(container.find('span',class_='metascore').text)
                metascores.append(metascore)

                # Liste des nombres de vote
                vote=int(container.find('span', attrs={'name':'nv'})['data-value'])
                votes.append(vote)


# In[12]:


movie_ratings=pd.DataFrame({
    'movie': names,
    'year': years, 
    'imdb': imdb_ratings, 
    'metascore': metascores, 
    'vote': votes  
    })
movie_ratings.head(100)


# In[ ]:




