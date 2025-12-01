# utils/desserializar.py
from models.aluno import Aluno
from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina
from models.matricula import Matricula
from models.historicoacademico import HistoricoAcademico
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.pessoa import Pessoa

import datetime
from typing import Dict, List, Tuple

# ============================================================
# FUNÇÕES DE DESSERIALIZAÇÃO SIMPLES
# ============================================================

def desserializar_pessoa(d: dict) -> Pessoa:
    p = Pessoa(
        d["nome"],
        d["email"],
        datetime.date.fromisoformat(d["data_nascimento"]),
        d["telefone"],
        d["endereco"]
    )
    return p


def desserializar_aluno(d: dict) -> Aluno:
    p = desserializar_pessoa(d)
    aluno = Aluno(
        p.get_nome(), p.get_email(), p.get_data_nascimento(),
        p.get_telefone(), p.get_endereco(),
        d["matricula"], d["periodo_atual"],
        d["email_institucional"], 
        None,  # curso será linkado depois
        d["creditos_concluidos"]
    )

    aluno._curso_codigo_temp = d["curso_codigo"]
    return aluno


def desserializar_professor(d: dict) -> Professor:
    p = desserializar_pessoa(d)
    prof = Professor(
        p.get_nome(), p.get_email(), p.get_data_nascimento(),
        p.get_telefone(), p.get_endereco(),
        d["codigo"], d["departamento"],
        [],  # disciplinas serão linkadas depois
        d["email_institucional"], d["titulo"]
    )
    prof._disciplinas_temp = d.get("disciplinas_codigos", [])
    return prof


def desserializar_curso(d: dict) -> Curso:
    c = Curso(
        d["codigo"], 
        [],  # disciplinas serão linkadas depois
        d["periodo"], 
        d["turno"], 
        d["avaliacao_curso"]
    )
    c._disciplinas_temp = d.get("disciplinas_codigos", [])
    return c


def desserializar_disciplina(d: dict) -> Disciplina:
    disc = Disciplina(
        d["codigo"], 
        d["periodo"],
        d["nome"], 
        None,  # professor será linkado depois
        []     # alunos serão linkados depois
    )
    disc._prof_temp = d.get("professor_responsavel_id")
    disc._alunos_temp = d.get("alunos_matriculas", [])
    return disc


def desserializar_historico(d: dict) -> HistoricoAcademico:
    h = HistoricoAcademico(
        matricula_aluno=None,  # será linkado depois
        data_emissao=datetime.date.today(),  # temporário
        quantidade_creditos=d["quantidade_creditos"],
        lista_atividades_complemetares=d["lista_atividades_complementares"],
        registros_disciplinas=None
    )

    h._matricula_temp = d["matricula_aluno_id"]
    h._registros_temp = d.get("registros_disciplinas", [])
    h._data_temp = d["data_emissao"]
    return h


def desserializar_matricula(d: dict) -> Matricula:
    m = Matricula(
        id_matricula=d["id_matricula"],
        aluno=None,  # será linkado depois
        historico_academico=None,  # será linkado depois
        status=d["status"],
        registros_disciplinas=None
    )

    m._aluno_temp = d["aluno_matricula_id"]
    m._historico_temp = d["historico_academico_id"]
    m._registros_temp = d.get("registros_disciplinas", [])
    return m


def desserializar_mpd(d: dict) -> MatriculaPagaDisciplina:
    mpd = MatriculaPagaDisciplina(
        matricula=None,  # será linkado depois
        disciplina=None,  # será linkado depois
        notas=[],  # temporário
        faltas=0,  # temporário
        historico_acad=None,  # será linkado depois
        nota_final=None
    )

    mpd._id_mpd = d["id_mpd"]
    mpd._matricula_temp = d["matricula_id"]
    mpd._disciplina_temp = d["disciplina_id"]
    mpd._historico_temp = d["historico_id"]

    mpd._notas_temp = d["notas"]
    mpd._faltas_temp = d["faltas"]
    mpd._media_temp = d["media_final"]
    mpd._nota_final_temp = d["nota_final"]
    return mpd


# ============================================================
# FUNÇÃO QUE RECONSTRÓI TODA A REDE DE OBJETOS
# ============================================================
def carregar_tudo(
    alunos_json: List[dict], 
    cursos_json: List[dict], 
    disciplinas_json: List[dict],
    professores_json: List[dict], 
    matriculas_json: List[dict],
    historicos_json: List[dict], 
    mpds_json: List[dict]
) -> Tuple[Dict[str, Aluno], Dict[str, Curso], Dict[str, Disciplina], 
           Dict[str, Professor], Dict[int, Matricula], Dict[str, HistoricoAcademico], 
           Dict[str, MatriculaPagaDisciplina]]:

    alunos: Dict[str, Aluno] = {}
    cursos: Dict[str, Curso] = {}
    disciplinas: Dict[str, Disciplina] = {}
    professores: Dict[str, Professor] = {}
    matriculas: Dict[int, Matricula] = {}
    historicos: Dict[str, HistoricoAcademico] = {}
    mpds: Dict[str, MatriculaPagaDisciplina] = {}

    # 1 — Criar objetos simples (sem ligações)
    for d in alunos_json:
        obj = desserializar_aluno(d)
        alunos[obj.get_matricula()] = obj

    for d in cursos_json:
        obj = desserializar_curso(d)
        cursos[obj.get_codigo()] = obj

    for d in disciplinas_json:
        obj = desserializar_disciplina(d)
        disciplinas[obj.get_codigo()] = obj

    for d in professores_json:
        obj = desserializar_professor(d)
        professores[obj.get_codigo()] = obj

    for d in matriculas_json:
        obj = desserializar_matricula(d)
        matriculas[obj.get_id_matricula()] = obj

    for d in historicos_json:
        obj = desserializar_historico(d)
        historicos[d["matricula_aluno_id"]] = obj

    for d in mpds_json:
        obj = desserializar_mpd(d)
        mpds[d["id_mpd"]] = obj

    # 2 — Ligar objetos
    for aluno in alunos.values():
        if hasattr(aluno, '_curso_codigo_temp') and aluno._curso_codigo_temp:
            curso = cursos.get(aluno._curso_codigo_temp)
            if curso:
                aluno._Aluno__curso = curso  # name mangling para atributo privado

    for curso in cursos.values():
        if hasattr(curso, '_disciplinas_temp'):
            curso._Curso__disciplinas = [
                disciplinas[codigo] for codigo in curso._disciplinas_temp
                if codigo in disciplinas
            ]

    for disciplina in disciplinas.values():
        if hasattr(disciplina, '_prof_temp') and disciplina._prof_temp:
            prof = professores.get(disciplina._prof_temp)
            if prof:
                disciplina.set_professor_responsavel(prof)

        if hasattr(disciplina, '_alunos_temp'):
            disciplina._Disciplina__alunos = [
                alunos[m] for m in disciplina._alunos_temp if m in alunos
            ]

    for historico in historicos.values():
        if hasattr(historico, '_matricula_temp'):
            historico._HistoricoAcademico__matricula_aluno = alunos.get(historico._matricula_temp)
        if hasattr(historico, '_data_temp'):
            historico._HistoricoAcademico__data_emissao = datetime.datetime.fromisoformat(historico._data_temp)

    for matricula in matriculas.values():
        if hasattr(matricula, '_aluno_temp'):
            matricula._Matricula__aluno = alunos.get(matricula._aluno_temp)
        if hasattr(matricula, '_historico_temp'):
            matricula._Matricula__historico_academico = historicos.get(matricula._historico_temp)

    for mpd in mpds.values():
        if hasattr(mpd, '_matricula_temp'):
            mpd._MatriculaPagaDisciplina__matricula = matriculas.get(mpd._matricula_temp)
        if hasattr(mpd, '_disciplina_temp'):
            mpd._MatriculaPagaDisciplina__disciplina = disciplinas.get(mpd._disciplina_temp)
        if hasattr(mpd, '_historico_temp'):
            mpd._MatriculaPagaDisciplina__historico_acad = historicos.get(mpd._historico_temp)

        if hasattr(mpd, '_notas_temp'):
            mpd._MatriculaPagaDisciplina__notas = mpd._notas_temp
        if hasattr(mpd, '_faltas_temp'):
            mpd._MatriculaPagaDisciplina__faltas = mpd._faltas_temp
        if hasattr(mpd, '_media_temp'):
            mpd._MatriculaPagaDisciplina__media_final = mpd._media_temp
        if hasattr(mpd, '_nota_final_temp'):
            mpd._MatriculaPagaDisciplina__nota_final = mpd._nota_final_temp

    return alunos, cursos, disciplinas, professores, matriculas, historicos, mpds