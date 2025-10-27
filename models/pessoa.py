import datetime

class Pessoa:
    def __init__(self, nome:str, email:str, data_nascimento:datetime, telefone:str , endereco:str):
        self.__nome = nome 
        self.__email = email
        self.__data_nascimento = data_nascimento
        self.__telefone = telefone
        self.__endereco = endereco 
#getters 
    def get_nome(self):
        return self.__nome
    
    def get_email(self):
        return self.__email
    
    def get_data_nascimento(self):
        return self.__data_nascimento
    
    def get_telefone(self):
        return self.__telefone
    
    def get_endereco(self):
        return self.__endereco
    
#setters  
    def set_email(self, email: str):
        if "@" in email:
            self.__email = email
        else:
            print(" Email inválido!")
      
#metódos 

    def _calcular_idade(self) -> int:
        hoje = datetime.date.today()
        nascimento = self.__data_nascimento
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade

    def exibir_detalhes(self) -> str:
        nome = self.__nome
        email = self.__email
        data = self.__data_nascimento
        if hasattr(data, 'strftime'):
            try:
                data_str = data.strftime('%d/%m/%Y')
            except Exception:
                data_str = str(data)
        else:
            data_str = str(data)
        idade = self._calcular_idade()
        telefone = self.__telefone
        endereco = str(self.__endereco)
        detalhes = (
            f"Nome: {nome}\n"
            f"Email: {email}\n"
            f"Data de nascimento: {data_str}\n"
            f"Idade: {idade}\n"
            f"Telefone: {telefone}\n"
            f"Endereço: {endereco}"
        )
        return detalhes










    














        
    
    