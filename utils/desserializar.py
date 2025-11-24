
from models.aluno import Aluno 
from models.curso import Curso
from models.disciplina import Disciplina
from models.historicoacademico import HistoricoAcademico
from models.matricula import Matricula
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.professor import Professor
from models.pessoa import Pessoa
from models.historicoacademico import HistoricoAcademico
from typing import Dict, Any, List


def desserializar_aluno(dados_json: dict) -> Aluno:
    dados_pessoa = desserializar_pessoa(dados_json) 
    
    matricula = dados_json['matricula']
    periodo_atual = dados_json['periodo_atual']
    email_institucional = dados_json['email_institucional']
    creditos_concluidos = dados_json['creditos_concluidos']
    curso_codigo = dados_json.get('curso_codigo', None)
    
    
    aluno = Aluno(
        nome=dados_pessoa.get_nome(),
        email=dados_pessoa.get_email(), 
        data_nascimento=dados_pessoa.get_data_nascimento(),
        telefone=dados_pessoa.get_telefone(),
        endereco=dados_pessoa.get_endereco(),
        matricula=matricula,
        periodo_atual=periodo_atual,
        email_institucional=email_institucional,
        curso=None, # Objeto 'Curso' é None por enquanto
        creditos_concluidos=creditos_concluidos
    )
  
    return aluno

def desserializar_curso(dados_json: Dict[str, Any]) -> Curso:
    
    codigo = dados_json['codigo']
    periodo = dados_json['periodo']
    turno = dados_json['turno']
    avaliacao_curso = dados_json['avaliacao_curso']
    
    disciplinas_codigos: List[str] = dados_json.get('disciplinas_codigos', [])
    curso = Curso(
        codigo=codigo,
        disciplinas=[], # Inicializa como lista vazia, o SistemaAcademico ligará os objetos depois
        periodo=periodo,
        turno=turno,
        avaliacao_curso=avaliacao_curso
    )
    
    return curso