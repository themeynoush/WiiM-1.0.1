# WiiM

Le projet WiiM est un outil d'analyse de données immobilières permettant d'évaluer et de comparer des biens selon différents critères pondérés. Il utilise des z-scores pour normaliser les données et pour identifier des propriétés atypiques ou exceptionnelles parmi un ensemble de biens immobiliers disponibles sur le marché.

## Fonctionnalités

-   Calcul de z-scores pour chaque paramètre numérique d'un bien immobilier.
-   Assignation d'une pondération personnalisable aux paramètres pour prioriser certaines caractéristiques.
-   Identification de propriétés exceptionnelles selon une combinaison de scores pondérés.
-   Visualisation des distributions des z-scores et des scores pondérés.

## Personnalisation

Vous pouvez ajuster les paramètres pour lesquels le z-score est calculé ainsi que les poids pour le calcul du z-score pondéré. Pour cela :

1. **Modifiez le fichier `conf.py`** pour ajuster les noms des paramètres (`param_names`) au besoin :
    - Vous pouvez ajouter ou enlever des paramètres à suivre.
2. **Ajustez les poids** associés à chaque paramètre dans le dictionnaire `weights` :
    - Changez les valeurs pour donner plus de poids à certains critères selon votre analyse.
    - Utilisez un poids positif pour les caractéristiques où un score élevé est avantageux et un poids négatif dans le cas contraire.

## Installation

Pour exécuter ce projet, vous aurez besoin des paquets Python suivants :

-   Numpy
-   Pandas
-   Matplotlib
-   Plotly
-   Scipy
-   Requests
-   Python-dotenv

Utilisez la commande suivante pour installer les dépendances :

```sh
pip install -r requirements.txt
```

## Configuration

Avant de lancer le script, veuillez configurer l'accès à l'API :

1. **Créez un fichier `.env`** à la racine du projet.
2. **Ajoutez votre clé d'API Casafari** comme suit :

```
CASAFARI_API_TOKEN=votre_token_d'api
```

## Exécution

Pour exécuter le script principal, utilisez la commande suivante :

```sh
python index.py
```

## Déploiement

Pour déployer la fonction sur firebase, utilisez la commande suivante:

```sh
firebase deploy
```

## Utilisation

La fonction firebase deployée prend en paramètres les mêmes que le endpoint https://api.casafari.com/v1/properties/search de casafari dont la documentation se trouve ici: https://developer.casafari.com/#operation/postPropertiesSearchResponse

Un paramètres supplémentaire "city" est à fournir et permet de préciser la ville où effectuer la recherche.
