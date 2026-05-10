# Financial Dashboard: Pipeline de Limpeza e Visualização

Este projeto é uma solução completa de **Ciência de Dados** que transforma dados brutos (e "sujos") de vendas em insights estratégicos. A aplicação automatiza o tratamento de outliers, correção de tipagem brasileira e gera um dashboard interativo para tomada de decisão.

---

## Funcionalidades
- **Geração de Dados Sintéticos:** Script para simular cenários reais com erros de tipagem, nulos e outliers absurdos.
- **Pipeline de Limpeza (ETL):** - Conversão de moeda brasileira (vírgula para ponto).
    - Tratamento de valores nulos usando a mediana (evitando distorções).
    - Identificação e tratamento de Outliers via **Método IQR (Interquartile Range)**.
- **Dashboard Interativo:** Visualização de KPIs e tendências mensais usando Streamlit e Plotly.

---

## Tecnologias Utilizadas
- **Python 3.12**
- **Pandas:** Manipulação e limpeza de dados.
- **Numpy:** Cálculos matemáticos e tratamento de anomalias.
- **Plotly:** Gráficos interativos.
- **Streamlit:** Framework para interface web.

---

## Estrutura do Dashboard
1.  **KPIs Financeiros:** Faturamento Bruto, Ticket Médio e Volume de Itens.
2.  **Análise Temporal:** Evolução mensal das vendas para identificação de sazonalidade.
3.  **Ranking de Performance:** Top 5 produtos que mais geram receita.

---

## ⚙️ Como Executar

### 1. Clonar o repositório
```bash
git clone [https://github.com/teu-usuario/projeto-vendas.git](https://github.com/teu-usuario/projeto-vendas.git)
cd projeto-vendas
