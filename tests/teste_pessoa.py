import sys
import os
import datetime

# adiciona a pasta raiz do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.pessoa import Pessoa

class PessoaTeste(Pessoa):
    pass

if __name__ == "__main__":
    data_nascimento = datetime.date(1990, 5, 15)
    pessoa = PessoaTeste(
        nome="Alan Pereira",
        email="alanpereira@gmail.com",
        data_nascimento=data_nascimento,
        telefone="(81) 98827-2516",
        endereco="Rua da Aurora, 123"
    )

    #calcular idade

    idade = pessoa._calcular_idade()
    print("\nteste: Calcular Idade:")
    print(f"Idade calculada: {idade} anos")

    #exibir detalhes
    print("Testando exibir_detalhes():\n")
    print(pessoa.exibir_detalhes())

    #testar setter de email inválido
    print("\nTestando email inválido:")
    pessoa.set_email("alanpereiragmail.com")

    
    
     
