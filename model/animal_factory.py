from femea import Femea
from macho import Macho

class AnimalFactory:
    
    @staticmethod
    def criar_animal(tipo_animal, brinco, raca, data_nascimento, castrado=False):

        if tipo_animal == 'Femea':
            return Femea(brinco, raca, data_nascimento)
            
        elif tipo_animal == 'Macho':
            return Macho(brinco, raca, data_nascimento, castrado)
            
        else:
            raise ValueError(f"Erro no Factory: O tipo '{tipo_animal}' não existe no sistema.")