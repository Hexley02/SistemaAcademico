# utils/desserializar.py
# versão iniciante, simples e 100% compatível com o projeto

from models.aluno import Aluno
from models.curso import Curso
from models.disciplina import Disciplina
from models.professor import Professor
from models.pessoa import Pessoa
from models.matricula import Matricula
from models.matriculapagadisciplina import MatriculaPagaDisciplina
from models.historicoacademico import HistoricoAcademico
import datetime



def desserializar_pessoa(dados: dict) -> Pessoa:
    data = datetime.date.fromisoformat(dados["data_nascimento"])
    pessoa = Pessoa(
        nome=dados["nome"],
        email=dados["email"],
        data_nascimento=data,
        telefone=dados["telefone"],
        endereco=dados["endereco"]
    )
    return pessoa


def desserializar_professor(dados: dict) -> Professor:
    pessoa = desserializar_pessoa(dados)

    prof = Professor(
        nome=pessoa.get_nome(),
        email=pessoa.get_email(),
        data_nascimento=pessoa.get_data_nascimento(),
        telefone=pessoa.get_telefone(),
        endereco=pessoa.get_endereco(),
        codigo=dados["codigo"],
        departamento=dados["departamento"],
        email_institucional=dados["email_institucional"],
        titulo=dados["titulo"]
    )

    # ainda sem disciplinas
    prof.disciplinas = []
    prof._disciplinas_codigos = dados.get("disciplinas_codigos", [])

    return prof


def desserializar_curso(dados: dict) -> Curso:

    curso = Curso(
        codigo=dados["codigo"],
        periodo=dados["periodo"],
        turno=dados["turno"],
        avaliacao_curso=dados["avaliacao_curso"],
        disciplinas=[]  # ligamos depois
    )

    curso._disciplinas_codigos = dados.get("disciplinas_codigos", [])

    return curso


def desserializar_disciplina(dados: dict) -> Disciplina:

    disc = Disciplina(
        codigo=dados["codigo"],
        nome=dados["nome"],
        periodo=dados["periodo"],
        professor_responsavel=None,  # liga depois
        alunos=[]
    )

    disc._prof_id = dados.get("professor_responsavel_id", None)
    disc._alunos_matriculas = dados.get("alunos_matriculas", [])

    return disc


def desserializar_aluno(dados: dict) -> Aluno:
    pessoa = desserializar_pessoa(dados)

    aluno = Aluno(
        nome=pessoa.get_nome(),
        email=pessoa.get_email(),
        data_nascimento=pessoa.get_data_nascimento(),
        telefone=pessoa.get_telefone(),
        endereco=pessoa.get_endereco(),
        matricula=dados["matricula"],
        periodo_atual=dados["periodo_atual"],
        email_institucional=dados["email_institucional"],
        curso=None,
        creditos_concluidos=dados["creditos_concluidos"]
    )

    aluno._curso_codigo = dados.get("curso_codigo", None)

    return aluno


def desserializar_historico(dados: dict) -> HistoricoAcademico:

    data = datetime.date.fromisoformat(dados["data_emissao"])

    hist = HistoricoAcademico(
        matricula_aluno=None,  # liga depois
        data_emissao=data
    )

    hist.quantidade_creditos = dados.get("quantidade_creditos", 0)
    hist.lista_atividades_complementares = dados.get(
        "lista_atividades_complementares", [])

    hist._registros_json = dados.get("registros_disciplinas", [])

    return hist


def desserializar_matricula(dados: dict) -> Matricula:

    mat = Matricula(
        id_matricula=dados["id_matricula"],
        aluno=None,  # liga depois
        historico_academico=None,  # liga depois
        status=dados["status"],
        registros_disciplinas=[]
    )

    mat._aluno_matricula_id = dados.get("aluno_matricula_id")
    mat._historico_id = dados.get("historico_academico_id")
    mat._registros_json = dados.get("registros_disciplinas", [])

    return mat


def desserializar_mpd(dados: dict) -> MatriculaPagaDisciplina:
    mpd = MatriculaPagaDisciplina(
        matricula=None,
        disciplina=None,
        notas=dados["notas"],
        faltas=dados["faltas"]
    )

    mpd.media_final = dados["media_final"]

    mpd._mat_id = dados["matricula_id"]
    mpd._disc_id = dados["disciplina_id"]
    mpd._hist_id = dados["historico_id"]

    return mpd


def ligar_objetos(alunos, cursos, disciplinas, professores, matriculas, historicos, mpds):

    # ligar aluno → curso
    for aluno in alunos.values():
        cod = aluno._curso_codigo
        if cod in cursos:
            aluno.set_curso(cursos[cod])

    # ligar curso → disciplinas
    for curso in cursos.values():
        lista = []
        for cod in curso._disciplinas_codigos:
            if cod in disciplinas:
                lista.append(disciplinas[cod])
        curso.disciplinas = lista

    # ligar disciplina → professor + alunos
    for disc in disciplinas.values():

        # professor
        if disc._prof_id in professores:
            disc.professor_responsavel = professores[disc._prof_id]

        # alunos matriculados
        alunos_lista = []
        for mat in disc._alunos_matriculas:
            if mat in alunos:
                alunos_lista.append(alunos[mat])
        disc.alunos = alunos_lista

    # ligar professor → disciplinas
    for prof in professores.values():
        lista = []
        for cod in prof._disciplinas_codigos:
            if cod in disciplinas:
                lista.append(disciplinas[cod])
        prof.disciplinas = lista

    # ligar histórico → matricula
    for hist in historicos.values():
        for mat_id, mat in matriculas.items():
            if mat_id == hist.get_matricula_aluno_id():
                hist.matricula_aluno = mat

    # ligar matricula → aluno e histórico
    for mat in matriculas.values():
        if mat._aluno_matricula_id in alunos:
            mat.aluno = alunos[mat._aluno_matricula_id]
        if mat._historico_id in historicos:
            mat.historico_academico = historicos[mat._historico_id]

    # ligar MPDs
    for mpd in mpds.values():
        if mpd._mat_id in matriculas:
            mpd.matricula = matriculas[mpd._mat_id]
        if mpd._disc_id in disciplinas:
            mpd.disciplina = disciplinas[mpd._disc_id]

#  FUNÇÃO FINAL – CARREGA TUDO A PARTIR DO JSON

def carregar_tudo(
        alunos_json,
        cursos_json,
        disciplinas_json,
        professores_json,
        matriculas_json,
        historicos_json,
        mpds_json
):

    alunos = {}
    cursos = {}
    disciplinas = {}
    professores = {}
    matriculas = {}
    historicos = {}
    mpds = {}

    # criar objetos sem ligação
    for d in cursos_json:
        c = desserializar_curso(d)
        cursos[c.get_codigo()] = c

    for d in disciplinas_json:
        disc = desserializar_disciplina(d)
        disciplinas[disc.get_codigo()] = disc

    for d in professores_json:
        p = desserializar_professor(d)
        professores[p.get_codigo()] = p

    for d in alunos_json:
        a = desserializar_aluno(d)
        alunos[a.get_matricula()] = a

    for d in historicos_json:
        h = desserializar_historico(d)
        historicos[h.get_id()] = h

    for d in matriculas_json:
        m = desserializar_matricula(d)
        matriculas[m.get_id_matricula()] = m

    for d in mpds_json:
        obj = desserializar_mpd(d)
        mpds[id(obj)] = obj  # MPDs não têm ID próprio

    # agora ligar tudo
    ligar_objetos(alunos, cursos, disciplinas, professores,
                  matriculas, historicos, mpds)

    return alunos, cursos, disciplinas, professores, matriculas, historicos, mpds
