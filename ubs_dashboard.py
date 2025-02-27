import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar o arquivo atualizado
df = pd.read_csv("ubs_atualizado.csv", sep=";", decimal=',')

# Contar a frequência de UBS por estado
df_freq = df['Nome_UF'].value_counts().reset_index()
df_freq.columns = ['Estado', 'Frequência']

# Criar o dashboard
st.title("Dashboard de Unidades Básicas de Saúde (UBS)")

# Gráfico de barras
grafico = px.bar(df_freq, x='Estado', y='Frequência', 
                 title='Frequência de UBS por Estado', 
                 labels={'Estado': 'Estado', 'Frequência': 'Número de UBS'},
                 text_auto=True)

st.plotly_chart(grafico)

# Gráfico de pizza
grafico_pizza = px.pie(df_freq, names='Estado', values='Frequência', 
                        title='Percentual de UBS por Estado',
                        hole=0.3)

st.plotly_chart(grafico_pizza)

# Histograma
df_municipios = df['Nome_Município'].value_counts().reset_index()
df_municipios.columns = ['Município', 'Quantidade_UBS']

min_ubs = st.slider("Selecione o número mínimo de UBS", 
                     min_value=int(df_municipios['Quantidade_UBS'].min()), 
                     max_value=int(df_municipios['Quantidade_UBS'].max()), 
                     value=int(df_municipios['Quantidade_UBS'].min()))

df_filtrado_municipios = df_municipios[df_municipios['Quantidade_UBS'] >= min_ubs]


grafico_histograma = px.histogram(df_filtrado_municipios, x='Quantidade_UBS', 
                                   title='Histograma da Quantidade de UBS por Município', 
                                   labels={'Quantidade_UBS': 'Número de UBS', 'count': 'Frequência'},
                                   nbins=140)

st.plotly_chart(grafico_histograma)

# Filtro para estados específicos
estados = st.multiselect("Selecione os estados", df_freq['Estado'].unique())
if estados:
    df_filtrado = df[df['Nome_UF'].isin(estados)]
    st.write(df_filtrado)
    df_filtrado = df_filtrado.dropna(subset=['LATITUDE','LONGITUDE'])
    mapa = px.scatter_map(df_filtrado, 
                             lat='LATITUDE', 
                             lon='LONGITUDE', 
                             hover_name='NOME', 
                             hover_data=['Nome_UF', 'Nome_Município'],
                             zoom=5, 
                             height=500,
                             title='Localização das UBS')


    mapa.update_layout(mapbox_style="open-street-map")


    st.plotly_chart(mapa)
else:

    st.subheader("Mapa Interativo das UBS por Estado")

    df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
    mapa = px.scatter_map(df, 
                             lat='LATITUDE', 
                             lon='LONGITUDE', 
                             hover_name='NOME', 
                             hover_data=['Nome_UF', 'Nome_Município'],
                             zoom=3, 
                             height=500,
                             title='Localização das UBS')


    mapa.update_layout(map_style="open-street-map") 

