class CointegrationParResponse(object):
    def __init__(self, ativo1, ativo2, data_inicial, data_geracao):
        self.ativo1 = ativo1
        self.ativo2 = ativo2
        self.periodos = []
        self.data_inicial = data_inicial
        self.data_geracao = data_geracao

    def addPeriodo(self, periodo):
        self.periodos.append((periodo))
