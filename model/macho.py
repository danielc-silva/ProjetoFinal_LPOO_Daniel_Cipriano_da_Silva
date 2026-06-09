from model.animal import Animal

class Macho(Animal):
    def __init__(self, brinco, raca, data_nascimento, castrado=False):
        super().__init__(brinco, raca, data_nascimento)
        self.castrado = castrado