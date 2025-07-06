# streamlit-duckdb-analytics
# 📊 Walmart Sales Dashboard – Projet MBA ESG

## 🎯 Objectif du Projet

Ce projet consiste à créer une **application web interactive avec Streamlit** qui permet :

- 📁 de téléverser un fichier CSV contenant des données de ventes Walmart,
- 🗃️ de stocker ces données dans une base **DuckDB locale**,
- 📈 de visualiser **quatre indicateurs clés de performance (KPI)** via des graphes interactifs,
- 🎛️ de filtrer dynamiquement les résultats par **magasin, période, et jours fériés**.

---

## 👥 Équipe 2 Projet : "Walmart Data Analyst"

| Membre               | Rôle                                  |
|--------------------- |---------------------------------------|
| Lyna Meryem Hamadou  | Just a Girl Team member               |       
| Salma Echalih        | Funny Team member                     |
| Mouheb Ben Abdallah  |  Super Team member                    |

PS : Ce travail était le fruit de contribution collaborative de tous les membres de l'équipe 
---

## 📦 Fonctionnalités de l'application

- Interface simple pour **téléverser un fichier CSV** (ex. `Walmart_sales_analysis.csv`)
- Stockage et interrogation via **DuckDB**
- **Filtres dynamiques** disponibles :
  - Par numéro de **magasin**
  - Par **plage de dates**
  - Par présence de **jours fériés**
- Visualisation de **4 KPI** :
  1. Ventes totales par magasin
  2. Évolution mensuelle des ventes
  3. Température vs ventes (taille = prix du carburant)
  4. Taux de chômage vs ventes (`trendline='ols'`)

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/streamlit-duckdb-walmart.git
cd streamlit-duckdb-walmart


### 2. Créer et activer l'environnement virtuel
``` bash
python -m venv .venv
.venv\Scripts\activate

### 3. Installer les dépendances
``` bash
pip install -r requirements.txt

### 4.🚀 Lancer l'application
``` bash
streamlit run main.py


