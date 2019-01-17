# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 09:15:10 2016

@author: Marcelo Del Fiore
"""
import datetime

from util.extrai_dados_diarios_bovespa import extrai_dados_formato_bovespa

from service.ServiceDatabase import DataBase

import pandas as pd

from model.Tradezone import Tradezone

from model.constantes import feriados

import os

import csv

ERRO_LEITURA_LISTA_ATIVOS = 1
ERRO_LEITURA_ARQUIVO_DADOS = 2
ATUALIZACAO_OK = 3

path_data = os.getcwd() + '/data'

lista_ativos = 'ativos_CUSTOM.csv'

# lê o primeiro arquivo de dados especificado
arq_ativos = os.path.join(path_data, lista_ativos)

try:
    with open(arq_ativos, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        ativos_selec = list(reader)

        # fecha o arquivo de dados já lido
        csvfile.close()
except:
    pass

hoje = datetime.date.today()

"""
verificação da diferença que deve ser usada para calcular a data de ontem, para só usar dias uteis. Segunda-feira = 0
até Domingo = 6
"""
hoje_dia = hoje.weekday()

if hoje_dia in {1, 2, 3, 4, 5}:
    diferenca = 1
elif hoje_dia == 6:
    diferenca = 2
else:
    diferenca = 3

data_pregao_anterior = hoje - datetime.timedelta(days=diferenca)

DataBase.connect()
last_run, last_data = DataBase.getLastRunData()
print("==> Última atualização dos bancos de dados foi realizada com dados do dia : " + str(last_data))

inicio_atualiza_data = datetime.datetime.strptime(last_data, '%Y%m%d') + datetime.timedelta(days=1)

datelist = pd.bdate_range(inicio_atualiza_data, data_pregao_anterior).tolist()

tradezone_connection = Tradezone()

for codigo in ativos_selec:
    arquivo_saida = str(codigo[0]) + '.csv'
    arquivo_de_saida = os.path.join(path_data, arquivo_saida)
    arquivo_saida = open(arquivo_de_saida, 'at')
    status = ATUALIZACAO_OK
    # depois de determinado o período em que os dados devem ser atualizados
    for query_date in datelist:
        date_str = str(query_date)
        tradezone_formated_date = date_str[0:10]
        output_file_formated_date = date_str[0:4] + date_str[5:7] + date_str[8:10]
        # e só vai fazer a atualização se o dia em questão não for feriado
        if output_file_formated_date not in feriados:
            cotacao = tradezone_connection.daily_quote_history(codigo[0], tradezone_formated_date, tradezone_formated_date)
            if len(cotacao) != 0:
                lista_dados = cotacao.split(';')
                data_hora = lista_dados[0]
                data = data_hora[0:10]
                output_file_formated_date = data[6:10] + data[3:5] + data[0:2]
                abertura = lista_dados[1]
                maxima = lista_dados[2]
                minima = lista_dados[3]
                fechamento = str("{0:.2f}".format(float((lista_dados[4]).strip('0').replace(',', '.'))))

                # escreve no arquivo de dados
                t1 = str(output_file_formated_date)
                t2 = str(fechamento)
                linha = t1 + ';' + t2 + '\n'
                arquivo_saida.write(linha)
            else:
                cotacao = "ERRO NOS DADOS RECEBIDOS - Comprimento nulo !"

tradezone_connection.logout_command()

# se atualizou corretamente atualiza o registro no BD
if status == ATUALIZACAO_OK:
    DataBase.connect()
    DataBase.saveLast(1, output_file_formated_date)
    DataBase.desconnect()
    print 'Atualização feita corretamente'
elif status == ERRO_LEITURA_LISTA_ATIVOS:
    print 'Erro na abertura do arquivo contendo a lista de ativos para atualizar'
else:
    print 'Erro na abertura do arquivo de dados'
