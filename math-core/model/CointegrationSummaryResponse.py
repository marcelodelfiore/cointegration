import json


class CointegrationSummaryResponse(object):
    def __init__(self, cointegrations, dataInicial, dataGeracao):
        self.cointegrations = cointegrations
        self.dataInicial = str(dataInicial)
        self.dataGeracao = str(dataGeracao)

    def __repr__(self):
        return json.dumps(self.__dict__)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
