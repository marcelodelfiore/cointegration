# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 10:23:27 2016

@author: Marcelo Del Fiore
"""

import numpy as np
from model.CalculoResiduos import CalculoResiduos
from model.CointegrationParResultados import CointegrationParResultados
from model.CointegrationResiduosPar import CointegrationResiduosPar
from model.CointrationParCriterios import CointegrationParCriterios
from model.CointegrationPairHistory import CointegrationPairHistory
from service.ServiceQuotes import ServiceQuotes
import statsmodels.api as sm
from scipy import stats
import pandas


def test_ADF_sf(residuos_adf, x, y):

    # cálculo da variação dos resíduos
    delta_residuos_ = []
    for i in range(len(residuos_adf) - 1):
        delta_residuos_.append(residuos_adf[i] - residuos_adf[i + 1])

    delta_residuos = np.asarray(delta_residuos_)

        # remove o primeiro elemento do vetor de resíduos para compatibilizar os tamanhos dos vetores
    residuos_adf = np.delete(residuos_adf, 0)

    # faz a regressão entre os "delta_residuos" (em Y) e "resíduos" (em X), e considera que o valor do intercepto, ou
    # alfa (coeficiente linear) é nulo, ou seja, ajuste o modelo somente com coeficiente angular, beta.
    model = sm.OLS(delta_residuos, residuos_adf)

    fit = model.fit()

    beta_ratio = fit.params[0]

    erro_padrao_ratio = np.sqrt(fit.mse_resid)

    # calcula o delta preco para fazer a regressão que vai determinar o alfa para calcular a estattística
    delta_preco = y - x
    # remove o primeiro elemento do vetor de resíduos para compatibilizar os tamanhos dos vetores
    delta_preco = np.delete(delta_preco, 0)

    X = sm.add_constant(delta_preco)
    model = sm.OLS(delta_residuos, X)
    fit = model.fit()

    alfa_intercep = fit.params[0]

    media_residuos_adf = np.mean(residuos_adf)
    desvio = []

    for i in range(len(residuos_adf)):
        desvio.append(residuos_adf[i] - media_residuos_adf)

    desvio_2 = np.power(desvio, 2)
    devsq = np.sqrt(np.sum(desvio_2))

    estatistica1 = erro_padrao_ratio / devsq
    estatistica = beta_ratio / estatistica1

    # cálculo da meia vida
    alfa_H = -alfa_intercep / beta_ratio
    beta_H = -np.log(1 + beta_ratio)
    meia_vida = 2.0 / beta_H

    return meia_vida, estatistica


def testa_coin_simples(ativo_dep, ativo_indep, periodo, data_inicial):

    per_teste = int(periodo) + 1

    data = []

    # Busca Dados dos ativos
    dados_ativo1 = ServiceQuotes.get_quotes(ativo_dep, data_inicial)
    dados_ativo2 = ServiceQuotes.get_quotes(ativo_indep, data_inicial)

    # caso nao tenha dados para o periodo, retorna None
    if len(dados_ativo1) < periodo or len(dados_ativo2) < periodo:
        return None

    ativo1_fech = dados_ativo1[0:per_teste - 1, [1]]
    ativo2_fech = dados_ativo2[0:per_teste - 1, [1]]

    # TODO fazer a consistÊncia dos dados utilizados:
    # 1. ambos os ativos tem que usar a mesma quantidade de dias
    # 2. os dias devem ser os mesmos

    # acerta o tipo
    # no eixo X vai a variável INDEPENDENTE
    x = ativo2_fech.astype(float)
    ativo2_fech_hoje = x[0][0]

    # no eixo Y vai a variável DEPENDENTE
    y = ativo1_fech.astype(float)
    ativo1_fech_hoje = y[0][0]

    # formata a data para mostrar os gráficos
    for i in range(per_teste - 1):
        data.append(dados_ativo1[i][0][0:9])

    ###################################################################################
    ###################################################################################
    # rotina de regressão linear entre os dados dos dois ativos selecionados e do tempo
    ###################################################################################
    ###################################################################################

    # vetor de tempo
    tempo = range(periodo, 0, -1)

    A = np.vstack([x.T, tempo, np.ones_like(x.T)]).T

    model = sm.OLS(y, A)
    fit = model.fit()

    # parâmetros de saída da regressão
    params = fit.params

    beta_ativo2_    = params[0]
    beta_tempo_     = params[1]
    alfa_           = params[2]

    # erros padrão da regressão calculada
    erro_padrao = fit.bse

    erro_padrao_beta_ativo2 = erro_padrao[0]
    erro_padrao_beta_tempo  = erro_padrao[1]
    erro_padrao_beta_alfa   = erro_padrao[2]

    # estatística da regressão
    valor_t = beta_tempo_ / erro_padrao_beta_tempo
    valor_critico = stats.t.ppf(0.99, periodo - 3)

    # e com a estatística da regressão, escolho os valores críticos
    if (valor_critico > np.absolute(valor_t)):
        crit_99 = -3.58
        crit_95 = -3.67
        crit_90 = -3.28
    else:
        crit_99 = -4.32
        crit_95 = -3.67
        crit_90 = -3.28

    tempo_ = range(0, periodo)

    y_teorico = []
    for i in tempo_:
        y_teorico.append(beta_ativo2_ * x[i] + beta_tempo_ * tempo[i] + alfa_)

    beta_ativo2 = (np.round(beta_ativo2_, 4))
    beta_tempo  = (np.round(beta_tempo_, 4))
    alfa        = (np.round(alfa_, 4))

    # e os resíduos
    residuos = y - y_teorico
    residuos_pd = pandas.DataFrame(residuos)
    residuos_adf = np.reshape(residuos, len(residuos))

    ###################################################
    ###################################################
    # teste de estacionaridade no vetor de resíduos ADF
    ###################################################

    # teste implementado calculado conforme planilha do Sergio Ferro
    meia_vida_raw, estatistica_estac = test_ADF_sf(residuos_adf, x, y)

    # verifica se o beta do par está na faixa admissível
    beta_ativo2_ok = (beta_ativo2 >= 0.5) and (beta_ativo2 <= 1.5)

    # Resultado dos testes
    match_99 = (estatistica_estac < crit_99) and beta_ativo2_ok
    match_95 = (estatistica_estac < crit_95) and beta_ativo2_ok
    match_90 = (estatistica_estac < crit_90) and beta_ativo2_ok

    # desvio padrão dos resíduos. Tem que ser calculado aqui para ser utilizado no
    # teste de sinal de entrada na operação
    desvio_padrao_res = residuos_pd.stack().std()

    # valor padrão do sinal de entrada. No caso de
    # não ter qualquer um dos matches, não tem sentido ser calculado.
    sinal_entrada = 0
    spread = 0.0

    # Se algum dos testes de hipótese retornou verdadeiro, calcula a meia vida e testa se
    # há sinal de entrada na operação
    if match_99 or match_95 or match_90:
        # teste de possível sinal de entrada na operação.
        lim_pos = 2.0 * np.abs(desvio_padrao_res)
        lim_neg = -2.0 * np.abs(desvio_padrao_res)

        if (residuos_adf[0] > lim_pos):
            sinal_entrada = 1
        elif (residuos_adf[0] > 0.0):
            sinal_entrada = 2
        elif (residuos_adf[0] < lim_neg):
            sinal_entrada = 4
        elif (residuos_adf[0] < 0.0):
            sinal_entrada = 3
        else:
            sinal_entrada = 0

    # formatar as casas decimais e cast para strings para colocar no JSON
    for i in range(len(residuos_adf)):
        residuos_adf[i] = "{0:.4f}".format(residuos_adf[i])

    crit_99 = "{0:.4f}".format(crit_99)
    crit_95 = "{0:.4f}".format(crit_95)
    crit_90 = "{0:.4f}".format(crit_90)
    ADF_result = "{0:.4f}".format(estatistica_estac)
    pValue = 0.0
    media = "{0:.4f}".format(np.mean(residuos_adf))
    desvio = "{0:.4f}".format(desvio_padrao_res)
    spread_res = spread
    meia_vida = "{0:.1f}".format(meia_vida_raw)
    alfa = alfa
    beta_ativo_dep = beta_ativo2
    beta_tempo_ = beta_tempo

    # Sinaliza o nível de confiança obtido nesse par
    nivel_confianca = 0
    if match_99:
        nivel_confianca = 99
    elif match_95:
        nivel_confianca = 95
    elif match_90:
        nivel_confianca = 90

    # CointegrationParResultados
    if match_99 or match_95 or match_90:

        data_residuos = []
        for j in range(per_teste - 1):
            data_residuos.append(residuos[j][0])

        residuosPar = vars(CointegrationResiduosPar(ativo_dep, ativo_indep, data_inicial, periodo, desvio, media, \
                                                    data_residuos))

        resultados = vars(
            CointegrationParResultados(ativo_dep, ativo_indep, periodo, beta_ativo_dep, sinal_entrada, meia_vida,\
                                       ADF_result, data_inicial, nivel_confianca, beta_tempo_, alfa))

        pair_history = vars(CointegrationPairHistory(ativo_dep, ativo_indep, data_inicial, sinal_entrada))
    else:
        resultados = None
        residuosPar = None
        pair_history = None

    return resultados, residuosPar, pair_history
