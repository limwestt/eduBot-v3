EduBot V3

Plateforme d'apprentissage intelligente propulsée par l'IA

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)
![Groq](https://img.shields.io/badge/IA-Groq-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Description

EduBot V3 est une plateforme e-learning conçue pour rendre l'apprentissage accessible
sur une grande variété de sujets. Elle intègre une IA conversationnelle via Groq,
un système de progression par XP, des missions pratiques et un système de notifications.

---

## Fonctionnalités

- Assistant IA pédagogique intégré via Groq
- Packs et leçons sur des sujets variés, structurés par niveaux
- Missions pratiques pour consolider les apprentissages
- Système de progression par XP et gamification
- Notifications et alertes en temps réel
- Authentification complète — inscription, connexion, profil
- Espace communautaire entre apprenants

---

## Structure du projet

edubot-v3/
├── apps/
│ ├── accounts/ # Authentification et profils
│ ├── ai/ # Service IA Groq
│ ├── ai_engine/ # Moteur IA
│ ├── community/ # Espace communautaire
│ ├── learning/ # Packs, leçons, dashboard
│ └── practice/ # Missions pratiques
├── config/ # Settings Django
├── templates/ # Templates HTML
├── static/ # Fichiers statiques
├── manage.py
└── requirements.txt

text

---

## Installation

Prérequis : Python 3.10+

```bash
git clone https://github.com/limwestt/eduBot-v3.git
cd eduBot-v3

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env

python manage.py migrate
python manage.py runserver
Variables d'environnement
Crée un fichier .env à la racine du projet :

text
SECRET_KEY=ta_secret_key_django
DEBUG=True
GROQ_API_KEY=ta_cle_groq
DATABASE_URL=sqlite:///db.sqlite3
Stack technique
Technologie	Usage
Django 4.x	Framework backend
Groq API	IA conversationnelle
SQLite	Base de données
HTML / CSS	Templates frontend
Licence
Ce projet est sous licence MIT.

Développé par Espoir HAINGA