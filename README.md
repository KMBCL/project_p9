# LITReview

Application web Django permettant de demander et de publier des critiques de livres ou d'articles.

Projet 9 du parcours Développeur d'application Python (OpenClassrooms).

## Prérequis

- Python 3.12
- Git

## 1. Cloner le dépôt

```bash
git clone https://github.com/KMBCL/project_p9.git
cd project_p9
```

## 2. Créer et activer l'environnement virtuel

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

Une fois activé, le nom `(venv)` apparaît au début de l'invite de commande.

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Fichier `.env`

Les secrets du projet ne sont pas écrits dans le code : `project_p9/settings.py` les lit dans le fichier
`.env` situé à la racine du dépôt (à côté de `manage.py`), via `python-dotenv`.

```ini
SECRET_KEY='...'   # clé secrète Django
DEBUG=True         # mode débogage (False par défaut si absent)
```

Ce fichier est **nécessaire au fonctionnement du projet** : sans `SECRET_KEY`, Django refuse de démarrer.
Il est volontairement inclus dans le dépôt afin que le projet fonctionne directement après un clone.
Pour un déploiement réel, il faudrait le retirer du dépôt et générer une nouvelle clé :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 5. Lancer le serveur

```bash
python manage.py migrate
python manage.py runserver
```

L'application est accessible à l'adresse <http://127.0.0.1:8000/home>.

## Données de démonstration

La base `db.sqlite3` fournie dans le dépôt contient déjà des données de démonstration
(images des tickets dans `media/ticket/`) :

- `UserA`, `UserB` suivent `RSI` ; `RSI` suit `UserC` et `UserD` ; `UserE` ne suit personne ;
- des tickets avec et sans image, des critiques, dont des réponses à ses propres tickets.

Mot de passe des comptes `UserA` à `UserE` : `litreview123`.
Mot de passe superutilisateur pour la démonstration `RSI` : `1234`

## Rapport flake8

```bash
flake8
```

Le rapport HTML est généré dans le dossier `flake8-report/` (configuration dans `.flake8`).
Flake vérifie uniquement le sous dossier core. Le sous dossier project_p9 est généré par django.
