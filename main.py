import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
from pathlib import Path

# 🎨 Configuration Streamlit
st.set_page_config(page_title="📊 Walmart Dashboard", layout="wide", page_icon="🛒")
st.markdown(
    "<h1 style='text-align: center; color: #2C3E50;'>📊 Tableau de Bord des Ventes Walmart</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:1px solid #bbb;'>", unsafe_allow_html=True)

# 📂 Téléversement
uploaded_file = st.file_uploader("📥 Veuillez téléverser votre fichier CSV de ventes :", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 🧹 Nettoyage
    df['Weekly_Sales'] = df['Weekly_Sales'].replace({',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

    # 🔗 Connexion DuckDB
    db_path = Path("data/walmart.duckdb")
    db_path.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(db_path))
    con.execute("DROP TABLE IF EXISTS ventes")
    con.execute("CREATE TABLE ventes AS SELECT * FROM df")

    # 🎛️ Filtres
    st.sidebar.markdown("## 🎚️ Filtres")
    stores = df['Store_Number'].unique()
    selected_stores = st.sidebar.multiselect("🏬 Magasins", stores, default=list(stores))

    date_min, date_max = df['Date'].min(), df['Date'].max()
    date_range = st.sidebar.date_input("📆 Plage de dates", (date_min, date_max))

    holiday_flag = st.sidebar.selectbox("🎉 Inclure les semaines fériées ?", ["Tous", "Oui", "Non"])

    # 🔎 Requête filtrée
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

    st.success(f"✅ {len(filtered_df)} lignes sélectionnées après filtrage")

    # 🧮 Résumé général en carte KPI
    st.markdown("### 🧾 Résumé des performances")
    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("💰 Ventes totales", f"{filtered_df['Weekly_Sales'].sum():,.2f} $")
    with colB:
        st.metric("📊 Moyenne hebdomadaire", f"{filtered_df['Weekly_Sales'].mean():,.2f} $")
    with colC:
        top_store = filtered_df.groupby('Store_Number')['Weekly_Sales'].sum().idxmax()
        st.metric("🏆 Meilleur magasin", f"Store {top_store}")

    # 🖥️ Tableau des 10 premières lignes
    st.markdown("### 📄 Aperçu des données")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    # 📈 VISUALISATIONS
    st.markdown("## 📊 Visualisations interactives")
    st.markdown("---")

    # ➤ Graph 1 : Ventes par magasin
    fig1 = px.bar(
        filtered_df.groupby('Store_Number', as_index=False)['Weekly_Sales'].sum(),
        x='Store_Number', y='Weekly_Sales',
        title="🏪 Ventes totales par magasin",
        color='Store_Number',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig1.update_layout(title_x=0.3, plot_bgcolor='#F9F9F9', paper_bgcolor='black')
    st.plotly_chart(fig1, use_container_width=True)

    # ➤ Graph 2 : Évolution mensuelle
    filtered_df['Mois'] = filtered_df['date_clean'].dt.to_period('M').astype(str)
    fig2 = px.area(
        filtered_df.groupby('Mois', as_index=False)['Weekly_Sales'].sum(),
        x='Mois', y='Weekly_Sales',
        title="📅 Évolution mensuelle des ventes",
        color_discrete_sequence=["#5B84B1"]
    )
    fig2.update_traces(mode='lines+markers', line=dict(width=2))
    fig2.update_layout(
    title_x=0.3,
    plot_bgcolor='white',
    paper_bgcolor='black',
    xaxis=dict(
        linecolor='black',
        linewidth=1,
        mirror=True,
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    yaxis=dict(
        linecolor='black',
        linewidth=1,
        mirror=True,
        showgrid=True,
        gridcolor='#e0e0e0'
    ),
    margin=dict(l=50, r=50, t=60, b=50)
)

    st.plotly_chart(fig2, use_container_width=True)

    # ➤ Graph 3 : Température vs ventes
    st.markdown("### 🌡️ Température vs Ventes hebdomadaires")
    fig3 = px.scatter(
        filtered_df, x='Temperature', y='Weekly_Sales',
        size='Fuel_Price', color='Holiday_Flag',
        hover_data=['Store_Number'],
        title="🔥 Impact de la température et du carburant sur les ventes",
        color_continuous_scale='sunset'
    )

    fig3.update_layout(
        title_x=0.3,
        plot_bgcolor='#F9F9F9',
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ➤ Graph 4 : Chômage vs ventes
    st.markdown("### 📉 Taux de chômage vs Ventes")
    fig4 = px.scatter(
        filtered_df, x='Unemployment', y='Weekly_Sales',
        trendline='ols', color='Store_Number',
        title="📊 Corrélation chômage et ventes",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig4.update_layout(
        title_x=0.3,
        plot_bgcolor='#F9F9F9',
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("📁 Veuillez téléverser un fichier CSV pour commencer.")
