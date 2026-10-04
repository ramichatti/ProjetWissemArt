# Projet WissemArt - Gestion des Achats

## Description

WissemArt Achat est une application desktop developpee en Python/Tkinter pour la gestion des factures d'achats. Le projet integre egalement un workflow ETL (Talend) et un tableau de bord Power BI pour l'analyse des donnees d'achats.

## Structure du Projet

`
WissemProject/
+-- App/                        # Application Desktop (Tkinter)
¦   +-- AppAchat.py            # Interface principale de l'application
¦   +-- create_shortcut.vbs    # Script pour creer un raccourci sur le bureau
¦   +-- START_HERE.bat         # Script d'installation/lancement
¦   +-- WissemArt_Achat.bat    # Lancement direct de l'application
¦   +-- LogoWissem.ico         # Icone de l'application
+-- Data/                       # Donnees sources (CSV)
¦   +-- EnteteAchat.csv        # En-tetes/factures d'achat
¦   +-- LigneAchat.csv         # Lignes de detail des achats
+-- PowerBI/                    # Dashboards BI
¦   +-- DashboardAchats.pbix   # Tableau de bord Power BI
+-- Capture/                    # Captures d'ecran (ETL, PowerBI, etc.)
+-- README.md                   # Ce fichier
+-- .gitignore
`

## Fonctionnalites

L'application de gestion des achats permet de :

- Gerer les factures d'achat : Creer, consulter, modifier et supprimer des factures
- Gerer les lignes de facture : Ajouter des produits avec quantite, prix unitaire, etc.
- Export/Import CSV : Stockage des donnees au format CSV (UTF-8-SIG avec separateur ;)
- Interface moderne : UI/UX professionnelle developpee avec Tkinter/TTK
- Validation des donnees : Controle des champs, calculs automatiques des montants
- Multi-fournisseurs : Gestion des fournisseurs avec matricule fiscal et adresse
- Modes de paiement : Especes, Cheque, Virement, Carte Bancaire

## Technologies Utilisees

- Python 3.x - Langage de developpement
- Tkinter/TTK - Interface graphique desktop
- CSV - Stockage des donnees
- Power BI - Analyse et visualisation des donnees
- Talend - ETL (Extract, Transform, Load)
- VBScript (.vbs) - Creation de raccourcis Windows

## Installation et Utilisation

### Prerequis

- Python 3.x installe sur Windows
- Tkinter (generalement inclus avec Python)

### Lancement de l'application

#### Option 1 : Via le script d'installation
Double-cliquer sur App/START_HERE.bat

#### Option 2 : Lancement direct
Double-cliquer sur App/WissemArt_Achat.bat

#### Option 3 : Via ligne de commande
`ash
cd App
python AppAchat.py
`

## Structure des Donnees

### EnteteAchat.csv
| Champ | Description |
|---|---|
| num_facture | Numero unique de la facture |
| date_achat | Date d'achat (format YYYY-MM-DD) |
| nom_fournisseur | Nom du fournisseur |
| matricule_fiscal | Matricule fiscal du fournisseur |
| adresse_fournisseur | Adresse du fournisseur |
| mode_paiement | Mode de paiement |
| total_achat | Montant total de la facture |

### LigneAchat.csv
| Champ | Description |
|---|---|
| num_facture | Reference vers la facture |
| nom_produit | Nom du produit |
| reference | Reference du produit |
| categorie | Categorie du produit |
| design | Designation du produit |
| quantite | Quantite |
| prix_unitaire | Prix unitaire |
| montant_ligne | Montant de la ligne (qte x PU) |

## Architecture ETL & BI

Le projet integre un processus ETL implemente avec Talend alimentant un DWH et un tableau de bord Power BI (DashboardAchats.pbix).

## Auteur

- Projet : WissemArt
- Developpeur : Wissem

## Licence

Ce projet est a usage professionnel/interne.

