# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:23:27 2016

@author: Marcelo Del Fiore
"""
import pymongo

import constantes


def seleciona(data=None, beta_min = 0.5, beta_max = 1.5):

    # conecta à BD
    client = pymongo.MongoClient('mongodb://teste:teste@ds023475.mlab.com:23475/cointegracao')
    db = client['cointegracao']

    # seleciona a collection apropriada
    collection = db['cointegrations_summary']

    result = []

    cursor = collection.find({"dataInicial": data,
                            "cointegrations.sinal_entrada": {"$in": ['C', 'V']},
                            "cointegrations.beta_ativo2": {"$gte": str(0.5), "$lte": str(1.5), }},
                            {'cointegrations.ativo1': 'true', 'cointegrations.ativo2': 'true',
                            'cointegrations.beta_ativo2': 'true', 'cointegrations.sinal_entrada': 'true'})

    for doc in cursor:
        result.append(doc)

    # desconecta do BD
    client.close()

    return result
