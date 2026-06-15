from model.femea import Femea
from model.macho import Macho

class AnimalFactory:
    
    @staticmethod
    def criar_animal(tipo_animal, brinco, raca, data_nascimento, is_castrado=None, estado_reprodutivo=None):

        if tipo_animal == 'Femea':
            return Femea(brinco, raca, data_nascimento, estado_reprodutivo)
            
        elif tipo_animal == 'Macho':
            return Macho(brinco, raca, data_nascimento, is_castrado)
            
        else:
            raise ValueError(f"Erro no Factory: O tipo '{tipo_animal}' não existe no sistema.")