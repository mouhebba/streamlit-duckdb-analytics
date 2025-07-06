import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="📊 Walmart Dashboard", layout="wide", page_icon="🛒")
st.title("📊 Analyse des Ventes Walmart")

uploaded_file = st.file_uploader("📁 Téléversez un fichier CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Nettoyage : conversion des colonnes
    df['Weekly_Sales'] = df['Weekly_Sales'].replace({',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    # Connexion à DuckDB
    db_path = Path("data/walmart.duckdb")
    db_path.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(db_path))
    con.execute("DROP TABLE IF EXISTS ventes")
    con.execute("CREATE TABLE ventes AS SELECT * FROM df")

    # Filtres dynamiques
    st.sidebar.header("🔍 Filtres")
    stores = df['Store_Number'].unique()
    selected_stores = st.sidebar.multiselect("Magasins", stores, default=list(stores))

    date_min, date_max = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input("Période", (date_min, date_max))

    holiday_flag = st.sidebar.selectbox("Jour férié ?", options=["Tous", "Oui", "Non"])

    # Requête SQL dynamique
    query = f"""
        SELECT *, Date AS date_clean
        FROM ventes
        WHERE Store_Number IN {tuple(selected_stores)}
        AND date_clean BETWEEN '{date_range[0]}' AND '{date_range[1]}'
    """
    if holiday_flag == "Oui":
        query += " AND Holiday_Flag = 1"
    elif holiday_flag == "Non":
        query += " AND Holiday_Flag = 0"

    filtered_df = con.execute(query).df()

    st.success(f"✅ {len(filtered_df)} lignes après filtrage")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    # Visualisations
    st.markdown("## 📈 Indicateurs Clés")

    col1, col2 = st.columns(2)

    with col1:
        total_sales = filtered_df['Weekly_Sales'].sum()
        st.metric("💰 Ventes totales", f"{total_sales:,.2f} $")

        fig1 = px.bar(filtered_df.groupby('Store_Number', as_index=False)['Weekly_Sales'].sum(),
                      x='Store_Number', y='Weekly_Sales', title="Ventes par magasin")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        filtered_df['Mois'] = filtered_df['date_clean'].dt.to_period('M').astype(str)
        fig2 = px.line(filtered_df.groupby('Mois', as_index=False)['Weekly_Sales'].sum(),
                       x='Mois', y='Weekly_Sales', title="Évolution mensuelle des ventes")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.scatter(filtered_df, x='Temperature', y='Weekly_Sales',
                          size='Fuel_Price', color='Holiday_Flag',
                          title="Température vs Ventes (taille = prix carburant)")
        st.plotly_chart(fig3, use_container_width=True)

    # KPI 4 : Corrélation chômage / ventes
    fig4 = px.scatter(filtered_df, x='Unemployment', y='Weekly_Sales',
                      trendline='ols', title="Chômage vs Ventes")
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("Veuillez téléverser un fichier CSV pour commencer.")
