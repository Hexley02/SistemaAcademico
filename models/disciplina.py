class Disciplina:
    def __init__(self, codigo:int, nome:str, carga_horaria:int, professor_responsavel, alunos:list):
        self.__codigo = codigo
        self.__nome = nome
        self.__carga_horaria = carga_horaria
        self.__professor_responsavel = professor_responsavel
        self.__alunos = alunos

#getters
    def get_codigo(self):
        return self.__codigo
    
    def get_nome(self):
        return self.__nome
    
    def get_carga_horaria(self):
        return self.__carga_horaria
    
    def get_professor_responsavel(self):
        return self.__professor_responsavel
    
    def get_alunos(self):
        return self.__alunos

#setters
    def set_nome(self, nome:str):
        self.__nome = nome
        
    def set_carga_horaria(self, carga_horaria:int):
        self.__carga_horaria = carga_horaria
        
    def set_professor_responsavel(self, professor):
        self.__professor_responsavel = professor
        
    def set_alunos(self, alunos:list):
        self.__alunos = alunos

#metódos
    def adicionar_aluno(self, aluno):
        self.__alunos.append(aluno)
    
    def remover_aluno(self, aluno):
        if aluno in self.__alunos:
            self.__alunos.remove(aluno)

    def exibir_detalhes(self) -> str:
        professor = self.__professor_responsavel.get_nome() if self.__professor_responsavel else "Sem professor"
        nomes_alunos = ', '.join([a.get_nome() for a in self.__alunos]) if self.__alunos else "Sem alunos"
        detalhes = (
            f"Código: {self.__codigo}\n"
            f"Nome: {self.__nome}\n"
            f"Carga horária: {self.__carga_horaria}h\n"
            f"Professor responsável: {professor}\n"
            f"Alunos: {nomes_alunos}"
        )
        return detalhes
