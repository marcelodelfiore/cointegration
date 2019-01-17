from pymongo import MongoClient


class oDataBase(object):
    @staticmethod
    def connect():
        DataBase.client = MongoClient('mongodb://teste:teste@ds023475.mlab.com:23475/cointegracao')
        DataBase.db = oDataBase.client['cointegracao']

    @staticmethod
    def desconnect():
        oDataBase.client.close()

    @staticmethod
    def RetrieveSummaryData(ativo1, ativo2):

        return registro
