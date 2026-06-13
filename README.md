# Previsão do Campeão da Copa do Mundo 2026 🏆

Projeto estatístico que estima a força de cada uma das 48 seleções a partir de
dados históricos reais, prevê o resultado de **cada jogo** e simula o torneio
inteiro milhares de vezes (Monte Carlo) para chegar ao **provável campeão**.

A previsão final é escrita em [jogos.md](jogos.md). As probabilidades completas
ficam em [outputs/](outputs/).

## Resultado (execução atual)

Favoritos ao título (Monte Carlo, 50.000 simulações; sorteio oficial de 2026):

| # | Seleção | P(Campeão) | P(Final) |
|---|---------|-----------|----------|
| 1 | Espanha | 15.9% | 25.1% |
| 2 | Argentina | 14.5% | 23.3% |
| 3 | França | 10.6% | 18.4% |
| 4 | Brasil | 9.4% | 16.8% |
| 5 | Inglaterra | 8.3% | 15.3% |
| 6 | Portugal | 6.7% | 13.2% |

> A "Previsão Final" (pódio) em jogos.md mostra um **cenário coerente** em que o
> favorito avança em cada confronto. Por causa do chaveamento, esse cenário pode
> diferir do favorito marginal. **As probabilidades no topo são o resultado
> robusto**; o bracket único é ilustrativo.

## Como funciona

1. **Dados** — `results.csv` do projeto [martj42/international_results](https://github.com/martj42/international_results)
   (~49 mil partidas internacionais de 1872 a 2026), baixado e cacheado em `data/`.
2. **Modelo de gols (Dixon-Coles)** — via [`penaltyblog`](https://github.com/martineastwood/penaltyblog).
   Cada seleção ganha parâmetros de ataque/defesa; há correção Dixon-Coles para
   placares baixos, **decaimento temporal** (jogos recentes pesam mais) e **peso
   por importância** do jogo (Copa > eliminatórias > amistosos).
3. **Rating Elo** — calculado sobre o mesmo histórico (`penaltyblog.ratings.Elo`).
4. **Ensemble DC + Elo** — a supremacia de gols mistura Dixon-Coles e Elo
   (`ENSEMBLE_W`), gerando os gols esperados de cada lado.
5. **Vantagem de casa** — bônus aplicado a EUA, Canadá e México (anfitriões).
6. **Partida → placar** — Poisson bivariado com correção Dixon-Coles; no
   mata-mata, empate nos 90' vai para prorrogação e pênaltis.
7. **Monte Carlo** — 50 mil torneios completos seguindo a **estrutura oficial
   FIFA 2026** (jogos 73–104), incluindo a alocação dos 8 melhores terceiros
   (regra do Anexo C). Agrega P(classificar), P(cada fase) e P(título) por seleção.

## Como rodar

```bash
python -m pip install -r requirements.txt     # instala penaltyblog etc. (Python 3.11)
python run.py                                  # ajusta, simula e reescreve jogos.md
python run.py --fast                           # reusa o modelo em cache (rápido)
python run.py --sims 100000                    # mais simulações
python -m src.backtest                         # validação em 2018 e 2022
python -m src.names                            # confere o mapeamento das 48 seleções
```

> No Windows, `pip`/`py` podem apontar para outra versão do Python. Use sempre
> `python -m pip ...` para instalar no mesmo interpretador do `python`.

## Validação (backtest sem vazamento de dados)

Treinando só com dados anteriores a cada Copa e prevendo a fase de grupos
(ver [outputs/calibration.md](outputs/calibration.md)):

| Copa | log-loss modelo | log-loss baseline | ganho | campeão real (P prevista / ranking) |
|------|-----------------|-------------------|-------|--------------------------------------|
| 2018 | 0.929 | 1.033 | **+10%** | França — 6.4% (5º favorito) |
| 2022 | 1.072 | 1.059 | −1% | Argentina — 11.5% (3º favorito) |

A Copa de 2022 teve muitas zebras na fase de grupos (Arábia 1–0 Argentina,
Japão batendo Alemanha e Espanha), o que derruba a previsibilidade — daí o
ganho ~0. Em ambas as edições o campeão real recebeu probabilidade alta e
ficou entre os favoritos. O *reliability diagram* fica em `outputs/figs/`.

A varredura indicou `ENSEMBLE_W = 1.0` (Dixon-Coles puro) com o menor log-loss,
mas `0.8` é praticamente idêntico; mantivemos **0.8** para preservar o Elo como
estabilizador do ensemble (custo de calibração desprezível).

## Estrutura

```
run.py                    # pipeline completo
src/config.py             # todos os parâmetros ajustáveis
src/data_loader.py        # carga + pesos (tempo x importância)
src/names.py              # 48 seleções e mapeamento PT-BR <-> dataset
src/model.py              # Dixon-Coles + Elo + ensemble + tabelas vetorizadas
src/match.py              # grid de placar, prorrogação e pênaltis
src/tournament.py         # primitivas vetorizadas (grupos, partidas)
src/simulate.py           # Monte Carlo da Copa 2026
src/backtest.py           # validação 2018/2022 + tuning
src/report.py             # gera saídas e reescreve jogos.md
src/brackets/wc2026.py    # estrutura oficial + alocação dos terceiros
src/brackets/legacy.py    # grupos/chaveamento 2018 e 2022 (backtest)
data/teams_2026.yaml      # as 48 seleções (sorteio oficial, 12 grupos)
data/third_place_allocation.csv  # tabela de alocação dos terceiros (Anexo C)
```

## Limitações e escolhas de modelagem

- **Placares por jogo** são o *placar modal* (mais provável individualmente),
  que tende a ser baixo (0-0, 1-0). A **classificação prevista** de cada grupo
  usa pontos esperados (mais robusto), então pode não bater ao somar os placares
  modais — é esperado.
- **Alocação dos terceiros**: implementamos as restrições oficiais do Anexo C
  (subconjuntos de grupos por confronto, sem reedição). Como há múltiplas
  alocações válidas por combinação, escolhemos uma de forma determinística; o
  efeito na probabilidade de título é desprezível. A tabela completa está em
  `data/third_place_allocation.csv` e pode ser trocada pela linha exata da FIFA.
- **Campo neutro**: a Copa é em campo neutro; a vantagem de casa só vale para os
  anfitriões. O Dixon-Coles é ajustado com mando global e aplicado só aos sedes.
- **Artilheiro** não é modelado (exigiria dados de jogadores).
- **Grupos e jogos** são o **sorteio oficial de 2026** (5 dez 2025), reconstruído
  dos confrontos reais no dataset e conferido com a fonte oficial (as 12 letras
  batem). O calendário exibido é o real (datas do dataset).

## Ajustes rápidos (`src/config.py`)

`N_SIMS` (simulações) · `TIME_DECAY_HALFLIFE_YEARS` (meia-vida do decaimento) ·
`ENSEMBLE_W` (peso DC × Elo) · `HOST_ADV_FACTOR` (vantagem dos anfitriões) ·
`IMPORTANCE_WEIGHTS` (peso por torneio) · `SEED` (reprodutibilidade).
