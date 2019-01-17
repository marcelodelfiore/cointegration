# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 10:23:27 2016

@author: Marcelo Del Fiore
"""

import time
from datetime import datetime

#import schedule

from service.ServiceJob import Jobs


def job():
    print("==> Cálculo da Cointegraçãos dos Ativos Selecionados foi Iniciado em:" + str(datetime.now()))
    Jobs.CalculoCointegration()


print("================================================================================================")
print("==> Cálculo da Cointegrações dos Ativos Selecionados foi Iniciado em: " + str(datetime.now()))
print("================================================================================================")
print("\n")

# a linha abaixo vai servir se a aplicação for hospedada
#schedule.every().day.at("18:15").do(job)

Jobs.CalculoCointegration()

#while 1:
#    schedule.run_pending()
#    time.sleep(1)
