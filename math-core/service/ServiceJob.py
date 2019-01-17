# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 10:23:27 2016

@author: Marcelo Del Fiore
"""

import pandas as pd
import datetime as datetime

import ServiceCointetrationCalculate
from service.ServiceDatabase import DataBase
from model.constantes import feriados

class Jobs(object):
    @staticmethod
    def CalculoCointegration():
        DataBase.connect()
        last_run, last_data = DataBase.getLastRunData()
        print("==> Última Execução foi realizada com dados do dia : " + str(last_run))

        inicio_run = datetime.datetime.strptime(last_run, '%Y%m%d') + datetime.timedelta(days=1)

        if (last_data > last_run):
            datelist = pd.bdate_range(inicio_run, last_data).tolist()
            for date in datelist:
                # verifica se o dia em que vai ser calculada a cointegração não é feriado
                data_run = date.strftime("%Y%m%d")
                if data_run not in feriados:
                    DataBase.deleteCointegrationResidues()
                    ServiceCointetrationCalculate.CointegrationCalculate('ativos_CUSTOM', str(date.strftime("%Y%m%d")))
                    DataBase.saveLast(2, str(date.strftime("%Y%m%d")))

            DataBase.desconnect()
        else:
            print("\n")
            print("Cálculos já realizados com os últimos dados de mercado disponíveis, nada executado.")

