class CointegrationParResultados(object):
    def __init__(self, ativo_dep, ativo_indep, periodo, beta_ativo_dep, sinal_entrada, meia_vida,\
                                       ADF_result, data_inicial, nivel_confianca, beta_tempo, alfa):
        self.ativo_dep = ativo_dep
        self.ativo_indep = ativo_indep
        self.periodo = periodo
        self.beta_ativo_dep = beta_ativo_dep
        self.sinal_entrada = sinal_entrada
        self.meia_vida = meia_vida
        self.ADF_result = ADF_result
        self.data_inicial = data_inicial
        self.nivel_confianca = nivel_confianca
        self.beta_tempo = beta_tempo
        self.alfa = alfa
