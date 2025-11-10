import datetime
from aluno import Aluno
from disciplina import Disciplina


class Matricula:
    
    def __init__(self, aluno: 'Aluno', disciplina: 'Disciplina', status: bool, 
                 semestre: str, data_matricula: datetime.date):
        
        self.__aluno = aluno
        self.__disciplina = disciplina
        self.__status = status
        self.__semestre = semestre
        self.__data_matricula = data_matricula

    #Getters 
    
    def get_aluno(self) -> 'Aluno':
        return self.__aluno

    def get_disciplina(self) -> 'Disciplina':
        return self.__disciplina
    
    def get_status(self) -> bool:
        return self.__status
    
    def get_semestre(self) -> str:
        return self.__semestre
    
    def get_data_matricula(self) -> datetime.date:
        return self.__data_matricula

    
   #metódos

    def alterar_matricula(self, novo_status: bool = None):
        
        if novo_status is not None:
            self.set_status(novo_status)
            status_str = "ATIVA" if novo_status else "TRANCADA/CANCELADA"
            
            # Tenta pegar os nomes para uma mensagem informativa
            aluno_nome = self.__aluno.get_nome() if hasattr(self.__aluno, 'get_nome') else "Aluno"
            disc_nome = self.__disciplina.get_nome() if hasattr(self.__disciplina, 'get_nome') else "Disciplina"

            print(f"Matrícula de {aluno_nome} em {disc_nome} alterada para: **{status_str}**.")

    def carregar_dados(self):
        # Tenta pegar os nomes para uma mensagem informativa
        aluno_nome = self.__aluno.get_nome() if hasattr(self.__aluno, 'get_nome') else "Aluno"
        disc_nome = self.__disciplina.get_nome() if hasattr(self.__disciplina, 'get_nome') else "Disciplina"
        
        # Aqui, no código real, você chamaria o GerenciadorArquivos.
        print(f" Dados da matrícula de {aluno_nome} em {disc_nome} carregados com sucesso!")
        
    def __str__(self) -> str:
        """Retorna uma representação em string concisa do objeto."""
        aluno_nome = self.__aluno.get_nome() if hasattr(self.__aluno, 'get_nome') else "Aluno Ref"
        disc_nome = self.__disciplina.get_nome() if hasattr(self.__disciplina, 'get_nome') else "Disciplina Ref"
        status_str = "Ativa" if self.__status else "Inativa"
        return f"Matricula({aluno_nome} em {disc_nome} - Semestre: {self.__semestre}, Status: {status_str})"