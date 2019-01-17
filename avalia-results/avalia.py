# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:23:27 2016

@author: Marcelo Del Fiore
"""

import sys

import constantes

import services.seleciona_entradas


data_avaliacao = sys.argv[1]

status = services.seleciona_entradas.seleciona(data_avaliacao)

res = "Em " + str(data_avaliacao) + 'foram encontrados ' + str(len(status)) + \
      ' pares cointegrados satisfazendo as condições' + '\n'

print len(status)

for i in range(len(status)):
    print status[i]

if status == constantes.AVALIACAO_OK:
    print 'Avaliação terminada corretamente, arquivo de saída gerado.'

elif status == constantes.ERRO_LEITURA_ARQUIVO_RESULTADOS:
    print 'Arquivo resultados não encontrado'

elif status is None:
    print 'Data para avaliação não foi fornecida'
