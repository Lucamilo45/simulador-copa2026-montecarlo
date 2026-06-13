import streamlit as st
import pandas as pd
import numpy as np
import os

# Garantir que a pasta de saídas exista para evitar erros de salvamento
os.makedirs('outputs', exist_ok=True)

# 1. Definição Completa de todos os 12 Grupos (Sorteio Oficial 2026)
grupos_copa = {
    'A': ['México', 'Coreia do Sul', 'África do Sul', 'Tchéquia'],
    'B': ['Canadá', 'Suíça', 'Catar', 'Bósnia e Herzegovina'],
    'C': ['Brasil', 'Marrocos', 'Escócia', 'Haiti'],
    'D': ['Estados Unidos', 'Paraguai', 'Austrália', 'Turquia'],
    'E': ['Alemanha', 'Equador', 'Costa do Marfim', 'Curaçao'],
    'F': ['Países Baixos', 'Japão', 'Tunísia', 'Suécia'],
    'G': ['Bélgica', 'Irã', 'Egito', 'Nova Zelândia'],
    'H': ['Espanha', 'Uruguai', 'Arábia Saudita', 'Cabo Verde'],
    'I': ['França', 'Senegal', 'Noruega', 'Iraque'],
    'J': ['Argentina', 'Áustria', 'Argélia', 'Jordânia'],
    'K': ['Portugal', 'Colômbia', 'Uzbequistão', 'Rep. D. do Congo'],
    'L': ['Inglaterra', 'Croácia', 'Panamá', 'Gana']
}

# 2. Dicionário Completo de Forças Estatísticas das 48 Seleções
forca_base = {
    'Espanha': 2.3, 'Argentina': 2.2, 'França': 2.1, 'Brasil': 2.0, 
    'Inglaterra': 1.9, 'Portugal': 1.8, 'Colômbia': 1.7, 'Alemanha': 1.7, 
    'Marrocos': 1.6, 'Países Baixos': 1.6, 'Bélgica': 1.5, 'Uruguai': 1.5,
    'Croácia': 1.4, 'Equador': 1.4, 'Japão': 1.3, 'Suíça': 1.3, 'México': 1.2,
    'Senegal': 1.1, 'Noruega': 1.1, 'Canadá': 1.1, 'Estados Unidos': 1.0,
    'Turquia': 1.0, 'Coreia do Sul': 0.9, 'Egito': 0.9, 'Paraguai': 0.8,
    'Costa do Marfim': 0.8, 'Suécia': 0.8, 'Tchéquia': 0.7, 'Tunísia': 0.7,
    'Escócia': 0.7, 'Uzbequistão': 0.6, 'Rep. D. do Congo': 0.6, 'África do Sul': 0.5,
    'Bósnia e Herzegovina': 0.5, 'Panamá': 0.4, 'Catar': 0.4, 'Cabo Verde': 0.4,
    'Arábia Saudita': 0.4, 'Iraque': 0.3, 'Haiti': 0.2, 'Curaçao': 0.2, 
    'Nova Zelândia': 0.2, 'Jordânia': 0.1, 'Gana': 0.5
}

todos_times = sorted([time for grupo in grupos_copa.values() for time in grupo])

st.title("🏆 Simulador Copa do Mundo 2026 - Previsões e Monte Carlo")
st.markdown("Interface interativa para análise preditiva baseada em distribuição de Poisson.")

# Seletor para os dois times do confronto
time_a = st.selectbox("Selecione o Time A", todos_times, index=todos_times.index('Brasil'))
time_b = st.selectbox("Selecione o Time B", [t for t in todos_times if t != time_a], index=0)

# Função para previsão de resultado baseado nas forças e distribuição de Poisson
def prever_confronto(time1, time2, forca):
    f1 = forca.get(time1, 1.0)
    f2 = forca.get(time2, 1.0)
    
    # Gerando amostras de gols simulados
    gols_t1 = np.random.poisson(f1 / (f2 + 0.5) + 0.8, 10000)
    gols_t2 = np.random.poisson(f2 / (f1 + 0.5) + 0.6, 10000)
    
    vitorias_t1 = (gols_t1 > gols_t2).mean()
    empates = (gols_t1 == gols_t2).mean()
    vitorias_t2 = (gols_t1 < gols_t2).mean()
    return vitorias_t1, empates, vitorias_t2

if st.button("📊 Mostrar Previsão do Confronto", type="secondary"):
    v_t1, emp, v_t2 = prever_confronto(time_a, time_b, forca_base)
    
    # Layout em colunas para exibir os resultados lado a lado de forma elegante
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Vitória {time_a}", f"{v_t1*100:.1f}%")
    c2.metric("Empate", f"{emp*100:.1f}%")
    c3.metric(f"Vitória {time_b}", f"{v_t2*100:.1f}%")

# Botão para rodar Monte Carlo completo
if st.button("🚀 Rodar Simulação Completa Monte Carlo", type="primary"):
    st.info("Rodando 10.000 simulações completas baseadas nos pesos das forças...")
    
    N = 10000
    contagem = {time: 0 for time in todos_times}
    
    # Somatório e array de probabilidades para o sorteio de Monte Carlo
    pesos = np.array([forca_base.get(t, 1.0) for t in todos_times])
    probabilidades = pesos / pesos.sum()
    
    for _ in range(N):
        vencedor = np.random.choice(todos_times, p=probabilidades)
        contagem[vencedor] += 1
        
    df = pd.DataFrame(list(contagem.items()), columns=['Seleção', 'Título Simulado'])
    df['P(Campeão) %'] = df['Título Simulado'] / N * 100
    df = df.sort_values(by='P(Campeão) %', ascending=False).reset_index(drop=True)
    
    st.subheader("📊 Top 10 Campeões Mais Prováveis")
    st.dataframe(df.head(10), use_container_width=True)
    
    df.to_csv('outputs/previsao_final_monte_carlo.csv', index=False)
    st.success("Simulação concluída com sucesso! Planilha salva em 'outputs/previsao_final_monte_carlo.csv'")

# Exibir os grupos para referência
if st.checkbox("🔍 Mostrar Composição dos Grupos"):
    st.markdown("---")
    for g, times in grupos_copa.items():
        st.markdown(f"**Grupo {g}:** {', '.join(times)}")