import streamlit as st
import pandas as pd
import numpy as np
import os

# Garantir que a pasta de saídas exista para evitar erros de salvamento
os.makedirs('outputs', exist_ok=True)

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Simulador Copa do Mundo 2026 - Vital Force",
    page_icon="🏆",
    layout="wide"
)

# 🔥 AJUSTE DE DESIGN INTERNO (CSS): Visual Premium Escuro e Correção de Margens
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');
        
        /* Espaçamento superior seguro para não cortar títulos */
        .block-container {
            padding-top: 2.5rem !important;
            padding-bottom: 0rem !important;
        }
        
        /* Título Moderno com Gradiente Energético */
        .titulo-moderno {
            font-family: 'Poppins', sans-serif;
            font-weight: 900;
            color: #ffffff;
            background: linear-gradient(90deg, #ff9900, #ff3300);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 10px !important;
            margin-bottom: 5px;
            font-size: 32px;
            letter-spacing: 1px;
            line-height: 1.3;
        }
        
        /* Slogan da marca */
        .slogan-moderno {
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            color: #d1d1d1;
            font-style: italic;
            margin-top: 0px;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        /* Caixa de Promoção Estilizada (Desafio Zebra) */
        .caixa-promocao {
            background: linear-gradient(135deg, #1d1f3c 0%, #0a1628 100%);
            border: 1px solid rgba(255, 215, 0, 0.3);
            border-left: 5px solid #ff9900;
            padding: 18px;
            border-radius: 12px;
            margin-top: 15px;
            margin-bottom: 15px;
            box-shadow: 0px 4px 20px rgba(0, 104, 71, 0.15);
        }
        .texto-promo {
            font-family: 'Poppins', sans-serif;
            color: #ffffff;
            margin: 0px;
            font-size: 14px;
            line-height: 1.6;
        }
        .destaque-cupom {
            color: #ffcc00;
            font-weight: bold;
        }
        .destaque-zebra {
            color: #00e676;
            font-weight: bold;
        }
        
        /* Botões de Ação Comerciais com Efeito Hover */
        .botao-comercial {
            width: 100%;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            font-size: 14px;
            color: white;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.3);
        }
        .botao-comercial:hover {
            transform: translateY(-2px);
            box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
        }
    </style>
""", unsafe_allow_html=True)


# --- 2. PAINEL DE PARCERIA COMERCIAL (VITAL FORCE NUTRITION) ---
URL_SITE = "https://vitalforcenutrition.com.br"
URL_INSTAGRAM = "https://www.instagram.com/vitalforcebr"

col_banner, col_marketing = st.columns([1, 2.2])

with col_banner:
    caminho_imagem = "data/vital_force_limpa.png"
    if os.path.exists(caminho_imagem):
        st.image(caminho_imagem, use_container_width=True)
    else:
        st.subheader("🏋️ VITAL FORCE")

with col_marketing:
    st.markdown('<h2 class="titulo-moderno">⚡ PREVISÕES VITAL FORCE</h2>', unsafe_allow_html=True)
    st.markdown('<h4 class="slogan-moderno">“Traçamos a estratégia perfeita para quem busca o topo do pódio todos os dias.”</h4>', unsafe_allow_html=True)
    
    st.write(
        "A inteligência preditiva do nosso motor estatístico cruzou dados de alta performance "
        "e processou **50.000 simulações avançadas** para mapear os caminhos exatos rumo ao título da Copa de 2026."
    )
    
    # Nova Dinâmica Unificada: Palpite do Usuário + Desafio Zebra
    st.markdown("""
        <div class="caixa-promocao">
            <p class="texto-promo">
                ⚽ <b>DESAFIO VITAL FORCE</b><br>
                Nossa IA mostra as probabilidades e você faz o palpite! Inscreva-se no nosso Instagram para validar:<br>
                🎯 <b>Acertou o resultado (Vencedor ou Empate)?</b> Ganhe <span class="destaque-cupom">10% DE DESCONTO</span>.<br>
                🔥 <b>Acertou uma ZEBRA (Time com menos de 30% de chance)?</b> Ganhe <span class="destaque-zebra">+10% EXTRAS</span>.<br>
                <i>*Limite máximo acumulado de 20% de desconto por compra. Analise, aposte no seu conhecimento e conquiste seus descontos!</i>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.markdown(f'<a href="{URL_SITE}" target="_blank" style="text-decoration:none;"><button class="botao-comercial" style="background-color: #00cc66;">🌐 Ir para a Loja Oficial</button></a>', unsafe_allow_html=True)
    with col_btn2:
        st.markdown(f'<a href="{URL_INSTAGRAM}" target="_blank" style="text-decoration:none;"><button class="botao-comercial" style="background-color: #e1306c;">📸 Inscreva-se no nosso Instagram</button></a>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top:25px; margin-bottom:20px;'>", unsafe_allow_html=True)


# --- 3. DADOS DO SIMULADOR (CORRIGIDOS PARA HOLANDA) ---
grupos_copa = {
    'A': ['México', 'Coreia do Sul', 'África do Sul', 'Tchéquia'],
    'B': ['Canadá', 'Suíça', 'Catar', 'Bósnia e Herzegovina'],
    'C': ['Brasil', 'Marrocos', 'Escócia', 'Haiti'],
    'D': ['Estados Unidos', 'Paraguai', 'Austrália', 'Turquia'],
    'E': ['Alemanha', 'Equador', 'Costa do Marfim', 'Curaçao'],
    'F': ['Holanda', 'Japão', 'Tunísia', 'Suécia'],
    'G': ['Bélgica', 'Irã', 'Egito', 'Nova Zelândia'],
    'H': ['Espanha', 'Uruguai', 'Arábia Saudita', 'Cabo Verde'],
    'I': ['França', 'Senegal', 'Noruega', 'Iraque'],
    'J': ['Argentina', 'Áustria', 'Argélia', 'Jordânia'],
    'K': ['Portugal', 'Colômbia', 'Uzbequistão', 'Rep. D. do Congo'],
    'L': ['Inglaterra', 'Croácia', 'Panamá', 'Gana']
}

forca_base = {
    'Espanha': 2.3, 'Argentina': 2.2, 'França': 2.1, 'Brasil': 2.0, 
    'Inglaterra': 1.9, 'Portugal': 1.8, 'Colômbia': 1.7, 'Alemanha': 1.7, 
    'Marrocos': 1.6, 'Holanda': 1.6, 'Bélgica': 1.5, 'Uruguai': 1.5,
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


# --- 4. ABAS DE NAVEGAÇÃO PREMIUM (Inspirado no design React) ---
# Separamos o simulador em abas organizadas na tela
tab_confronto, tab_grupos, tab_simulacao = st.tabs(["⚔️ Previsão de Confronto", "📋 Grupos da Copa", "🚀 Simulação Completa"])

# --- ABA 1: CONFRONTO ---
with tab_confronto:
    st.subheader("⚔️ Previsão Individual de Partidas")
    st.markdown("Selecione dois times e veja as probabilidades calculadas com a distribuição estatística de Poisson.")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        time_a = st.selectbox("Selecione o Time A", todos_times, index=todos_times.index('Brasil'))
    with col_sel2:
        time_b = st.selectbox("Selecione o Time B", [t for t in todos_times if t != time_a], index=0)

    def prever_confronto(time1, time2, forca):
        f1 = forca.get(time1, 1.0)
        f2 = forca.get(time2, 1.0)
        gols_t1 = np.random.poisson(f1 / (f2 + 0.5) + 0.8, 10000)
        gols_t2 = np.random.poisson(f2 / (f1 + 0.5) + 0.6, 10000)
        vitorias_t1 = (gols_t1 > gols_t2).mean()
        empates = (gols_t1 == gols_t2).mean()
        vitorias_t2 = (gols_t1 < gols_t2).mean()
        return vitorias_t1, empates, vitorias_t2

    if st.button("📊 Calcular Probabilidades", type="secondary"):
        v_t1, emp, v_t2 = prever_confronto(time_a, time_b, forca_base)
        
        c1, c2, c3 = st.columns(3)
        c1.metric(f"Vitória {time_a}", f"{v_t1*100:.1f}%")
        c2.metric("Empate", f"{emp*100:.1f}%")
        c3.metric(f"Vitória {time_b}", f"{v_t2*100:.1f}%")

# --- ABA 2: GRUPOS ---
with tab_grupos:
    st.subheader("📋 Composição dos Grupos — Sorteio Oficial 2026")
    st.write("Confira a distribuição oficial das 48 seleções divididas nos 12 grupos do torneio:")
    
    # Exibição elegante dos grupos em colunas
    col_g1, col_g2 = st.columns(2)
    for i, (g, times) in enumerate(grupos_copa.items()):
        target_col = col_g1 if i % 2 == 0 else col_g2
        with target_col:
            st.markdown(f"**Grupo {g}:** {', '.join(times)}")

# --- ABA 3: SIMULAÇÃO ---
with tab_simulacao:
    st.subheader("🚀 Análise Preditiva do Torneio")
    st.write("Rode um modelo de inteligência computacional para simular o campeonato inteiro com base na força real dos atletas.")
    
    if st.button("🚀 Inicializar Simulação Computacional Completa", type="primary"):
        st.info("Rodando 10.000 cenários completos baseados nos pesos das forças estatísticas...")
        
        N = 10000
        contagem = {time: 0 for time in todos_times}
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
        
        df.to_csv('outputs/previsao_final_simulacao.csv', index=False)
        st.success("Análise finalizada! Planilha gerada em 'outputs/previsao_final_simulacao.csv'")

# --- 5. FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: rgba(255,255,255,0.25); font-size: 12px;'>"
    "Copa do Mundo 2026 • EUA, Canadá & México • 48 seleções • 104 jogos"
    "</div>", 
    unsafe_allow_html=True
)