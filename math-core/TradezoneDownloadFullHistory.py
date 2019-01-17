# -*- coding: utf-8 -*-
"""
Created on Mon Fev 27 2017

@author: Marcelo Del Fiore
"""

""" Script utilizado para ler os arquivos de dados históricos baixados do site
    do Tradezone e extrair os dados de ativos no "formato de candle", isto é, máxima,
    mínima, abertura e fechamento
"""

import csv
import os
from model.Tradezone import Tradezone
import pandas
import datetime
from model.constantes import feriados

ERRO_LEITURA_LISTA_ATIVOS = 1
ERRO_LEITURA_ARQUIVO_DADOS = 2
ATUALIZACAO_OK = 3

path_data = os.getcwd() + '/data'
path_temp = path_data + '/market_data'

lista_ativos = 'lista_diaria_ativos_para_atualizar.csv'

# lê o primeiro arquivo de dados especificado
lista_ativos = os.path.join(path_temp, lista_ativos)

try:
    with open(lista_ativos, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        ativos_selec = list(reader)
        csvfile.close()
except:
    pass

# inicializa a conexão com o app Tradezone para ler as requisições GET
tradezone_connection = Tradezone()

# período de tempo para leitura, o BD tem que ter 250 dias úteis
hoje = datetime.date.today()
hoje_dia = hoje.weekday()

if hoje_dia in {1, 2, 3, 4, 5}:
    diferenca = 1
elif hoje_dia == 6:
    diferenca = 2
else:
    diferenca = 3

data_pregao_anterior = hoje - datetime.timedelta(days=diferenca)

inicio = data_pregao_anterior - datetime.timedelta(days=380)

datelist = pandas.bdate_range(end=data_pregao_anterior, start=inicio).tolist()

# varre a lista de ativos que precisam ser atualizados com os dados baixados
for codigo in ativos_selec:
    arquivo_saida = str(codigo[0]) + '.csv'
    arquivo_de_saida = os.path.join(path_data, arquivo_saida)
    arquivo_saida = open(arquivo_de_saida, 'wt')
    for data_consulta in datelist:
        date_str = str(data_consulta)
        tradezone_formated_date = date_str[0:10]
        output_file_formated_date = date_str[0:4] + date_str[5:7] + date_str[8:10]
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
            else:
                cotacao = "ERRO NOS DADOS RECEBIDOS - Comprimento nulo !"

            #print codigo, output_file_formated_date, cotacao
            arquivo_saida.write(linha)
        else:
            pass

    arquivo_saida.close()

tradezone_connection.logout_command()



