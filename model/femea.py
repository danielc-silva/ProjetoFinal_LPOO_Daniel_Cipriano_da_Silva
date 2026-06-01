from animal import Animal

class Femea(Animal):
    def __init__(self, brinco, raca, data_nascimento, peso, lote=None):
        super().__init__(brinco, raca, data_nascimento, peso, lote)
        self.estado_reprodutivo = "Vazia" 
        self.data_ultima_inseminacao = None

    def inseminar(self, data):
        pass
        
    def confirmar_prenhez(self):
        pass