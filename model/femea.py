from model.animal import Animal

class Femea(Animal):
    def __init__(self, brinco, raca, data_nascimento):
        super().__init__(brinco, raca, data_nascimento)
        self.estado_reprodutivo = "Vazia" 
        self.data_ultima_inseminacao = None

    def inseminar(self, data):
        pass
        
    def confirmar_prenhez(self):
        pass