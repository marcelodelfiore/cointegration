import csv
import os
import sys

import numpy as np


class ServiceQuotes(object):
    path_data = os.getcwd() + '/data'
    dados = None

    @staticmethod
    def get_quotes(ativo, data_inicial):
        ativo += '.csv'
        dados_selecionados = []
        arq_dados_ativo1 = os.path.join(ServiceQuotes.path_data, ativo)

        try:
            with open(arq_dados_ativo1, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                dados_ativo_raw = list(reader)
                csvfile.close()
        except:
            print "Erro na leitura da base de dados do ativo ", ativo
            sys.exit()

        """
        Ordena os dados, a data mais atual deve ser o primeiro elemento do array de
        dados, e transforma em um array do numpy para processamento
        """
        dados_ativo_raw.sort()
        dados_ativo_raw = dados_ativo_raw[::-1]

        for i in range(len(dados_ativo_raw)):
            if (int(dados_ativo_raw[i][0]) <= int(data_inicial)):
                dados_selecionados.append(dados_ativo_raw[i])

        return np.array(dados_selecionados)

    @staticmethod
    def get_ativos(lista_ativos):
        arq_ativos = os.path.join(ServiceQuotes.path_data, lista_ativos)
        try:
            with open(arq_ativos, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                ativos_selec = list(reader)

                csvfile.close()
        except:
            print "Erro na leitura da base de dados do ativo ", lista_ativos
            sys.exit()

        return ativos_selec
