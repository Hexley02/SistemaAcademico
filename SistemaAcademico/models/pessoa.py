import datetime


class Pessoa:
    def __init__(self, nome: str, email: str, data_nascimento: datetime.date, telefone: str, endereco: str):
        self.__nome = nome 
        self.__email = email
        self.__data_nascimento = data_nascimento
        self.__telefone = telefone
        self.__endereco = endereco

    # getters 
    def get_nome(self) -> str:
        return self.__nome
    
    def get_email(self) -> str:
        return self.__email
    
    def get_data_nascimento(self) -> datetime.date:
        return self.__data_nascimento
    
    def get_telefone(self) -> str:
        return self.__telefone
    
    def get_endereco(self) -> str:
        return self.__endereco
    
    # setters  
    def set_email(self, email: str) -> None:
        if "@" in email:
            self.__email = email
        else:
            print("Email inválido!")
    """
    criar outras limitações e verificações para email. usando except
    """
      
    # métodos 

    def calcular_idade(self) -> int:
        
        hoje = datetime.date.today()
        nascimento = self.__data_nascimento
       
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade

    def exibir_detalhes(self) -> str:
        
        nome = self.__nome
        email = self.__email
        data = self.__data_nascimento
        
        data_str = data.strftime('%d/%m/%Y')
        
        idade = self.calcular_idade() 
        telefone = self.__telefone
        endereco = self.__endereco
        
        detalhes = (
            f"Nome: {nome}\n"
            f"Email: {email}\n"
            f"Data de nascimento: {data_str}\n"
            f"Idade: {idade} anos\n"
            f"Telefone: {telefone}\n"
            f"Endereço: {endereco}"
        )
        return detalhes