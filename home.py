#Importons les librairies necessaire
import streamlit as st
import pandas as pd 
import numpy as np 
from numerize.numerize import numerize
import plotly.express as px
import plotly.subplots as sp

#Configuration de la barre de page 
st.set_page_config(page_title="Kpi analyse financiere", page_icon="📈", layout="wide")  
st.subheader("📈 Analyse de donnees : DAKITSE-BENISSAN KIMYE ")

# Chargement du fichier csv
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Chargement du dataframe 
df=pd.read_csv('data2.csv')




st.sidebar.header("Analyse par filtre")
livraison=st.sidebar.multiselect(
    "Filtre par rapport au statut",
     options=df["Livraison"].unique(),
     default=df["Livraison"].unique(),
)
methode_payer=st.sidebar.multiselect(
    "Filtre par methode",
     options=df["Methode_payer"].unique(),
     default=df["Methode_payer"].unique(),
)
status=st.sidebar.multiselect(
    "Filtre par statut",
     options=df["Status"].unique(),
     default=df["Status"].unique(),
)

df_selection=df.query(
    "Livraison==@livraison & Methode_payer==@methode_payer & Status ==@status"
)
st.subheader('Objectif 1 : Créeons un indicateur qui permettent de connaître la santée financière de entreprise', divider='rainbow')

# TOP KPI's
total_sales = int(df_selection["Prix_total"].sum())
nombe_produit = int(df_selection.Nom_produit.count())
average_sale_by_transaction = round(df_selection["Prix_total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Chiffre d'affaire:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Nombre de produit :")
    st.subheader(f"{nombe_produit} ")
with right_column:
    st.subheader("Vente moyenne par transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

#top analytics
def metrics():
 from streamlit_extras.metric_cards import style_metric_cards
 col1, col2, col3 = st.columns(3)

 col1.metric(label="Nombre de produit total", value=df_selection.Nom_produit.count(), delta="Produit")

 col2.metric(label="Total Chiffe d'affaire", value= f"{df_selection.Prix_total.sum():,.0f}",delta=df.Prix_total.median())

 col3.metric(label="vente moyenne par transaction", value= f"{df_selection.Prix_total.mean():,.0f}",delta="Achat moyen")

 style_metric_cards(background_color="#A7ADBA",border_left_color="#f20045",box_shadow="5px")

 #create divs
div1, div2=st.columns(2)
st.subheader('Objectif 2: Ranger les produits en fonctions de leurs chiffres d’affaires', divider='rainbow')

# SALES BY Product [BAR CHART]
chart_type = st.selectbox('Choisissez un type de graphique 😀', ['Bar', 'Line'],key="unique_key_1")
if chart_type == 'Bar':
    sales_by_hour = df_selection.groupby(by=["Nom_produit"])[["Prix_total"]].sum()
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Prix_total",
        title="<b>Vente par produit</b>",
        color_discrete_sequence=["#A7ADBA"] * len(sales_by_hour),
        template="plotly_white",
        height=400,
        width=1200,
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
elif chart_type == 'Line':
     sales_by_hour = df_selection.groupby(by=["Nom_produit"])[["Prix_total"]].sum()
     fig_hourly_sales = px.line(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Prix_total",
        title="<b>Vente par produit</b>",
        color_discrete_sequence=["#A7ADBA"] * len(sales_by_hour),
        template="plotly_white",
        height=400,
        width=1200,
    )
     fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

st.plotly_chart(fig_hourly_sales, use_container_width=True)


## Créer un dataframe exemple


st.subheader('Objectif 3: Quel est le moyen de paiement le plus utilisé', divider='rainbow')

# SALES BY PAYEMENT[BAR CHART]

sales_by_hours = df_selection.groupby(by=["Methode_payer"])[["Transaction_ID"]].sum()
fig_hourly_sale = px.bar(
    sales_by_hours,
    x=sales_by_hours.index,
    y="Transaction_ID",
    title="<b>Methode la plus utilise </b>",
    color_discrete_sequence=["#A7ADBA"] * len(sales_by_hours),
    template="plotly_white",
)
fig_hourly_sale.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_hourly_sale, use_container_width=True)
st.markdown('''
    Le moyen de paiement le plus utilisé est :red[PayPal] ''')

st.subheader('Objectif 4: Déterminer dans quel pays du monde, les ventes sont plus élevées', divider='rainbow')

chart_types = st.selectbox('Choisissez un type de graphique 😀', ['Bar', 'Line'],key="unique_key_2")
if chart_types == 'Bar':
    sales = df_selection.groupby(by=["Pays"])[["Prix_total"]].sum()
    fig_hourly_sales = px.bar(
        sales,
        x=sales.index,
        y="Prix_total",
        title="<b>Vente par pays</b>",
        color_discrete_sequence=["#65737E"] * len(sales),
        template="plotly_white",
        height=400,
        width=1000,
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
elif chart_types == 'Line':
     sales = df_selection.groupby(by=["Pays"])[["Prix_total"]].sum()
     fig_hourly_sales = px.line(
        sales,
        x=sales.index,
        y="Prix_total",
        title="<b>Vente par produit</b>",
        color_discrete_sequence=["#65737E"] * len(sales),
        template="plotly_white",
        height=400,
        width=1000,
    )
     fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )

st.plotly_chart(fig_hourly_sales, use_container_width=True)
st.markdown('''
    Le pays qui a le plus vendu est le :red[Portugal] ''')

st.subheader('Objectif 5: Afficher la tendance des ventes en fonction du temps', divider='rainbow')
sales_by_hours = df_selection.groupby(by=["date"])[["Prix_total"]].sum()
fig_hourly_sale = px.bar(
    sales_by_hours,
    x=sales_by_hours.index,
    y="Prix_total",
    title="<b>Tendance en fonction de la date </b>",
    color_discrete_sequence=["#A7ADBA"] * len(sales_by_hours),
    template="plotly_white",
)
fig_hourly_sale.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_hourly_sale, use_container_width=True)

sales_by_hours = df_selection.groupby(by=["heure"])[["Prix_total"]].sum()
fig_hourly_sale = px.bar(
    sales_by_hours,
    x=sales_by_hours.index,
    y="Prix_total",
    title="<b>Tendance en fonction de l'heure </b>",
    color_discrete_sequence=["#A7ADBA"] * len(sales_by_hours),
    template="plotly_white",
)
fig_hourly_sale.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

st.plotly_chart(fig_hourly_sale, use_container_width=True)

#mysql table
def table():
  with st.expander("Tabular"):
  #st.dataframe(df_selection,use_container_width=True)
   shwdata = st.multiselect('Filter :', df.columns, default=["Transaction_ID","Nom_client","Nom_produit","Quantite","Prix_unitaire","Prix_total","Transaction_Date","Pays","Ville","Methode_payer","Livraison","Status"])
   st.dataframe(df_selection[shwdata],use_container_width=True)

#option menu
from streamlit_option_menu import option_menu
with st.sidebar:
        selected=option_menu(
        menu_title="Main Menu",
         #menu_title=None,
        options=["Home","Table"],
        icons=["house","book"],
        menu_icon="cast", #option
        default_index=0, #option
        orientation="vertical",



        )


if selected=="Home":
    
   # pie()
   # barchart()
    metrics()

if selected=="Table":
   metrics()
   table()
   st.dataframe(df_selection.describe().T,use_container_width=True)
 

