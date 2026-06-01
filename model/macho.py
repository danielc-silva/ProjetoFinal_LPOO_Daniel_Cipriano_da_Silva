from animal import Animal

class Macho(Animal):
    def __init__(self, brinco, raca, data_nascimento, peso, lote=None, castrado=False):
        super().__init__(brinco, raca, data_nascimento, peso, lote)
        self.castrado = castrado