# Hangman

Projet de jeu du pendu réalisé en Python. Il comprend une version graphique avec Pygame, une version en ligne de commande et un script pour générer un guide PDF.

## Prérequis

- Python 3
- Les dépendances listées dans `requirements.txt`

## Installation

Depuis la racine du projet, installe les dépendances avec :

```powershell
python -m pip install -r requirements.txt
```

## Lancer le jeu graphique

Dans PowerShell, depuis la racine du projet :

```powershell
cd .\hangman
python ".\full game.py"
```

Le jeu graphique dessine son décor dans la fenêtre. Il ne charge pas `background.png`.

## Lancer la version en ligne de commande

Depuis la racine du projet :

```powershell
python .\hangman\challenge.py .\hangman\my_wordlist.txt
```

Des options permettent de personnaliser la partie :

```powershell
python .\hangman\challenge.py .\hangman\my_wordlist.txt --penalties 6 --length 5 --theme animaux
```

- `--penalties` : nombre maximal de pénalités (12 par défaut).
- `--length` : longueur du mot à choisir (facultatif).
- `--theme` : thème affiché au début de la partie (`general` par défaut).

## Générer le guide PDF

Depuis la racine du projet :

```powershell
python .\hangman\generer_guide.py
```

Le fichier PDF est généré dans le dossier `hangman`.