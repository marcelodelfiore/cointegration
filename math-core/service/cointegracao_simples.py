# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 14:19:18 2016

@author: Marcelo Del Fiore
"""

import algos_coin
from service.ServiceDatabase import DataBase
import os
from sys import platform as _platform


def cointegracao_simples(ativo1, ativo2, data_inicial, data_geracao):

    data = None

    if _platform == "linux" or _platform == "linux2":
        os.system('clear')
    elif _platform == "darwin":
        pass
    elif _platform == "win32":
        os.system('cls')

    temp = ativo1 + '/' + ativo2

    print('Calculando a cointegração do par ' + temp)

    # periodos
    periods = [100, 120, 140, 160, 180, 200, 220, 250]

    # chama o teste de conintegração para dois ativos
    result_coins = []
    result_residuos = []
    result_hystory = []

    for periodo in periods:
        resultado_periodo, residuosPar, pair_history = algos_coin.testa_coin_simples(ativo1, ativo2, periodo,
                                                                                     data_inicial)

        if resultado_periodo is not None:
            result_coins.append(resultado_periodo)
            result_residuos.append(residuosPar)
            result_hystory.append(pair_history)

    # se para qualquer período, há cointegração em alqum dos níveis de significancia de interesse
    quantidade_cointegrados_99 = 0
    quantidade_cointegrados_95 = 0
    quantidade_cointegrados_90 = 0

    list_periodos = result_coins

    for algo_coin in list_periodos:
        if algo_coin is not None:
            if algo_coin['nivel_confianca'] == 99:
                quantidade_cointegrados_99 += 1

            if algo_coin['nivel_confianca'] == 95:
                quantidade_cointegrados_95 += 1

            if algo_coin['nivel_confianca'] == 90:
                quantidade_cointegrados_90 += 1

    if (quantidade_cointegrados_99 >= 3) or (quantidade_cointegrados_95 >= 3) or (quantidade_cointegrados_90 >= 3):

        DataBase.connect()
        DataBase().insertCointegrationPar(result_coins)
        DataBase().insertCointegrationResidues(result_residuos)
        DataBase().insertCointegrationHystory(pair_history)
        DataBase.desconnect()
