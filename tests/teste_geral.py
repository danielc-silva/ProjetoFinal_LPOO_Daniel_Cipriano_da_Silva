import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.proprietario import Proprietario
from model.femea import Femea
from model.raca import Raca
from model.manejo import Manejo

from dao.pessoa_dao import PessoaDAO
from dao.animal_dao import AnimalDAO
from dao.manejos_dao import ManejosDAO 

from model.pessoa_factory import PessoaFactory
from model.animal_factory import AnimalFactory

def executar_teste():
    print("=== INICIANDO TESTE COMPLETO DO SISTEMA ===\n")

    pessoa_dao = PessoaDAO()
    animal_dao = AnimalDAO()
    manejo_dao = ManejosDAO()

    cpf_teste = "04110220084" 
    brinco_teste = 121

    print("--- Testando PessoaDAO ---")
    try:
        prop = Proprietario(
            cpf=cpf_teste, 
            nome="João da Silva", 
            telefone="54999999999", 
            inscricao_estadual="123456789", 
            nome_fazenda="Fazenda Esperança"
        )
        sucesso, msg = pessoa_dao.salvar(prop)
        print(f"Resultado: {msg}")
    except Exception as e:
        print(f"Aviso/Erro Pessoa: {e}")


    print("--- Testando PessoaFactory ---")
    try:
        prop = PessoaFactory.criar_pessoa("Proprietario",
            cpf="81238070078", 
            nome="João da Silva", 
            telefone="54999999999", 
            inscricao_estadual="123456789", 
            nome_fazenda="Fazenda Esperança"
        )
        sucesso, msg = pessoa_dao.salvar(prop)
        print(f"Resultado: {msg}")
    except Exception as e:
        print(f"Aviso/Erro Pessoa: {e}")


    print("\n--- Testando AnimalDAO ---")
    try:
        vaca = Femea(brinco=brinco_teste, raca=Raca.ANGUS, data_nascimento="10-01-2022")
        vaca.estado_reprodutivo = "Vazia" 
        sucesso, msg = animal_dao.salvar(vaca)
        print(f"Resultado: {msg}")
    except Exception as e:
        print(f"Aviso/Erro Animal: {e}")

    print("\n--- Testando AnimalFactory ---")
    try:
        vaca = AnimalFactory.criar_animal("Macho", brinco= 987, raca=Raca.ANGUS, data_nascimento="10-01-2022")
        vaca.estado_reprodutivo = "Vazia" 
        sucesso, msg = animal_dao.salvar(vaca)
        print(f"Resultado: {msg}")
    except Exception as e:
        print(f"Aviso/Erro Animal: {e}")


    print("\n--- Testando ManejosDAO ---")
    try:

        novo_manejo = Manejo(
            brinco_animal=brinco_teste,
            cpf_responsavel=cpf_teste,
            data_evento="15-05-2024",
            tipo_evento="Inseminação",
            observacao="Manejo test"
        )
        
        sucesso, msg = manejo_dao.salvar(novo_manejo)
        print(f"Resultado: {msg}")
        
    except Exception as e:
        print(f"Aviso/Erro Manejo: {e}")

if __name__ == "__main__":
    executar_teste()