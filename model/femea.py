from model.animal import Animal
from model.estados_reprodutivos import EstadoVazia, EstadoInseminada, EstadoPrenha

class Femea(Animal):
    def __init__(self, brinco, raca, data_nascimento):
        super().__init__(brinco, raca, data_nascimento)
        # nasceu, no caso foi cadastrada inicia como estado de vazia
        self._estado_objeto = EstadoVazia()

    @property
    def estado_reprodutivo(self):
        return self._estado_objeto.nome

    @estado_reprodutivo.setter
    def estado_reprodutivo(self, valor_do_banco):
        if valor_do_banco == "Vazia":
            self._estado_objeto = EstadoVazia()
        elif valor_do_banco == "Inseminada":
            self._estado_objeto = EstadoInseminada()
        elif valor_do_banco == "Prenha":
            self._estado_objeto = EstadoPrenha()
        else:
            raise ValueError(f"Estado reprodutivo desconhecido: {valor_do_banco}")

    # método para mudanças de estados pelo sistema
    def mudar_estado(self, novo_estado):
        self._estado_objeto = novo_estado

    # métodos utilizados pelo padrão state
    def inseminar(self):
        return self._estado_objeto.registrar_inseminacao(self)

    def diagnosticar(self, positivo):
        return self._estado_objeto.registrar_diagnostico(self, positivo)

    def parir(self):
        return self._estado_objeto.registrar_parto(self)

    def abortar(self):
        return self._estado_objeto.registrar_aborto(self)