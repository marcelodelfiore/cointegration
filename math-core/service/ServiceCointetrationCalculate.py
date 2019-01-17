# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 14:19:16 2016

@author: Marcelo Del Fiore
"""
import itertools as it

from datetime import datetime

from service import cointegracao_simples as coin_s

from service.ServiceQuotes import ServiceQuotes


def CointegrationCalculate(lista_ativos, data_inicial):
    print("")
    print("==> Calculando dados para: " + data_inicial)

    # CointegrationCalculate Tempo de execucao
    t1 = datetime.now()

    # lista de argumentos de entrada, se existirem
    lista_ativos += '.csv'

    #
    pares = []

    # lê o primeiro arquivo de dados especificado
    ativos_selec = ServiceQuotes.get_ativos(lista_ativos)

    # armazena a data e hora da execução do teste
    data_geracao = str(datetime.now().strftime("%Y%m%d"))

    # gera os pares para os quais precisamos rodar a verificação de cointegração
    for p in it.permutations(ativos_selec, 2):
        pares.append(p)

    # ajusta a quantidade de repeticões, considerando o 0
    repeticoes = len(pares) - 1

    # chama a rotina de cointegração simples para varrer todas as combinações
    # necessárias para a lista de ativos solicitada
    for i in range(repeticoes):
        # seleciona os ativos, 2 a 2
        ativo1 = pares[i][0][0]
        ativo2 = pares[i][1][0]

        # chama a rotina de cointegração simples
        coin_s.cointegracao_simples(ativo1, ativo2, data_inicial, data_geracao)

    # Print Logs
    delta = datetime.now() - t1
    print("==> Tempo:" + str(delta.total_seconds()) + " segundos")
