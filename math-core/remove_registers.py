from service.ServiceDatabase import DataBase

DataBase.connect()

delete_date = "20170410"

DataBase.delete_cointegration_registers(delete_date)

DataBase.desconnect()
