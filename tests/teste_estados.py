import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.femea import Femea
from model.raca import Raca

def testar_estados():
    mimosa = Femea(brinco=101, raca=Raca.ANGUS, data_nascimento="01-01-2022")
    print(f"Estaddo inicial: {mimosa.estado_reprodutivo}")

    mimosa.inseminar()
    print(f"depois de inseminar: {mimosa.estado_reprodutivo}")

    mimosa.diagnosticar(positivo=True)
    print(f"Após toque positivo: {mimosa.estado_reprodutivo}")

    print("\nTestand inseminar matriz prenha:")
    try:
        mimosa.inseminar()
    except Exception as e:
        print(f"Erro capturado: {e}")

    print("\n")
    mimosa.parir()
    print(f"depois q parir: {mimosa.estado_reprodutivo}")

if __name__ == "__main__":
    testar_estados()