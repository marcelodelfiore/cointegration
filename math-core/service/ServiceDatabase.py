# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 10:23:27 2016

@author: Marcelo Del Fiore
"""

from datetime import date, timedelta

from pymongo import MongoClient


class DataBase(object):
    @staticmethod
    def connect():
        DataBase.client = MongoClient('mongodb://teste:teste@ds119618.mlab.com:19618/cointegracao')
        DataBase.db = DataBase.client['cointegracao']

    @staticmethod
    def desconnect():
        DataBase.client.close()

    @staticmethod
    def delete_cointegration_registers(delete_date):
        collection = DataBase.db.Pairs
        collection.delete_many({"data_inicial": str(delete_date)})

    @staticmethod
    def insertCointegrationSummary(jsonData):
        collection = DataBase.db.cointegrations_summary
        collection.delete_one({"dataInicial": str(jsonData['dataInicial'])})
        inserted_id = collection.insert_one(jsonData).inserted_id
        return inserted_id

    @staticmethod
    def insertCointegrationPar(jsonData):
        collection = DataBase.db.Pairs
        if (jsonData):
            inserted_ids = collection.insert_many(jsonData).inserted_ids
            return inserted_ids

    @staticmethod
    def insertCointegrationResidues(jsonData):
        collection = DataBase.db.Residues
        if (jsonData):
            inserted_ids = collection.insert_many(jsonData).inserted_ids
            return inserted_ids

    @staticmethod
    def deleteCointegrationResidues():
        collection = DataBase.db.Residues
        collection.remove({})

    @staticmethod
    def insertCointegrationHystory(jsonData):
        collection = DataBase.db.PairsHistory
        if (jsonData):
            inserted_ids = collection.insert_one(jsonData).inserted_id
            return inserted_ids


    @staticmethod
    def getLastRunData():
        # type: () -> object

        # Recupera a última data onde as cointegrações foram calculadas
        collection = DataBase.db.LastRun
        cursor = collection.find()
        last_job = None
        for document in cursor:
            last_job = (document['date'])

        if (last_job is None):
            last_job = (date.today() - timedelta(days=20))

        # Recupera a última data onde os dados de mercado foram atualizados
        collection = DataBase.db.LastData
        cursor = collection.find()
        last_data = None
        for document in cursor:
            last_data = (document['date'])

        if (last_data is None):
            last_data = (date.today() - timedelta(days=20))

        return last_job, last_data

    @staticmethod
    def saveLast(colec, date):
        if colec == 1:
            collection = DataBase.db.LastData
        elif colec == 2:
            collection = DataBase.db.LastRun

        collection.remove()
        last = collection.insert_one({"date": date})

        return last
