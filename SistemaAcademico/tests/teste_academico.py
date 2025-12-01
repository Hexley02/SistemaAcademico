import json
import os

# --- 1. Classes de Dados Mockup (Para Teste) ---

class Aluno:
    """Representa um Aluno no sistema acadêmico."""
    # CORRIGIDO: O construtor correto em Python
    def __init__(self, matricula, nome, nota=None):
        self.matricula = matricula
        self.nome = nome
        self.nota = nota if nota is not None else {} # Notas por disciplina

    def to_dict(self):
        """Converte o objeto Aluno para um dicionário serializável."""
        return {
            'matricula': self.matricula,
            'nome': self.nome,
            'notas': self.nota
        }

    @staticmethod
    def from_dict(data):
        """Cria um objeto Aluno a partir de um dicionário desserializado."""
        return Aluno(data['matricula'], data['nome'], data['notas'])

    # CORRIGIDO: O método de representação de string correto
    def __str__(self):
        return f"Aluno(Matrícula: {self.matricula}, Nome: {self.nome})"


# --- 2. Gerenciador de Dados (Mockup de Serialização) ---

class Serializador:
    """Responsável por converter objetos para JSON (serializar)."""
    def serialize(self, dados, filename):
        """Salva os dados (dicionário) em um arquivo JSON."""
        print(f"\n[SERIALIZADOR] Salvando dados em '{filename}'...")
        try:
            # Garante a criação do diretório (se necessário, para o mockup)
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4)
            print("[SERIALIZADOR] Dados salvos com sucesso.")
        except IOError as e:
            print(f"[ERRO SERIALIZAÇÃO] Não foi possível salvar o arquivo: {e}")

class Desserializador:
    """Responsável por carregar dados de um arquivo JSON (desserializar)."""
    def deserialize(self, filename):
        """Carrega dados de um arquivo JSON."""
        print(f"\n[DESSERIALIZADOR] Carregando dados de '{filename}'...")
        if not os.path.exists(filename):
            print("[DESSERIALIZADOR] Arquivo não encontrado. Retornando dados vazios.")
            return None
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            print("[DESSERIALIZADOR] Dados carregados com sucesso.")
            return dados
        except json.JSONDecodeError:
            print("[ERRO DESSERIALIZAÇÃO] Arquivo JSON corrompido ou mal formatado.")
            return None
        except IOError as e:
            print(f"[ERRO DESSERIALIZAÇÃO] Não foi possível ler o arquivo: {e}")
            return None

class GerenciadorDados:
    """
    Mockup de GerenciadorDados.
    ***CORRIGIDO***: Removido o argumento 'filename' do __init__ para resolver o TypeError.
    """
    def __init__(self):
        # Nome do arquivo fixo dentro da classe para não precisar do argumento
        self.filename = "dados_academicos_teste.json" 
        self.serializador = Serializador()
        self.desserializador = Desserializador()

    def salvar_sistema(self, sistema):
        """Serializa o estado do Sistema Acadêmico."""
        dados_alunos = [aluno.to_dict() for aluno in sistema.alunos.values()]
        dados = {'alunos': dados_alunos}
        self.serializador.serialize(dados, self.filename)

    def carregar_sistema(self, sistema):
        """Desserializa o estado e popula o Sistema Acadêmico."""
        dados = self.desserializador.deserialize(self.filename)
        if dados and 'alunos' in dados:
            sistema.alunos = {
                data['matricula']: Aluno.from_dict(data)
                for data in dados['alunos']
            }
            print("[GERENCIADOR] Sistema Acadêmico populado com sucesso.")
            return True
        return False


# --- 3. Sistema Acadêmico (Mockup para Teste) ---

class SistemaAcademico:
    """Contém a lógica de negócio principal."""
    # CORRIGIDO: O construtor correto em Python
    def __init__(self):
        self.alunos = {}
        print("\n[SISTEMA] Sistema Acadêmico Inicializado.")

    def adicionar_aluno(self, aluno):
        """Adiciona um novo aluno."""
        if aluno.matricula not in self.alunos:
            self.alunos[aluno.matricula] = aluno
            print(f"[SISTEMA] Aluno {aluno.nome} ({aluno.matricula}) adicionado.")
        else:
            print(f"[SISTEMA] Erro: Matrícula {aluno.matricula} já existe.")

    def exibir_alunos(self):
        """Exibe todos os alunos cadastrados."""
        print("\n--- Lista de Alunos no Sistema ---")
        if not self.alunos:
            print("Nenhum aluno cadastrado.")
            return
        for aluno in self.alunos.values():
            print(aluno)
        print("----------------------------------")


# --- 4. Script de Teste Principal ---

def rodar_teste_de_ciclo_de_vida():
    print("==============================================")
    print("  INÍCIO DO TESTE DE CICLO DE VIDA DO SISTEMA ")
    print("==============================================")
    
    # O FILENAME agora é definido internamente em GerenciadorDados
    
    # 1. TESTE DE SALVAMENTO (Serialização)
    print("\n\n=== FASE 1: CRIAÇÃO E SALVAMENTO DE DADOS NOVOS ===")
    
    # A. Inicializa o sistema (instância 1)
    sistema1 = SistemaAcademico()
    
    # CHAMADA CORRIGIDA: SEM ARGUMENTOS
    gerenciador = GerenciadorDados() 
    
    # B. Adiciona dados de teste
    aluno_a = Aluno("2024001", "Maria Silva")
    aluno_b = Aluno("2024002", "João Pereira")
    
    # Adicionando uma nota para testar
    aluno_a.nota['Programacao I'] = 9.5
    
    sistema1.adicionar_aluno(aluno_a)
    sistema1.adicionar_aluno(aluno_b)
    
    sistema1.exibir_alunos()
    
    # C. Salva o estado atual
    gerenciador.salvar_sistema(sistema1)
    
    
    # 2. TESTE DE CARREGAMENTO (Desserialização)
    print("\n\n=== FASE 2: CARREGAMENTO E VERIFICAÇÃO DE DADOS ===")
    
    # D. Cria uma nova instância do sistema (simulando uma reinicialização)
    print("\n[TESTE] Criando uma NOVA INSTÂNCIA do Sistema Acadêmico...")
    sistema2 = SistemaAcademico()
    
    # E. Tenta carregar os dados salvos
    gerenciador.carregar_sistema(sistema2)
    
    # F. Verifica se os dados foram restaurados
    sistema2.exibir_alunos()
    
    # G. Confirmação do Teste
    if "2024001" in sistema2.alunos and sistema2.alunos["2024001"].nome == "Maria Silva":
        print("\n[VERIFICAÇÃO] SUCESSO! Aluno 'Maria Silva' foi carregado corretamente.")
        if sistema2.alunos["2024001"].nota.get('Programacao I') == 9.5:
             print("[VERIFICAÇÃO] SUCESSO! A nota (9.5) foi preservada na serialização/desserialização.")
        else:
             print("[VERIFICAÇÃO] FALHA! A nota do aluno não foi carregada corretamente.")
    else:
        print("\n[VERIFICAÇÃO] FALHA! O aluno não foi encontrado ou os dados estão incorretos.")

    print("\n==============================================")
    print("  FIM DO TESTE ")
    print("==============================================")

if __name__ == "__main__":
    rodar_teste_de_ciclo_de_vida()