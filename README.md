# Plateforme de Recettes Maison

## Description

Plateforme de Recettes Maison est une application web developpee avec Django. Elle permet aux utilisateurs de consulter, creer, partager, commenter, noter et organiser des recettes de cuisine.

Le projet propose une interface simple pour les visiteurs, un espace utilisateur pour gerer ses recettes et un espace d'administration pour moderer le contenu publie.

## Membres du Projet

- Soumaya Sakkaoui
- Fatima Ezahra Mouslih
- Kawtar Zaim Sassi

Classe: 3IIR G7

## Technologies Utilisees

- Python
- Django
- MySQL
- HTML
- CSS
- Bootstrap
- JavaScript

## Fonctionnalites Principales

### Gestion des Recettes

- Affichage de la liste des recettes.
- Consultation du detail d'une recette.
- Creation de recettes par les utilisateurs connectes.
- Modification et suppression des recettes par leur auteur.
- Ajout d'une image pour chaque recette.
- Classification par categorie et tags.
- Recherche et filtrage des recettes.

### Evaluation des Recettes

- Systeme de notation sur 5 etoiles.
- Un utilisateur connecte peut noter une recette.
- Affichage de la moyenne des notes et du nombre de votes.

### Commentaires

- Les utilisateurs connectes peuvent commenter les recettes.
- Les commentaires peuvent etre moderes depuis l'administration.
- Seuls les commentaires approuves sont affiches publiquement.

### Favoris

- Les utilisateurs connectes peuvent ajouter ou retirer une recette de leurs favoris.

### Fonctionnalites Avancees

- Gestion du nombre de portions d'une recette.
- Ajustement automatique des quantites des ingredients selon le nombre de portions choisi.
- Valeurs nutritionnelles optionnelles:
  - Calories
  - Proteines
  - Glucides
  - Lipides
- Suggestions de recettes similaires selon la categorie et les tags.
- Creation d'un menu hebdomadaire pour organiser les recettes par jour et par type de repas.

### Administration

- Moderation des recettes avec plusieurs statuts:
  - Brouillon
  - En attente
  - Approuvee
  - Rejetee
- Moderation des commentaires.
- Mise en avant de recettes sur la page d'accueil.
- Gestion des categories.
- Gestion des tags.
- Gestion des notes, favoris et menus hebdomadaires.

## Structure du Projet

```text
Platforme_de_recettes/
├── backend/
│   ├── backend/          # Configuration principale Django
│   ├── base/             # Page d'accueil et templates globaux
│   ├── recettes/         # Recettes, commentaires, notes, favoris, menus
│   ├── category/         # Gestion des categories
│   ├── tag/              # Gestion des tags
│   ├── users/            # Authentification et profils utilisateurs
│   ├── ingredient/       # Module ingredients
│   ├── photo/            # Module photos
│   └── manage.py
├── env/                  # Environnement virtuel Python
└── README.md
```

## Installation et Lancement

### 1. Ouvrir le Projet

```powershell
cd C:\Users\PC\Platforme_de_recettes
```

### 2. Activer l'Environnement Virtuel

```powershell
.\env\Scripts\activate
```

### 3. Entrer dans le Dossier Backend

```powershell
cd backend
```

### 4. Verifier la Base de Donnees

Le projet utilise MySQL avec la base de donnees:

```text
dbculinary
```

Il faut s'assurer que MySQL est lance et que la base `dbculinary` existe.

### 5. Appliquer les Migrations

```powershell
python manage.py migrate
```

### 6. Lancer le Serveur

```powershell
python manage.py runserver
```

### 7. Ouvrir l'Application

Dans le navigateur:

```text
http://127.0.0.1:8000/
```

## Administration

Pour acceder a l'administration Django:

```text
http://127.0.0.1:8000/admin/
```

Si aucun compte administrateur n'existe, creer un superutilisateur:

```powershell
python manage.py createsuperuser
```

Depuis l'administration, l'administrateur peut:

- Approuver ou rejeter les recettes.
- Approuver ou rejeter les commentaires.
- Mettre des recettes en avant sur la page d'accueil.
- Gerer les categories et les tags.
- Consulter les notes et les favoris.

## Utilisation de l'Application

### Visiteur

Un visiteur peut:

- Voir la page d'accueil.
- Consulter les recettes approuvees.
- Rechercher des recettes.
- Filtrer par categorie, temps, difficulte et tags.
- Voir les details d'une recette.

### Utilisateur Connecte

Un utilisateur connecte peut:

- Creer une recette.
- Modifier ou supprimer ses propres recettes.
- Ajouter une recette aux favoris.
- Noter une recette.
- Ajouter un commentaire.
- Creer un menu hebdomadaire.

### Administrateur

Un administrateur peut:

- Moderer les recettes et commentaires.
- Gerer les categories et tags.
- Mettre en avant des recettes.
- Gerer le contenu de la plateforme.

## Commandes Utiles

Verifier le projet:

```powershell
python manage.py check
```

Creer des migrations apres modification des models:

```powershell
python manage.py makemigrations
```

Appliquer les migrations:

```powershell
python manage.py migrate
```

Lancer le serveur:

```powershell
python manage.py runserver
```

## Remarque

Les nouvelles recettes et les nouveaux commentaires peuvent passer par la moderation. Pour qu'ils soient visibles publiquement, ils doivent etre approuves depuis l'interface d'administration.
