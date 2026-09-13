# 🏭 Application web — Analyse exploratoire Hygiène des PME

Application **Streamlit** (interface en français) pour l'analyse et la visualisation des pratiques d'hygiène des PME, conçue comme un **tableau de bord d'évaluation** à partir d'une enquête terrain (CSV).

---

## 🇫🇷 Français

### 🎯 Objectif
Évaluer le niveau d'hygiène des PME (BPH, BPF, HACCP, procédures, stockage, contrôle qualité…) via **9 indicateurs**, et les **obstacles** qui freinent leur mise en œuvre — pour guider les démarches d'amélioration.

### 🏗️ Démarche
1. **Chargement maîtrisé des données** — encodage géré (UTF-8-SIG), valeurs « Oui / Non / Inconnu » traitées explicitement.
2. **Statistiques** — descriptives + **intervalles de confiance** pour les proportions.
3. **Analyses croisées** — obstacles (4 catégories), formations & corrélations, comparaison inter-entreprises.
4. **Visualisation** — radar par entreprise, barres, heatmap, boxplot (Plotly, code couleur sémantique vert/rouge/orange).

### 🗂️ Architecture
`app.py` (UI + navigation sidebar) · `data_analysis.py` (`DataAnalyzer`) · `visualization.py` (`HygieneVisualizer`) · données dans `attached_assets/`

### 🛠️ Technologies
Python · Streamlit (`@st.cache_data`) · pandas · numpy · Plotly · scipy

### 📊 Résultats
- Dashboard **bilingue / français** avec navigation par sections.
- **Analyses reproductibles et expliquées** (IC, proportions, scores).
- Code modulaire (analyse / visualisation / UI séparés) — facile à étendre.

---

## 🇬🇧 English

### 🎯 Objective
Assess SME hygiene levels (GHP/GMP, HACCP, procedures, storage, quality control…) across **9 indicators**, and the **barriers** hindering them — to guide improvement programmes.

### 🏗️ Approach
1. **Robust data loading** — managed encoding (UTF-8-SIG), explicit handling of “Yes / No / Unknown”.
2. **Statistics** — descriptive + **confidence intervals** for proportions.
3. **Cross-analyses** — barriers (4 categories), training & correlations, cross-company comparison.
4. **Visualisation** — per-company radar, bars, heatmap, boxplot (Plotly, semantic green/red/orange).

### 🗂️ Architecture
`app.py` (UI + sidebar navigation) · `data_analysis.py` (`DataAnalyzer`) · `visualization.py` (`HygieneVisualizer`) · data in `attached_assets/`

### 🛠️ Tech Stack
Python · Streamlit (`@st.cache_data`) · pandas · numpy · Plotly · scipy

### 📊 Results
- Dashboard with **sidebar-driven navigation**.
- **Reproducible, explained analytics** (CIs, proportions, scores).
- Modular code (analysis / visualisation / UI separated) — easy to extend.

---

### 🚀 Démarrage / Quick start
`pip install -r requirements.txt` → `streamlit run app.py`