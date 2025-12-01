import json
import os
from typing import Dict, Any, Optional


class GerenciadorArquivos:
    def __init__(self, arquivos_dados: Dict[str, str]):
        """
        Inicializa com o caminho do arquivo principal, extraindo do dicionário.
        
        Args:
            arquivos_dados: Dicionário contendo os caminhos, ex: {'principal': 'path/to/file.json'}
            
        Raises:
            ValueError: Se a chave 'principal' não existir no dicionário
        """
        # Extrai o caminho da chave 'principal'
        self.caminho_arquivo = arquivos_dados.get('principal')
        
        if not self.caminho_arquivo:
            raise ValueError("O dicionário 'arquivos_dados' deve conter a chave 'principal' com um caminho válido.")
        
        # Garante que o diretório existe antes de tentar salvar
        self._verificar_diretorio()

    def _verificar_diretorio(self) -> None:
        """
        Verifica se o diretório para salvar o arquivo existe e o cria se necessário.
        """
        diretorio = os.path.dirname(self.caminho_arquivo)
        
        # Se houver um diretório especificado e ele não existir, cria-o
        if diretorio and not os.path.exists(diretorio):
            try:
                os.makedirs(diretorio, exist_ok=True)
                print(f"📁 Diretório criado: {diretorio}")
            except OSError as e:
                print(f"❌ ERRO: Falha ao criar o diretório {diretorio}. {e}")
                raise  # Re-raise para que o erro não seja silenciosamente ignorado

    def salvar(self, dados: Dict[str, Any]) -> bool:
        """
        Salva os dados no arquivo JSON.
        
        Args:
            dados: Dicionário com os dados a serem salvos
            
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        try:
            # Cria um backup do arquivo existente antes de sobrescrever
            self._criar_backup()
            
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                # ensure_ascii=False garante que caracteres acentuados funcionem
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
            print(f"💾 Dados salvos com sucesso em {self.caminho_arquivo}")
            return True
            
        except IOError as e:
            print(f"❌ ERRO: Não foi possível escrever no arquivo {self.caminho_arquivo}. {e}")
            return False
            
        except TypeError as e:
            print(f"❌ ERRO: Objeto inválido para serialização JSON. Verifique as funções de serialização. {e}")
            return False
            
        except Exception as e:
            print(f"❌ ERRO inesperado ao salvar: {e}")
            return False

    def carregar(self) -> Dict[str, Any]:
        """
        Carrega os dados do arquivo JSON.
        
        Returns:
            Dict com os dados carregados, ou dict vazio se houver erro
        """
        try:
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                print(f"📥 Dados carregados com sucesso de {self.caminho_arquivo}")
                return dados
                
        except FileNotFoundError:
            # Comum no primeiro uso - não é necessariamente um erro
            print(f"📝 Arquivo {self.caminho_arquivo} não encontrado. Sistema iniciará vazio.")
            return {}
            
        except json.JSONDecodeError as e:
            # Arquivo corrompido - tenta recuperar do backup
            print(f"⚠️  AVISO: Arquivo corrompido em {self.caminho_arquivo}. {e}")
            return self._tentar_recuperar_backup()
            
        except Exception as e:
            print(f"❌ ERRO inesperado ao carregar dados: {e}")
            return {}

    def _criar_backup(self) -> None:
        """
        Cria um backup do arquivo existente antes de sobrescrever.
        """
        if os.path.exists(self.caminho_arquivo):
            backup_path = f"{self.caminho_arquivo}.backup"
            try:
                import shutil
                shutil.copy2(self.caminho_arquivo, backup_path)
            except Exception as e:
                print(f"⚠️  Não foi possível criar backup: {e}")

    def _tentar_recuperar_backup(self) -> Dict[str, Any]:
        """
        Tenta recuperar dados do arquivo de backup.
        
        Returns:
            Dict com os dados do backup, ou dict vazio se falhar
        """
        backup_path = f"{self.caminho_arquivo}.backup"
        
        if not os.path.exists(backup_path):
            print("❌ Nenhum backup disponível.")
            return {}
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
                print(f"✅ Dados recuperados do backup!")
                return dados
        except Exception as e:
            print(f"❌ Falha ao recuperar backup: {e}")
            return {}

    def arquivo_existe(self) -> bool:
        """
        Verifica se o arquivo de dados existe.
        
        Returns:
            bool: True se o arquivo existe, False caso contrário
        """
        return os.path.exists(self.caminho_arquivo)

    def limpar_dados(self) -> bool:
        """
        Remove o arquivo de dados (use com cuidado!).
        
        Returns:
            bool: True se removeu com sucesso, False caso contrário
        """
        try:
            if self.arquivo_existe():
                os.remove(self.caminho_arquivo)
                print(f"🗑️  Arquivo {self.caminho_arquivo} removido com sucesso.")
                return True
            else:
                print(f"⚠️  Arquivo não existe: {self.caminho_arquivo}")
                return False
        except Exception as e:
            print(f"❌ Erro ao remover arquivo: {e}")
            return False