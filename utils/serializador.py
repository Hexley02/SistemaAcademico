import datetime
from models.aluno import Aluno 
from models.curso import Curso
from models.disciplina import Disciplina
from models.historicoacademico import HistoricoAcademico
from models.matricula import Matricula
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.professor import Professor
from models.pessoa import Pessoa
from models.historicoacademico import HistoricoAcademico

def serealizar_aluno(aluno: Aluno) -> dict:
    dados = serializar_pessoa(aluno)

    dados["matricula"] = aluno.get_matricula()
    dados["periodo_atual"] = aluno.get_periodo_atual()
    dados["email_institucional"] = aluno.get_email_institucional()
    dados["creditos_concluidos"] = aluno.get_creditos_concluidos()
    #salvamos apenas o código\id do curso não o objeto inteiro
    curso_obj = aluno.get_curso()

    if curso_obj and hasattr(curso_obj, "get_codigo"):
        dados["curso_codigo"] = curso_obj.get_codigo()
    else:
        dados["curso_codigo"] = None

    return dados

def serealizar_curso(curso: Curso) -> dict:

    codigos_disciplinas = []
    if curso.get_disciplinas():
        for disciplina in curso.get_disciplinas():
            if hasattr(disciplina, "get_codigo"):
                codigos_disciplinas.append(disciplina.get_codigo())

    return {
        "codigo": curso.get_codigo(),
        "periodo": curso.get_periodo(),
        "turno": curso.get_turno(),
        "avaliacao_curso": curso.get_avaliacao_curso(),
        "disciplinas_codigos": codigos_disciplinas
    }

def serealizar_disciplina(disciplina: Disciplina) -> dict:
    professor_id = None
    professor_obj = disciplina.get_professor_responsavel()

    if professor_obj:
        if hasattr(professor_obj, "get_codigo"):
            professor_id = professor_obj.get_codigo()
        else:
            professor_id = None
    
    alunos_matriculas = []
    if disciplina.get_alunos():
        for aluno in disciplina.get_alunos():
            if hasattr(aluno, 'get_matricula'):
                alunos_matriculas.append(aluno.get_matricula())
    return {
        "codigo": disciplina.get_codigo(),
        "nome": disciplina.get_nome(),
        "periodo": disciplina.get_periodo(),
        "professor_responsavel_id": professor_id,
        "alunos_matriculas": alunos_matriculas
    }

def serializar_historico(historico: HistoricoAcademico) -> dict:
    data_emissao_str = historico.get_data_emissao().isoformat()
    matricula_obj = historico.get_matricula_aluno()
    matricula_id = matricula_obj.get_id_matricula() if hasattr(matricula_obj, 'get_id_matricula') else matricula_obj.get_matricula()

    registros_serializados = []
    for registro in historico.get_registros_disciplinas():
        if hasattr(registro, 'to_dict'):
            registros_serializados.append(registro.to_dict())
        
    return {
        'matricula_aluno_id': matricula_id,
        'data_emissao': data_emissao_str,
        'quantidade_creditos': historico.get_quantidade_creditos(),
        'lista_atividades_complementares': historico.get_lista_atividades_complementares(),
        'registros_disciplinas': registros_serializados # Lista de dicionários (MPDs)
    }

def serializar_matricula(matricula: Matricula) -> dict:
    aluno_obj = matricula.get_aluno()
    aluno_matricula_id = aluno_obj.get_matricula() if hasattr(aluno_obj, "get_matricula")else None
    
    historico_obj = matricula.get_historico_academico()
    historico_id = matricula.get_id_matricula() 
    
   
    registros_serializados = [] 
    for registro in matricula.get_registros_disciplinas():
        if hasattr(registro, 'to_dict'):
            registros_serializados.append(registro.to_dict())
        
    return {
        'id_matricula': matricula.get_id_matricula(),
        'status': matricula.get_status(),
        'aluno_matricula_id': aluno_matricula_id,
        'historico_academico_id': historico_id, 
        'registros_disciplinas': registros_serializados
    }

def serializar_matricula_paga_disciplina(mpd: MatriculaPagaDisciplina) -> dict:
    id_mpd =id(mpd)
   
    matricula_obj = mpd.get_matricula()
    matricula_id = matricula_obj.get_id_matricula() if hasattr(matricula_obj, 'get_id_matricula') else None

    disciplina_obj = mpd.get_disciplina()
    disciplina_id = disciplina_obj.get_codigo() if hasattr(disciplina_obj, 'get_codigo') else None
    
    historico_obj = mpd.get_historico_acad()
    historico_id = historico_obj.get_matricula_aluno().get_id_matricula() \
                   if (historico_obj and hasattr(historico_obj, 'get_matricula_aluno')) else None
    
    return {
        'id_mpd': id_mpd,
        'matricula_id': matricula_id,
        'disciplina_id': disciplina_id,
        'historico_id': historico_id,
        'notas': mpd.get_notas(),      
        'faltas': mpd.get_faltas(),
        'media_final': mpd.get_media_final(),
        'nota_final': mpd.get_nota_final()
    }

def serializar_pessoa(pessoa: Pessoa) -> dict:
    
    data_nascimento_str = pessoa.get_data_nascimento().isoformat()
    
    return {
        'nome': pessoa.get_nome(),
        'email': pessoa.get_email(),
        'data_nascimento': data_nascimento_str,
        'telefone': pessoa.get_telefone(),
        'endereco': pessoa.get_endereco()
    }

def serializar_professor(professor: Professor) -> dict:
    
    dados = serializar_pessoa(professor) 
    
    dados['codigo'] = professor.get_codigo()
    dados['departamento'] = professor.get_departamento()
    dados['email_institucional'] = professor.get_email_institucional()
    dados['titulo'] = professor.get_titulo()
    
  
    codigos_disciplinas = []
    
    if professor.get_disciplinas():
        for disciplina in professor.get_disciplinas():
            if hasattr(disciplina, 'get_codigo'):
                codigos_disciplinas.append(disciplina.get_codigo())
            
    dados['disciplinas_codigos'] = codigos_disciplinas
    
    return dados
