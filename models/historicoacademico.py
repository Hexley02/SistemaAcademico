import datetime
from matricula import Matricula
from disciplina import Disciplina
from matriculapagadisciplina import MatriculaPagaDisciplina  

class HistoricoAcademico:
    
    def __init__(self, matricula: "Matricula", data: datetime.date, disciplinas: list, 
                 carga_horaria: float, quantidade_creditos: int, matricula_pd: list = None):
        
        self.__matricula = matricula
        self.__data = data
        self.__disciplinas = disciplinas if disciplinas is not None else [] 
        self.__carga_horaria = carga_horaria
        self.__quantidade_creditos = quantidade_creditos
        self.__matricula_pd = matricula_pd if matricula_pd is not None else []

    #Getters 
    
    def get_matricula(self) -> 'Matricula':
        return self.__matricula

    def get_data(self) -> datetime.date:
        return self.__data
    
    def get_disciplinas(self) -> list:
        return self.__disciplinas
    
    def get_carga_horaria(self) -> float:
        return self.__carga_horaria
    
    def get_quantidade_creditos(self) -> int:
        return self.__quantidade_creditos
    
    def get_matricula_pd(self) -> list:
        return self.__matricula_pd
    
   
    #métodos
    
    def exibir_historico(self):
        
        # Acessa um ID do objeto Matrícula, assumindo que ele tenha um método get_id()
        matricula_ref = self.__matricula.get_id() if hasattr(self.__matricula, 'get_id') else "Objeto Matrícula não inicializado"
        
        # Cria a lista de nomes das disciplinas inscritas
        disciplinas_nomes = [d.get_nome() for d in self.__disciplinas if hasattr(d, 'get_nome')]
        disciplinas_str = ', '.join(disciplinas_nomes) if disciplinas_nomes else "Nenhuma disciplina"
        
        print(f"\n--- Histórico de Inscrição ---")
        print(f"Referência Matrícula: **{matricula_ref}**")
        print(f"Data de Inscrição: {self.__data.strftime('%d/%m/%Y')}")
        print(f"Carga Horária Total: {self.__carga_horaria:.1f}h")
        print(f"Créditos Totais: {self.__quantidade_creditos}")
        print(f"Disciplinas Inscritas ({len(self.__disciplinas)}): {disciplinas_str}")
        print(f"Registros Detalhados (MatriculaPD): {len(self.__matricula_pd)} itens")
        print("------------------------------\n")


    def adicionar_disciplina_e_registro(self, disciplina: 'Disciplina', registro_pd: 'MatriculaPagaDisciplina'):
        """
        Método 2: Adiciona uma nova disciplina e seu registro detalhado de MatrículaPagaDisciplina.
        Atualiza a carga horária e os créditos totais agregados.
        """
        
        # 1. Adiciona a disciplina e atualiza os totais
        if disciplina not in self.__disciplinas:
            self.__disciplinas.append(disciplina)
            
            # Tenta atualizar os totais: verifica se a Disciplina tem os getters
            if hasattr(disciplina, 'get_carga_horaria'):
                self.__carga_horaria += disciplina.get_carga_horaria()
            if hasattr(disciplina, 'get_creditos'):
                self.__quantidade_creditos += disciplina.get_creditos()
            
            nome_disc = disciplina.get_nome() if hasattr(disciplina, 'get_nome') else 'Nova'
            print(f"Disciplina '{nome_disc}' adicionada. Totais atualizados.")
        else:
            print(f"Disciplina já está inscrita neste Histórico.")
        
        # 2. Adiciona o registro detalhado
        self.__matricula_pd.append(registro_pd)
        print("Registro detalhado (MatriculaPD) adicionado.")