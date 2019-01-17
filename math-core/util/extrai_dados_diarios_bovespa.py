# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:01:24 2016

@author: Marcelo Del Fiore
"""

""" Script utilizado para ler os arquivos de dados históricos baixados do site
    da bovespa 
    http://www.bmfbovespa.com.br/pt_br/servicos/market-data/historico/mercado-a-vista/series-historicas/
    e extrair os dados de ativos no "formato de candle", isto é, máxima,
    mínima, abertura e fechamento
"""

import csv
import os

ERRO_LEITURA_LISTA_ATIVOS = 1
ERRO_LEITURA_ARQUIVO_DADOS = 2
ATUALIZACAO_OK = 3

def extrai_dados_formato_bovespa(dia):

    path_data = os.getcwd() + '/data'
    path_temp = path_data + '/market_data'

    lista_ativos = 'lista_diaria_ativos_para_atualizar.csv'

    # lê o primeiro arquivo de dados especificado
    arq_ativos = os.path.join(path_temp, lista_ativos)

    try:
        with open(arq_ativos, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            ativos_selec = list(reader)

            # fecha o arquivo de dados já lido
            csvfile.close()
    except:
        return ERRO_LEITURA_LISTA_ATIVOS

    # array para armazenar os dados extraídos
    codneg = []
    preabe = []
    premax = []
    premin = []
    premed = []
    preult = []

    # data para compor o nome do arquivo de dados da bovespa
    data_dados = dia

    # leitura do arquivo de dados da bovespa
    arquivo_temp = 'COTAHIST_D' + data_dados + '.txt'
    arquivo_dados = os.path.join(path_temp, arquivo_temp)
    try:
        dados = open(arquivo_dados, 'rt')
    except:
        return ERRO_LEITURA_ARQUIVO_DADOS

    # lê a primeira linha do arquivo que deve ser a descrição dos dados
    linha_titulo = dados.readline()
    linhas = dados.readlines()

    # data do pregão em questão
    data = linha_titulo[23:31]

    # geração do nome do arquivo de saída com os dados para a planilha so Sérgio Ferro
    nome_planilha = data[0:4] + data[4:6] + data[6:8] + '_planilha_cointegracao' + '.csv'
    nome_arquivo_saida_planilha = os.path.join(path_temp, nome_planilha)


    # extrai os dados do arquivo de cotações daquele dia
    for linha in linhas:
        codneg.append(linha[12:24])
        preabe.append(linha[57:69])
        premax.append(linha[70:82])
        premin.append(linha[83:95])
        preult.append(linha[109:121])

    # remove os espaços em branco que existem à direita dos códigos dos ativos
    codneg = [i.rstrip(' ') for i in codneg]

    # remove os zeros que existem à esquerda dos preços
    preabe = [i.lstrip('0') for i in preabe]
    preabe = [i.lstrip('0') for i in preabe]
    premax = [i.lstrip('0') for i in premax]
    premin = [i.lstrip('0') for i in premin]
    preult = [i.lstrip('0') for i in preult]

    linha_planilha = ''
    linha_planilha2 = ''

    # varre a lista de ativos que precisam ser atualizados com os dados baixados
    for codigo in ativos_selec:
        for i in range(len(codneg)):
            if codneg[i] == codigo[0]:
                # abre o arquivo de dados
                arquivo_saida = codneg[i] + '.csv'
                arquivo_de_saida = os.path.join(path_data, arquivo_saida)
                arquivo_saida = open(arquivo_de_saida, 'at')

                # prepara o conteúdo para escrever
                t1 = str(data)
                t2 = str(float(preult[i]) / 100)
                linha = t1 + ';' + t2 + '\n'

                # string para atualizar a planilha
                temp2 = codneg[i] + ';'
                temp = t2 + ';'
                linha_planilha += temp
                linha_planilha2 += temp2

                # atualiza a BD
                arquivo_saida.write(linha)

                # fecha o arquivo
                arquivo_saida.close()

    # gera a atualização para a planilha do Sérgio Ferro
    linha_planilha = linha_planilha.replace('.', ',')
    linha_planilha2 = linha_planilha2 + '\n'
    arquivo_saida_planilha = open(nome_arquivo_saida_planilha, 'wt')
    arquivo_saida_planilha.write(linha_planilha2)
    arquivo_saida_planilha.write(linha_planilha)
    arquivo_saida_planilha.close()

    return ATUALIZACAO_OK
