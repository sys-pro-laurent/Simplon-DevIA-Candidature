import plotly.express as px
import pandas as pd
import sqlite3

# Charger les données depuis le fichier CSV
données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

# Créer deux connexion à deux bases de données SQLite
connexion1 = sqlite3.connect('ventes_par_produit.db')
connexion2 = sqlite3.connect('ventes_par_region.db')

# Importer les données dans deux tables SQLite
données.to_sql('données', connexion1, index=False, if_exists='replace')
données.to_sql('données', connexion2, index=False, if_exists='replace')

# Exécuter les requêtes SQL Ventes par produit
ventes_par_produit = pd.DataFrame(connexion1.execute("""
    SELECT produit, SUM(prix * qte) AS chiffre_daffaires_produit
    FROM données
    GROUP BY produit;
""").fetchall(), columns=['produit', 'chiffre_daffaires_produit'])

# Exécuter les requêtes SQL Ventes par région
ventes_par_region = pd.DataFrame(connexion2.execute("""
    SELECT region, SUM(prix * qte) AS chiffre_daffaires_region
    FROM données
    GROUP BY region;
""").fetchall(), columns=['region', 'chiffre_daffaires_region'])   

# Tracer les graphiques en utilisant Plotly Express
figure1 = px.pie(ventes_par_produit, values='chiffre_daffaires_produit', names='produit', title='chiffre d\'affaires par produit')
figure2 = px.pie(ventes_par_region, values='chiffre_daffaires_region', names='region', title='chiffre d\'affaires par région')

# Afficher la valeur brute de quantité sur chaque tranche au lieu du pourcentage
figure1.update_traces(textinfo='value')
figure2.update_traces(textinfo='value')

# Enregistrer les graphiques au format HTML
figure1.write_html('ventes-par-produit.html')
print('ventes-par-produit.html généré avec succès !')
figure2.write_html('ventes-par-region.html')
print('ventes-par-region.html généré avec succès !')

# Fermer les connexions aux bases de données
connexion1.close()
connexion2.close()