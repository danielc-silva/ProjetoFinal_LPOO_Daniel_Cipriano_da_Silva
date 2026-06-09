from model.proprietario import Proprietario
from model.veterinario import Veterinario

class PessoaFactory:
    
    @staticmethod
    def criar_pessoa(tipo_pessoa, cpf, nome, telefone, inscricao_estadual=None, nome_fazenda=None, crmv=None):

        if tipo_pessoa == 'Proprietario':

            if not inscricao_estadual or not nome_fazenda:
                raise ValueError("Para instanciar um Proprietário, IE e Nome da Fazenda são obrigatórios.")
            
            return Proprietario(cpf, nome, telefone, inscricao_estadual, nome_fazenda)
            
        elif tipo_pessoa == 'Veterinario':
            if not crmv:
                raise ValueError("Para instanciar um Veterinário, o CRMV é obrigatório.")
                
            return Veterinario(cpf, nome, telefone, crmv)
            
        else:
            raise ValueError(f"Erro no Factory: O tipo '{tipo_pessoa}' não existe no sistema.")