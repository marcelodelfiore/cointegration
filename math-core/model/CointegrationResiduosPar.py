class CointegrationResiduosPar(object):
    def __init__(self, ativo_dep, ativo_indep, data_inicial, periodo, desvio, media, residuos):
        self.ativo_dep = ativo_dep
        self.ativo_indep = ativo_indep
        self.data_inicial = data_inicial
        self.periodo = periodo
        self.desvio = desvio
        self.media = media
        self.residuos = residuos
