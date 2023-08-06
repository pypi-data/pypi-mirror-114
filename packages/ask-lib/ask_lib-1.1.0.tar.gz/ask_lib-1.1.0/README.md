# ASK Lib

## Présentation

`ask_lib` est un module pour le langage Python proposant une seule fonction; `ask()`.
Le but principal de cette fonction est de proposer un wrapper de la fonction `input()` pour demander la confirmation de l'utilisateur avant de réaliser une action. `ask_lib` est donc particulièrement utile pour la création de [CLI](https://fr.wikipedia.org/wiki/Interface_en_ligne_de_commande).

## Exemple
```py
import os

from ask_lib import AskResult, ask

reponse = ask("Êtes-vous sûr de vouloir supprimer ce fichier ?", AskResult.YES)
if reponse:
    try:
        os.remove("fichier.txt") # Supprime le fichier | A titre d'exemple
    except Exception:
        print("Quelque chose s'est mal passé...")
    else:
        print("Le fichier vient d'être supprimé.")
else:
    print("Le fichier n'a pas été supprimé.") 
```

Point de vu de l'utilisateur ;
```
Êtes-vous sûr de vouloir supprimer ce fichier ? [Y/n] n
Le fichier n'a pas été supprimé.
```
```
Êtes-vous sûr de vouloir supprimer ce fichier ? [Y/n] y
Le fichier vient d'être supprimé.
```

Pour en savoir plus, cliquez [ICI](https://github.com/CallMePixelMan/ask_lib).

## Mise à jour
> ### 1.1.0
> Ajout du paramètre `flag` pour la fonction `ask()`. Permet de passer la confirmation en spécifiant un choix par défaut.