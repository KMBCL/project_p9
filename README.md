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

## 4. Lancer le serveur

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

## Rapport flake8

```bash
flake8
```

Le rapport HTML est généré dans le dossier `flake8-report/` (configuration dans `.flake8`).
