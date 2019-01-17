class CointegrationParCriterios(object):
    VALOR_95 = "95"
    VALOR_99 = "99"

    def __init__(self, name, valor, match):
        self.name = name
        self.valor = valor
        self.match = str(match)
