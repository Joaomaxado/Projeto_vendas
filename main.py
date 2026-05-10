# Dataframe cobaia

import pandas as pd
import numpy as np
import random


def criar_dados_sujos(n_linhas=100):
    np.random.seed(42)  # Garante que os números "aleatórios" sejam sempre os mesmos para teste

    data = {
        # Coluna com nomes de colunas variados
        'Data_Venda': [f"{random.randint(1, 28)}/0{random.randint(1, 9)}/2026" for _ in range(n_linhas)],
        'Item_Comercializado': [random.choice(['Mouse', 'Teclado', 'Monitor', 'Cabo HDMI', None]) for _ in
                                range(n_linhas)],
        'Preco_Unit': np.random.uniform(50, 500, n_linhas),
        'Qtd_Vendida': np.random.randint(1, 15, n_linhas)
    }

    df = pd.DataFrame(data)

    # Inserindo SUJEIRA propositalmente:

    # 1. Valores Nulos (NaN)
    df.loc[df.sample(frac=0.1).index, 'Preco_Unit'] = np.nan

    # 2. Outliers Absurdos (Preços impossíveis)
    df.loc[df.sample(n=5).index, 'Preco_Unit'] = [15000, 25000, -500, 99999, 12000]

    # Salva o arquivo
    df.to_csv('dados_empresa_sujos.csv', index=False)
    print("✅ Arquivo 'dados_empresa_sujos.csv' criado com sucesso!")


if __name__ == "__main__":
    criar_dados_sujos()

import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title='Dashboard Financeiro', layout='wide')

@st.cache_data
def carregar_e_limpar():
    df = pd.read_csv('dados_empresa_sujos.csv')
    df['Faturamento_linha'] = df['Preco_Unit'] * df['Qtd_Vendida']

    # Tratamento de tipagem
    df['Qtd_Vendida'] = df['Qtd_Vendida'].fillna(0)
    df['Preco_Unit'] = df['Preco_Unit'].astype(str).str.replace(',', '.', regex=False)
    df['Preco_Unit'] = pd.to_numeric(df['Preco_Unit'], errors='coerce')
    df['Preco_Unit'] = df['Preco_Unit'].fillna(df['Preco_Unit'].median())
    df['Qtd_Vendida'] = pd.to_numeric(df['Qtd_Vendida'], errors='coerce')
    df['Data_Venda'] = pd.to_datetime(df['Data_Venda'], format='%d/%m/%Y')
    df['Item_Comercializado'] = df['Item_Comercializado'].replace('NaN', None)

    # Engenharia de dados
    df['Mes'] = df['Data_Venda'].dt.month
    df['Ano'] = df['Data_Venda'].dt.year
    monthly_revenue = df.groupby('Mes')['Qtd_Vendida'].sum().reset_index()
    df.groupby(['Ano', 'Mes'])['Qtd_Vendida'].sum()

    # Tratamento de outliers
    q1 = df['Preco_Unit'].quantile(.25)
    q3 = df['Preco_Unit'].quantile(.75)

    iqr = q3 - q1

    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr

    # Capping
    df['Preco_Unit'] = np.where(df['Preco_Unit'] < limite_inferior, limite_inferior, df['Preco_Unit'])
    df['Preco_Unit'] = np.where(df['Preco_Unit'] > limite_superior, limite_superior, df['Preco_Unit'])

    return df
# Interface com KPI's
df = carregar_e_limpar()

st.title('Painel de controle financeiro')

col1, col2, col3 = st.columns(3)

total_revenue = (df['Preco_Unit'] * df['Qtd_Vendida']).sum()
mean_ticket = df['Preco_Unit'].mean()
total_itens = df['Qtd_Vendida'].sum()

with col1:
    st.metric(label='Faturamento bruto', value=f'R$ {total_revenue:.2f}')

with col2:
    st.metric(label='Ticket Medio', value=f'R$ {mean_ticket:.2f}')

with col3:
    st.metric(label='Volume de Itens', value=f'R$ {total_itens:.2f}')

# Visualização
st.markdown('---')
st.subheader('Evolução Mensal do Faturamento')

# Gráfico
monthly_revenue = df.groupby('Mes')['Faturamento_linha'].sum().reset_index()
fig = px.line(monthly_revenue, x='Mes', y='Faturamento_linha',
              title='Faturamento Mensal', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Top 5 produtos
st.subheader('Top 5 Produtos por Faturamento')
top_produtos = df.groupby('Item_Comercializado')['Faturamento_linha'].sum().reset_index()
top_produtos = top_produtos.sort_values(by='Faturamento_linha', ascending=False).head(5)

fig_barras = px.bar(top_produtos, x='Faturamento_linha', y='Item_Comercializado',
                    orientation='h', color='Faturamento_linha',
                    color_continuous_scale='Greens')
st.plotly_chart(fig_barras, use_container_width=True)