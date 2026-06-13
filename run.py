import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from penaltyblog.models import DixonColesGoalModel

print("====== 🤖 INICIANDO MOTOR DE MONTE CARLO - COPA 2026 ======")

# 1. Criação das pastas de ambiente se não existirem
os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# 2. Definição Oficial dos 12 Grupos extraídos do seu documento
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

# 3. Simulação Estatística das Forças (Dixon-Coles simplificado baseado no Elo e Histórico)
# Mapeamento do Rating de Força Médio das Equipes para a distribuição de Poisson
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
    'Arábia Saudita': 0.4, 'Iraque': 0.3, 'África do Sul': 0.3, 'Haiti': 0.2,
    'Curaçao': 0.2, 'Nova Zelândia': 0.2, 'Jordânia': 0.1, 'Gana': 0.5
}

# Definição das configurações de Monte Carlo
N_SIMULACOES = 50000
contagem_campeao = {time: 0 for grupo in grupos_copa.values() for time in grupo}

print(f"Calculando probabilidades avançadas sobre {N_SIMULACOES} linhas de tempo...")

# 4. Loop de Monte Carlo
for sim in range(N_SIMULACOES):
    classificados_mata_mata = []
    
    # --- Fase de Grupos ---
    for grupo, selecoes in grupos_copa.items():
        pontos = {time: 0 for time in selecoes}
        
        # Simular confrontos internos do grupo
        for i in range(len(selecoes)):
            for j in range(i+1, len(selecoes)):
                t1, t2 = selecoes[i], selecoes[j]
                f1, f2 = forca_base.get(t1, 0.5), forca_base.get(t2, 0.5)
                
                # Sorteio de Gols por Poisson baseado na força Dixon-Coles
                gols_t1 = np.random.poisson(f1 / (f2 + 0.5) + 0.8)
                gols_t2 = np.random.poisson(f2 / (f1 + 0.5) + 0.6)
                
                if gols_t1 > gols_t2:
                    pontos[t1] += 3
                elif gols_t2 > gols_t1:
                    pontos[t2] += 3
                else:
                    pontos[t1] += 1
                    pontos[t2] += 1
                    
        # Ordenar os melhores do grupo
        ranking_grupo = sorted(pontos.items(), key=lambda x: x[1], reverse=True)
        classificados_mata_mata.append(ranking_grupo[0][0]) # 1º Lugar
        classificados_mata_mata.append(ranking_grupo[1][0]) # 2º Lugar

    # --- Estrutura do Mata-Mata (Cenário de Afunilamento Direto) ---
    # Para simplificar o chaveamento das 24 seleções classificadas diretamente até a Final
    sobreviventes = classificados_mata_mata[:16] # Afunilando o Top 16 das chaves principais
    
    while len(sobreviventes) > 1:
        proxima_fase = []
        for i in range(0, len(sobreviventes), 2):
            if i+1 < len(sobreviventes):
                t1, t2 = sobreviventes[i], sobreviventes[i+1]
                f1, f2 = forca_base.get(t1, 0.5), forca_base.get(t2, 0.5)
                
                # No mata-mata não há empate
                prob_t1 = f1 / (f1 + f2)
                if np.random.random() < prob_t1:
                    proxima_fase.append(t1)
                else:
                    proxima_fase.append(t2)
            else:
                proxima_fase.append(sobreviventes[i])
        sobreviventes = proxima_fase
        
    # Contabiliza o campeão da simulação atual
    campeao_final = sobreviventes[0]
    contagem_campeao[campeao_final] += 1

# 5. Consolidação e salvamento das planilhas de Previsão
df_final = pd.DataFrame(list(contagem_campeao.items()), columns=['Seleção', 'Títulos Simulado'])
df_final['P(Campeão) %'] = (df_final['Títulos Simulado'] / N_SIMULACOES) * 100
df_final = df_final.sort_values(by='P(Campeão) %', ascending=False).reset_index(drop=True)

# Salva na pasta de outputs
df_final.to_csv('outputs/previsao_final_monte_carlo.csv', index=False)

print("\n==================================================")
print("🏆 PREVISÃO FINAL DO TOP 10 CAMPEÕES (MONTE CARLO)")
print("==================================================")
print(df_final.head(10).to_string(index=False))
print("==================================================")
print("💾 Processamento concluído! Dados guardados em 'outputs/previsao_final_monte_carlo.csv'")