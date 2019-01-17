class CointegrationSummary(object):
    def __init__(self, ativo1, ativo2, beta_ativo2, hurst_exp, sinal_entrada, meia_vida, co99, co95, co90):
        self.ativo1 = ativo1
        self.ativo2 = ativo2
        self.beta_ativo2 = beta_ativo2
        self.hurst_exp = hurst_exp
        self.sinal_entrada = sinal_entrada
        self.meia_vida = meia_vida
        self.co99 = co99
        self.co95 = co95
        self.co90 = co90
