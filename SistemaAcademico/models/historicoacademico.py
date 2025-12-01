import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.matricula import Matricula
    from models.disciplina import Disciplina
    from models.matriculapagadisciplina import MatriculaPagaDisciplina

class HistoricoAcademico:
    
    def __init__(self, matricula_aluno: 'Matricula', data_emissao: datetime.date, 
                quantidade_creditos: int, lista_atividades_complemetares = [],
                 registros_disciplinas: List['MatriculaPagaDisciplina'] = None
                ):
        
        self.__matricula_aluno = matricula_aluno
        self.__data_emissao = data_emissao
        self.__registros_disciplinas = registros_disciplinas if registros_disciplinas is not None else []
        self.__quantidade_creditos = quantidade_creditos
        self.__lista_atividades_complementares = lista_atividades_complemetares if lista_atividades_complemetares is not None else []

    # Getters 

    def get_matricula_aluno(self) -> 'Matricula':
        return self.__matricula_aluno
    
    def get_data_emissao(self) -> datetime.date:
        return self.__data_emissao
    
    def get_registros_disciplinas(self) -> List['MatriculaPagaDisciplina']:
        return self.__registros_disciplinas
    
    def get_quantidade_creditos(self) -> int:
        return self.__quantidade_creditos
    
    def get_lista_atividades_complementares(self) -> list:
        return self.__lista_atividades_complementares
    
    # Métodos

    # método para lista de atividades complementares

    def adicionar_atividade_complementar(self, descricao_atividade: str) -> None:
        
        if not isinstance(descricao_atividade, str) or not descricao_atividade.strip():
            raise TypeError("A descrição da atividade deve ser uma string não vazia.")
            
        self.__lista_atividades_complementares.append(descricao_atividade)
        print(f"Atividade '{descricao_atividade[:30]}...' adicionada com sucesso.")

    def calcular_ira(self) -> float:
        """ Calcula o Índice de Rendimento Acadêmico (IRA).
        """
        if not self.__registros_disciplinas:
            return 0.0
        
        total_pontos = 0
        total_creditos = 0
        
        for registro in self.__registros_disciplinas:
            if hasattr(registro, 'get_media_final') and hasattr(registro, 'get_creditos_disciplina'):
                media = registro.get_media_final()
                creditos = registro.get_creditos_disciplina() 
                
                total_pontos += (media * creditos)
                total_creditos += creditos
        
        ira = total_pontos / total_creditos if total_creditos > 0 else 0.0
        return ira

    def exibir_historico(self) -> None:
        
        ira_atual = self.calcular_ira()
        
        print(f"\n===== HISTÓRICO ACADÊMICO ({self.__data_emissao.strftime('%d/%m/%Y')}) =====")
        print(f"Referência Matrícula: {self.__matricula_aluno.get_id()}")
        print(f"Quantidade de Créditos: {self.__quantidade_creditos}")
        print(f"IRA/CR Atual: **{ira_atual:.2f}**")
        print(f"Total de Registros de Disciplinas: {len(self.__registros_disciplinas)}")
        
        print("\n--- REGISTROS DE DISCIPLINAS ---")
        for i, registro in enumerate(self.__registros_disciplinas):
            disc_nome = registro.get_disciplina().get_nome() if hasattr(registro, 'get_disciplina') else "N/A"
            media = registro.get_media_final() if hasattr(registro, 'get_media_final') else "N/A"
            print(f"Registro {i+1}: {disc_nome} (Média: {media:.2f})")
            
        print("\n--- ATIVIDADES COMPLEMENTARES ---")
        if self.__lista_atividades_complementares:
            for i, atividade in enumerate(self.__lista_atividades_complementares):
                print(f"[{i+1}] {atividade}")
        else:
            print("Nenhuma atividade complementar registrada.")