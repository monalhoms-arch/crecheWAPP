# 🏫 Système de Gestion de Crèche

Application web complète pour la gestion d'une crèche, développée avec Flask et MongoDB.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Rôles et permissions](#rôles-et-permissions)
- [Captures d'écran](#captures-décran)
- [Contribuer](#contribuer)
- [Licence](#licence)

## ✨ Fonctionnalités

### 👨‍💼 Administration
- Gestion complète des utilisateurs (CRUD)
- Gestion des profils (Parents, Éducateurs, Diététiciens)
- Gestion des enfants et groupes
- Gestion des paiements et facturation
- Intégration API Chargily pour paiements en ligne
- Système de communication (messages, plaintes)

### 👨‍🏫 Éducateurs
- **Présences** : Système de registre quotidien
  - Vue complète de tous les enfants
  - Suivi des heures d'arrivée/départ
  - Statistiques en temps réel
  - Blocage des dates futures
- **Activités** : Planification et gestion des activités
- **Groupes** : Gestion des groupes d'enfants
- Communication avec les parents

### 👨‍⚕️ Diététiciens
- Création et gestion des repas
- Planification des menus hebdomadaires
- Plans nutritionnels personnalisés par enfant
- Suivi des restrictions alimentaires et allergies
- Enregistrement des repas consommés

### 👨‍👩‍👧 Parents
- **Portail Parent** complet (lecture seule)
  - Suivi des présences de leurs enfants
  - Consultation des activités planifiées
  - Accès aux plans nutritionnels
  - Consultation des menus hebdomadaires
- Gestion des paiements
- Communication avec l'administration
- Dépôt de plaintes

## 🛠 Technologies utilisées

### Backend
- **Flask** - Framework web Python
- **MongoDB** - Base de données NoSQL
- **Flask-Login** - Gestion de l'authentification
- **Werkzeug** - Hashage des mots de passe
- **Chargily API** - Passerelle de paiement

### Frontend
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Bibliothèque d'icônes
- **Jinja2** - Moteur de templates
- **JavaScript** - Interactivité client

### Outils de développement
- **Mermaid** - Génération de diagrammes UML
- **Docker** - Conteneurisation (optionnel)

## 📦 Installation

### Prérequis
- Python 3.8+
- MongoDB 4.4+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/gestion_creche_final.git
cd gestion_creche_final
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer MongoDB**
```bash
# Démarrer MongoDB
mongod --dbpath /path/to/data
```

5. **Créer le fichier de configuration**
```bash
# Créer .env à la racine
cp .env.example .env
```

## ⚙️ Configuration

### Fichier `.env`
```env
# MongoDB
MONGO_URI=mongodb://localhost:27017/creche_db

# Flask
SECRET_KEY=votre_cle_secrete_tres_longue_et_aleatoire
FLASK_ENV=development

# Chargily API (optionnel)
CHARGILY_API_KEY=votre_cle_api_chargily
CHARGILY_SECRET=votre_secret_chargily
```

### Initialisation de la base de données

```bash
python init_db.py
```

Cela créera :
- Un utilisateur admin par défaut (username: `admin`, password: `admin123`)
- Les collections nécessaires
- Des données de test (optionnel)

## 🚀 Utilisation

### Démarrer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

### Connexion par défaut

**Administrateur**
- Username: `admin`
- Password: `admin123`

⚠️ **Important** : Changez le mot de passe admin après la première connexion !

### Créer les premiers utilisateurs

1. Connectez-vous en tant qu'admin
2. Allez dans "Profils" → "Utilisateurs System"
3. Créez les profils nécessaires (Parents, Éducateurs, Diététiciens)
4. Créez les comptes utilisateurs associés

## 🏗 Architecture

```
gestion_creche_final/
├── app.py                 # Point d'entrée de l'application
├── db.py                  # Configuration MongoDB
├── requirements.txt       # Dépendances Python
│
├── controllers/           # Logique métier
│   ├── auth_controller.py
│   ├── parents_controller.py
│   ├── enfants_controller.py
│   ├── presence_controller.py
│   ├── activites_controller.py
│   ├── nutrition_controller.py
│   ├── paiements_controller.py
│   └── ...
│
├── models/               # Modèles de données
│   ├── user.py
│   ├── parent.py
│   ├── enfant.py
│   ├── presence.py
│   └── ...
│
├── templates/            # Templates Jinja2
│   ├── base.html
│   ├── enfants.html
│   ├── presences.html
│   ├── nutrition/
│   └── ...
│
├── static/              # Fichiers statiques
│   ├── style.css
│   └── images/
│
├── utils/               # Utilitaires
│   └── decorators.py   # @admin_required, @role_required
│
└── diagrams/            # Documentation UML
    ├── ERD.md
    ├── Architecture.md
    └── ...
```

## 📚 Documentation

### Diagrammes UML

Le projet inclut une documentation complète avec 12 diagrammes UML :

- **ERD** - Schéma de base de données
- **Architecture** - Vue d'ensemble du système
- **Use Cases** - Cas d'utilisation par rôle
- **Class Diagram** - Modèles de données
- **Sequence Diagrams** - Flux (Login, Payment, Presence)
- **Activity Diagrams** - Processus (Presence, Parent Portal)
- **State Diagram** - États des factures
- **Component Diagram** - Architecture système
- **Deployment** - Infrastructure Docker

📖 Voir [diagrams/README.md](diagrams/README.md) pour plus de détails.

### Guides

- [Walkthrough complet](docs/walkthrough.md) - Guide détaillé des fonctionnalités
- [API Documentation](docs/api.md) - Documentation des endpoints
- [Guide de déploiement](docs/deployment.md) - Instructions de déploiement

## 🔐 Rôles et permissions

| Fonctionnalité | Admin | Éducateur | Diététicien | Parent |
|----------------|-------|-----------|-------------|--------|
| Gestion utilisateurs | ✅ | ❌ | ❌ | ❌ |
| Gestion enfants | ✅ | ❌ | ❌ | 👁️ |
| Gestion groupes | ✅ | ✅ | ❌ | ❌ |
| Présences | ✅ | ✅ | ❌ | 👁️ |
| Activités | ✅ | ✅ | ❌ | 👁️ |
| Nutrition - Repas | ✅ | ❌ | ✅ | ❌ |
| Nutrition - Menus | ✅ | ❌ | ✅ | 👁️ |
| Nutrition - Plans | ✅ | ❌ | ✅ | 👁️ |
| Paiements | ✅ | ❌ | ❌ | ✅ |
| Communication | ✅ | ✅ | ✅ | ✅ |

**Légende** : ✅ Accès complet | 👁️ Lecture seule | ❌ Pas d'accès

## 📸 Captures d'écran

### Dashboard Admin
![Dashboard](docs/screenshots/dashboard.png)

### Système de Présence
![Presences](docs/screenshots/presences.png)

### Portail Parent
![Parent Portal](docs/screenshots/parent_portal.png)

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment procéder :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Standards de code

- Suivre PEP 8 pour Python
- Commenter le code complexe
- Écrire des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation

## 🐛 Signaler un bug

Utilisez les [GitHub Issues](https://github.com/votre-username/gestion_creche_final/issues) pour signaler des bugs.

## 📝 Changelog

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique des versions.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Développement initial* - [VotreGitHub](https://github.com/votre-username)

## 🙏 Remerciements

- Bootstrap pour le framework CSS
- MongoDB pour la base de données
- Flask pour le framework web
- Chargily pour l'API de paiement
- La communauté open source

## 📞 Contact

Pour toute question ou suggestion :
- Email: votre.email@example.com
- GitHub: [@votre-username](https://github.com/votre-username)
- LinkedIn: [Votre Profil](https://linkedin.com/in/votre-profil)

---

**Note** : Ce projet a été développé dans le cadre de la gestion d'une crèche. Il peut être adapté pour d'autres types d'établissements éducatifs.

Fait avec ❤️ en Algérie 🇩🇿
