# READ ME
### Plateforme pour amateurs de Nutella
#### Des aliments sains dans un corps sain
La startup **Pur Beurre** souhaite développer une plateforme web à destination de ses clients soucieux de leur alimentation.
Ce site permettra de trouver un subtitut sain à un aliment considéré comme **trop gras, trop sucré ou en trop sucré**

_______________________________
**Cahier des charges**

Créer une plateforme web pour trouver un subtitut sain.
Pur Beurre doit respecter une dateline. Le site doit être prêt un mois avant le congrès qui aura lieu dans 6 mois.
Le plateforme n'inclut pas pour le moment un mode paiement.
Cette plateforme doit satisfaire les personnes en quête de meilleurs produits, de qualités en un clic.
Il faut suivre la charte graphique déssinée et imaginée par Pur Beurre.
_______________________________
**Comment installer le programme**
Il faut tout d'abord créer un environnement virtuel
``` shell
pip install virtualenv
virtualenv -p python3 myvenv
source myvenv/bin/activate
```
Puis installer les paquets Python-Django
``` shell
pip install -r requirements.txt
```
_______________________________

**Description du parcours utilisateur**

*Customer Journey*

Les utilisateurs pourront s'inscrire sur la plateforme afin de pouvoir gérer leur compte par la suite.
Ils pourront rechercher le produit *malsain* et choisir le subtitut de meilleur qualité.
En effet, ils pourront choisir parmi une liste de subtituts proposés.
Des informations détaillées concernant le subtitut choisi s'afficheront.
* Description de l'aliment
* Liste des magasins dans lequel le prosuit est en vente
* Lien vers la page d'Open Food Facts concernant cet aliment
* Le nutriscore et le novascore
Ils pourront sauvegarder le subtitut choisi dans la base de données.


________________________________
**Fonctionnalités**

* Affichage du champ de recherche dès la page d'accueil
* Interface responsive
* Authentification de l'utilisateur :
    * création de compte en entrant un mail et un mot de passe
    * impossibilité de pour pouvoir changer son mot de passe pour le moment
_____________________________

* Méthode Agile -> Users Stories / Tableau de tâches et sous tâches sur Trello :
https://trello.com/b/iMvWuBbe/p8-creez-une-plateforme-pour-amateurs-de-nutella
* Heroku




