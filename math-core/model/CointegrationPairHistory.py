class CointegrationPairHistory(object):
    def __init__(self, ativo_dep, ativo_indep, data_inicial, sinal_entrada):
        self.ativo_dep = ativo_dep
        self.ativo_indep = ativo_indep
        self.data_inicial = data_inicial
        self.sinal_entrada = sinal_entrada
