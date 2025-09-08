# Application-web-pour-l-analyse-Exploratoire-des-Donn-es-d-Hygi-ne-des-PME/2
 # Vue d’ensemble

Ce projet est une application d’analyse et de visualisation de données basée sur Streamlit axée sur l’évaluation de l’hygiène pour les petites et moyennes entreprises (PME) en français. L’application fournit des outils d’analyse de données exploratoires pour examiner les pratiques d’hygiène, les obstacles, les programmes de formation et l’analyse comparative entre les entreprises. Il propose des visualisations interactives, notamment des graphiques radar, des résumés statistiques et des comparaisons multidimensionnelles, pour aider à comprendre les modèles de mise en œuvre de l’hygiène dans les environnements commerciaux.

# Préférences de l’utilisateur

Style de communication préféré : Langage simple et quotidien.

# Architecture du système

## Architecture frontend
- **Framework** : Cadre d’application web Streamlit
- **Mise en page** : Mise en page large avec navigation dans la barre latérale extensible
- **Mise en cache** : Utilise le décorateur @st.cache_data de Streamlit pour un chargement efficace des données
- **Navigation** : Sélection de section basée sur un bouton radio dans la barre latérale
- **Internationalisation** : Interface et labels en français

## Architecture de traitement des données
- **Data Layer** : stockage de données basé sur un fichier CSV dans attached_assets répertoire
- **Analysis Module** : Classe DataAnalyzer dédiée pour les calculs statistiques
- **Module de visualisation** : Classe HygieneVisualizer distincte pour la génération de graphiques
- **Validation des données** : Gestion des erreurs pour les problèmes de chargement et d’encodage des fichiers

## Composants clés
- **Application principale (app.py)** : Point d’entrée avec configuration et navigation Streamlit
- **Classe DataAnalyzer** : Gère l’analyse statistique, y compris les intervalles de confiance, les proportions et les statistiques descriptives
- **Classe HygieneVisualizer** : Gère les visualisations interactives avec l’intégration de Plotly

## Schéma de données
- **Pratiques d’hygiène** : Neuf indicateurs d’hygiène de base (BPH, BPF, HACCP, procédures, formation, hygiène du personnel, hygiène des installations, stockage, contrôle de la qualité)
- **Analyse des obstacles** : Quatre catégories d’obstacles (technique, financier, organisationnel, humain)
- **Identification de l’entreprise** : ID d’entreprise uniques pour l’analyse comparative
- **Valeurs de réponse** : Système à trois états (Oui/Non/Inconnu - Oui/Non/Inconnu)

## Stratégie de visualisation
- **Choix de la bibliothèque** : Plotly pour les graphiques interactifs avec prise en charge de la langue française
- **Code couleur** : Schéma de couleurs sémantique (vert pour oui, rouge pour non, orange pour inconnu)
- **Types de cartes** : Graphiques radar pour des entreprises individuelles, tracés statistiques pour l’analyse comparative
- **Responsive Design** : Optimisation de la mise en page large pour une présentation de type tableau de bord

# Dépendances externes

## Bibliothèques de base
- **streamlit** : Cadre d’application Web pour l’interface utilisateur
- **pandas** : Manipulation et analyse de données
- **numpy** : Opérations de calcul numérique
- plotly.express & plotly.graph_objects : Bibliothèque de visualisation interactive
- **scipy.stats** : Analyse statistique et calculs d’intervalles de confiance

## Bibliothèques de visualisation  
- **plotly.subplots** : Création de graphiques multi-panneaux
- **seaborn** : Visualisation des données statistiques (importées mais l’utilisation n’est pas visible dans le code fourni)

## Source de données
- **Fichier de données CSV** : Stockage local des fichiers à 'attached_assets/data_1757344901533.csv' avec encodage UTF-8-SIG
- **Format de fichier** : Valeurs séparées par des virgules avec contenu en français

## Outils de développement
- **warnings** : Suppression des avertissements Python pour une sortie plus propre lors des calculs statistiques
- **re** : Expressions régulières (importées dans data_analysis module)
