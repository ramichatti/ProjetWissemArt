# Projet WissemArt - Système de Gestion des Achats

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/ramichatti/ProjetWissemArt.git)

## À propos du projet

**WissemArt Achat** est une application de bureau complète conçue pour la gestion et le suivi des factures d'achats de l'entreprise WissemArt. Le projet combine une interface utilisateur intuitive développée en Python/Tkinter, un processus ETL automatisé avec Talend, et un tableau de bord analytique Power BI pour un suivi efficace des achats.

## Objectifs

- Centraliser la gestion des factures d'achat
- Suivre les achats par fournisseur, produit et catégorie
- Automatiser le traitement et l'intégration des données
- Fournir des analyses visuelles pour la prise de décision
- Assurer la traçabilité complète des transactions d'achat

## Architecture du Projet

`
WissemProject/
+-- App/                    # Application Desktop Tkinter
¦   +-- AppAchat.py        # Application principale
¦   +-- create_shortcut.vbs # Générateur de raccourci bureau
¦   +-- START_HERE.bat    # Menu d'installation
¦   +-- WissemArt_Achat.bat # Lanceur direct
¦   +-- LogoWissem.ico    # Icône de l'application
¦   +-- __pycache__/      # Fichiers compilés Python
+-- Data/                   # Données sources (format CSV)
¦   +-- EnteteAchat.csv   # En-têtes des factures
¦   +-- LigneAchat.csv    # Détails des lignes d'achat
+-- PowerBI/               # Rapports et tableaux de bord
¦   +-- DashboardAchats.pbix # Tableau de bord Power BI
+-- Capture/               # Captures d'illustration
+-- README.md             # Documentation
+-- .gitignore
`

## Fonctionnalités Principales

### Application Desktop

- **Gestion des factures** : Création, consultation, modification et suppression des factures d'achat
- **Gestion des lignes de facture** : Ajout de produits avec quantité, prix unitaire et calcul automatique du montant
- **Sélection des fournisseurs** : Enregistrement du nom, matricule fiscal et adresse du fournisseur
- **Modes de paiement** : Prise en charge d'Espèces, Chèque, Virement et Carte Bancaire
- **Validation intelligente** : Contrôles de saisie et validation des données en temps réel
- **Calcul automatique** : Calcul automatique des totaux et montants par ligne
- **Interface moderne** : Design professionnel avec palettes de couleurs cohérentes et expérience utilisateur optimisée
- **Sauvegarde CSV** : Stockage structuré des données au format CSV (UTF-8-SIG, séparateur point-virgule)

## Stack Technique

| Composant | Technologie | Description |
|---|---|---|
| Application Desktop | Python 3.x + Tkinter/TTK | Interface graphique native Windows |
| Stockage des données | CSV | Format simple et portable pour les données d'achat |
| Business Intelligence | Power BI | Visualisation, analyse et tableaux de bord |
| ETL | Talend | Extraction, Transformation et Chargement des données vers l'entrepôt |
| Automatisation Windows | VBScript | Création automatique de raccourcis |
| Scripts Batch | .BAT | Installation et lancement simplifiés |

## Données

### Fichier EnteteAchat.csv - En-têtes de factures
| Colonne | Type | Description |
|---|---|---|
| num_facture | Texte | Numéro unique de facture (PK) |
| date_achat | Date | Date de l'achat (YYYY-MM-DD) |
| nom_fournisseur | Texte | Nom complet du fournisseur |
| matricule_fiscal | Texte | Matricule fiscal du fournisseur |
| adresse_fournisseur | Texte | Adresse du fournisseur |
| mode_paiement | Texte | Mode de règlement |
| total_achat | Décimal | Montant total TTC de la facture |

### Fichier LigneAchat.csv - Lignes de détail
| Colonne | Type | Description |
|---|---|---|
| num_facture | Texte | Clé étrangère vers l'en-tête de facture |
| nom_produit | Texte | Désignation du produit |
| reference | Texte | Référence unique du produit |
| categorie | Texte | Catégorie du produit |
| design | Texte | Désignation détaillée |
| quantite | Numérique | Quantité achetée |
| prix_unitaire | Décimal | Prix unitaire HT/TTC |
| montant_ligne | Décimal | Montant calculé (quantité × prix unitaire) |

## Installation & Démarrage

### Prérequis
- Windows 10/11
- Python 3.8+ installé
- Tkinter (inclus par défaut avec l'installation Python standard)

### Démarrage rapide

1. **Option A - Menu d'installation complet**
   `atch
   Double-cliquez sur : App/START_HERE.bat
   `
   Ce menu vous permet de créer un raccourci sur le bureau ou de lancer directement l'application.

2. **Option B - Lancement direct**
   `atch
   Double-cliquez sur : App/WissemArt_Achat.bat
   `

3. **Option C - Depuis la ligne de commande**
   `ash
   cd App
   python AppAchat.py
   `

## Workflow ETL & Business Intelligence

Le projet intègre un pipeline ETL complet développé sous Talend :

1. **Staging Area** - Import et contrôle qualité des fichiers CSV
2. **Dimensions** - Création des dimensions DimProduit et DimFournisseur
3. **Table de Faits** - Construction de la table de faits FactAchats
4. **Data Warehouse (DWH)** - Modélisation en étoile pour optimiser les analyses
5. **Power BI** - Restitution via le tableau de bord interactif DashboardAchats.pbix

## Captures d'écran

Les captures illustrant l'application, le processus ETL Talend et le tableau de bord Power BI sont disponibles dans le dossier Capture/.

## Remarques

- Les fichiers de données Data/ contiennent des données d'exemple à des fins de démonstration.
- L'application est configurée pour fonctionner depuis C:\Users\ramic\Desktop\WissemProject\ par défaut.
- Les fichiers .pyc dans __pycache__/ sont générés automatiquement lors de l'exécution.

## Auteur

**WissemArt** - Projet de gestion des achats développé par Wissem

## Licence

Ce projet est destiné à un usage professionnel et interne.

