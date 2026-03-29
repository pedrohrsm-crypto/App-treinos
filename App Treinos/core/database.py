"""
Sistema de Banco de Dados - App Treinos
========================================

Gerenciamento de usuários e autenticação.
Suporta SQLite (desenvolvimento) e MySQL (produção).
"""

import sqlite3
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple


class DatabaseManager:
    """Gerenciador de banco de dados para autenticação de usuários."""
    
    def __init__(self, db_path: Optional[str] = None, use_mysql: bool = False):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            db_path: Caminho para o arquivo SQLite (None = padrão)
            use_mysql: Se True, usa MySQL ao invés de SQLite
        """
        self.use_mysql = use_mysql
        
        if use_mysql:
            try:
                import mysql.connector
                self.mysql_connector = mysql.connector
                self.connection = None
                self._connect_mysql()
            except ImportError:
                print("⚠️ MySQL não instalado. Usando SQLite como fallback.")
                self.use_mysql = False
        
        if not self.use_mysql:
            if db_path is None:
                # Usar diretório data/ no projeto
                project_root = Path(__file__).parent.parent
                data_dir = project_root / "data"
                data_dir.mkdir(exist_ok=True)
                db_path = str(data_dir / "app_treinos.db")
            
            self.db_path = db_path
            self.connection = None
            self._init_sqlite_db()
    
    def _connect_mysql(self):
        """Conecta ao MySQL (configurações podem ser ajustadas)."""
        try:
            self.connection = self.mysql_connector.connect(
                host="localhost",
                user="root",
                password="",  # Ajustar conforme necessário
                database="app_treinos"
            )
            self._init_mysql_db()
        except Exception as e:
            print(f"❌ Erro ao conectar MySQL: {e}")
            raise
    
    def _init_sqlite_db(self):
        """Inicializa banco de dados SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE,
                cref TEXT UNIQUE,
                nome TEXT NOT NULL,
                email TEXT,
                senha_hash TEXT NOT NULL,
                tipo TEXT DEFAULT 'usuario',
                data_cadastro TEXT NOT NULL,
                ultimo_acesso TEXT,
                ativo INTEGER DEFAULT 1
            )
        ''')
        
        # Criar usuário administrador padrão se não existir
        cursor.execute('SELECT id FROM usuarios WHERE tipo = "admin"')
        if not cursor.fetchone():
            senha_hash = self._hash_password("adminDB")
            cursor.execute('''
                INSERT INTO usuarios (cpf, nome, email, senha_hash, tipo, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("00000000000", "Administrador", "admin@apptreinos.com", 
                  senha_hash, "admin", datetime.now().isoformat()))
            print("✅ Usuário administrador criado")
        
        conn.commit()
        conn.close()
    
    def _init_mysql_db(self):
        """Inicializa tabelas no MySQL."""
        cursor = self.connection.cursor()
        
        # Criar database se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS app_treinos")
        cursor.execute("USE app_treinos")
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cpf VARCHAR(11) UNIQUE,
                cref VARCHAR(20) UNIQUE,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                senha_hash VARCHAR(64) NOT NULL,
                tipo VARCHAR(20) DEFAULT 'usuario',
                data_cadastro DATETIME NOT NULL,
                ultimo_acesso DATETIME,
                ativo TINYINT DEFAULT 1
            )
        ''')
        
        # Criar admin se não existir
        cursor.execute('SELECT id FROM usuarios WHERE tipo = "admin"')
        if not cursor.fetchone():
            senha_hash = self._hash_password("adminDB")
            cursor.execute('''
                INSERT INTO usuarios (cpf, nome, email, senha_hash, tipo, data_cadastro)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', ("00000000000", "Administrador", "admin@apptreinos.com", 
                  senha_hash, "admin", datetime.now()))
        
        self.connection.commit()
    
    def _hash_password(self, password: str) -> str:
        """Gera hash PBKDF2-SHA256 com salt (ou SHA-256 legado para compatibilidade).

        Formato novo: 'pbkdf2$<salt_hex>$<hash_hex>'
        Formato legado: 64 caracteres hex (SHA-256 puro)
        """
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
        return f"pbkdf2${salt.hex()}${dk.hex()}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verifica senha contra hash armazenado (suporta PBKDF2 e SHA-256 legado)."""
        if stored_hash.startswith("pbkdf2$"):
            _, salt_hex, hash_hex = stored_hash.split("$", 2)
            salt = bytes.fromhex(salt_hex)
            dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
            return dk.hex() == hash_hex
        else:
            # Formato legado SHA-256
            return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    
    def _get_connection(self):
        """Retorna conexão ativa."""
        if self.use_mysql:
            return self.connection
        else:
            return sqlite3.connect(self.db_path)
    
    def cadastrar_usuario(self, cpf: str, cref: str, nome: str, 
                         senha: str, email: str = "") -> Tuple[bool, str]:
        """
        Cadastra novo usuário no sistema.
        
        Args:
            cpf: CPF do usuário (11 dígitos)
            cref: CREF do profissional
            nome: Nome completo
            senha: Senha para acesso
            email: Email (opcional)
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        # Validação de campos obrigatórios
        if not senha or len(senha.strip()) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres."
        if not nome or len(nome.strip()) < 2:
            return False, "O nome deve ter no mínimo 2 caracteres."

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Verificar se CPF ou CREF já existem
            if self.use_mysql:
                cursor.execute(
                    'SELECT id FROM usuarios WHERE cpf = %s OR cref = %s',
                    (cpf, cref)
                )
            else:
                cursor.execute(
                    'SELECT id FROM usuarios WHERE cpf = ? OR cref = ?',
                    (cpf, cref)
                )
            
            if cursor.fetchone():
                conn.close()
                return False, "CPF ou CREF já cadastrados no sistema."
            
            # Inserir novo usuário
            senha_hash = self._hash_password(senha)
            data_cadastro = datetime.now()
            
            if self.use_mysql:
                cursor.execute('''
                    INSERT INTO usuarios 
                    (cpf, cref, nome, email, senha_hash, tipo, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (cpf, cref, nome, email, senha_hash, "usuario", data_cadastro))
            else:
                cursor.execute('''
                    INSERT INTO usuarios 
                    (cpf, cref, nome, email, senha_hash, tipo, data_cadastro)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (cpf, cref, nome, email, senha_hash, "usuario", 
                      data_cadastro.isoformat()))
            
            conn.commit()
            conn.close()
            
            return True, "Usuário cadastrado com sucesso!"
        
        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"
    
    def autenticar_usuario(self, credencial: str, senha: str) -> Tuple[bool, Optional[Dict]]:
        """
        Autentica usuário por CPF ou CREF.

        Args:
            credencial: CPF ou CREF do usuário
            senha: Senha de acesso

        Returns:
            Tupla (sucesso, dados_usuario ou None)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Buscar utilizador pela credencial (verificação de senha em Python)
            if self.use_mysql:
                cursor.execute('''
                    SELECT id, cpf, cref, nome, email, tipo, ativo, senha_hash
                    FROM usuarios
                    WHERE (cpf = %s OR cref = %s) AND ativo = 1
                ''', (credencial, credencial))
            else:
                cursor.execute('''
                    SELECT id, cpf, cref, nome, email, tipo, ativo, senha_hash
                    FROM usuarios
                    WHERE (cpf = ? OR cref = ?) AND ativo = 1
                ''', (credencial, credencial))

            resultado = cursor.fetchone()

            if resultado and self._verify_password(senha, resultado[7]):
                # Atualizar último acesso
                user_id = resultado[0]
                if self.use_mysql:
                    cursor.execute(
                        'UPDATE usuarios SET ultimo_acesso = %s WHERE id = %s',
                        (datetime.now(), user_id)
                    )
                else:
                    cursor.execute(
                        'UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?',
                        (datetime.now().isoformat(), user_id)
                    )

                # Migrar hash legado (SHA-256) para PBKDF2 na primeira autenticação
                stored_hash = resultado[7]
                if not stored_hash.startswith("pbkdf2$"):
                    new_hash = self._hash_password(senha)
                    if self.use_mysql:
                        cursor.execute(
                            'UPDATE usuarios SET senha_hash = %s WHERE id = %s',
                            (new_hash, user_id)
                        )
                    else:
                        cursor.execute(
                            'UPDATE usuarios SET senha_hash = ? WHERE id = ?',
                            (new_hash, user_id)
                        )

                conn.commit()

                usuario = {
                    'id': resultado[0],
                    'cpf': resultado[1],
                    'cref': resultado[2],
                    'nome': resultado[3],
                    'email': resultado[4],
                    'tipo': resultado[5],
                    'ativo': resultado[6]
                }

                conn.close()
                return True, usuario

            conn.close()
            return False, None

        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False, None
    
    def autenticar_por_hash(self, credencial: str, senha_hash: str) -> Tuple[bool, Optional[Dict]]:
        """
        Autentica usuário por CPF ou CREF comparando hash armazenado.

        Usado pelo auto-login: o preferences.json guarda o hash completo
        da DB (PBKDF2 ou SHA-256 legado) e este método compara directamente.

        Args:
            credencial: CPF ou CREF do usuário
            senha_hash: Hash completo armazenado (PBKDF2 ou SHA-256 legado)

        Returns:
            Tupla (sucesso, dados_usuario ou None)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if self.use_mysql:
                cursor.execute('''
                    SELECT id, cpf, cref, nome, email, tipo, ativo, senha_hash
                    FROM usuarios
                    WHERE (cpf = %s OR cref = %s) AND ativo = 1
                ''', (credencial, credencial))
            else:
                cursor.execute('''
                    SELECT id, cpf, cref, nome, email, tipo, ativo, senha_hash
                    FROM usuarios
                    WHERE (cpf = ? OR cref = ?) AND ativo = 1
                ''', (credencial, credencial))

            resultado = cursor.fetchone()

            if resultado and resultado[7] == senha_hash:
                user_id = resultado[0]
                if self.use_mysql:
                    cursor.execute(
                        'UPDATE usuarios SET ultimo_acesso = %s WHERE id = %s',
                        (datetime.now(), user_id)
                    )
                else:
                    cursor.execute(
                        'UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?',
                        (datetime.now().isoformat(), user_id)
                    )
                conn.commit()

                usuario = {
                    'id': resultado[0],
                    'cpf': resultado[1],
                    'cref': resultado[2],
                    'nome': resultado[3],
                    'email': resultado[4],
                    'tipo': resultado[5],
                    'ativo': resultado[6]
                }

                conn.close()
                return True, usuario

            conn.close()
            return False, None

        except Exception as e:
            print(f"❌ Erro na autenticação por hash: {e}")
            return False, None

    def autenticar_admin(self, usuario: str, senha: str) -> bool:
        """
        Autentica acesso administrativo.
        
        Args:
            usuario: Nome de usuário (deve ser "admin")
            senha: Senha de acesso (deve ser "adminDB")
        
        Returns:
            True se autenticado
        """
        if usuario != "admin":
            return False
        
        return self.autenticar_usuario("00000000000", senha)[0]
    
    def listar_usuarios(self) -> List[Dict]:
        """Lista todos os usuários cadastrados (apenas admin)."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, cpf, cref, nome, email, tipo, data_cadastro, 
                       ultimo_acesso, ativo
                FROM usuarios
                WHERE tipo != 'admin'
                ORDER BY nome
            ''')
            
            usuarios = []
            for row in cursor.fetchall():
                usuarios.append({
                    'id': row[0],
                    'cpf': row[1],
                    'cref': row[2],
                    'nome': row[3],
                    'email': row[4],
                    'tipo': row[5],
                    'data_cadastro': row[6],
                    'ultimo_acesso': row[7],
                    'ativo': row[8]
                })
            
            conn.close()
            return usuarios
        
        except Exception as e:
            print(f"❌ Erro ao listar usuários: {e}")
            return []
    
    def atualizar_usuario(self, user_id: int, **kwargs) -> Tuple[bool, str]:
        """
        Atualiza dados de um usuário.
        
        Args:
            user_id: ID do usuário
            **kwargs: Campos a atualizar (nome, email, ativo, etc.)
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Whitelist estrita — apenas estes nomes de coluna são permitidos
            _CAMPOS_PERMITIDOS = frozenset({'nome', 'email', 'ativo', 'cpf', 'cref'})
            campos = []
            valores = []

            for campo, valor in kwargs.items():
                if campo in _CAMPOS_PERMITIDOS:
                    campos.append(f"{campo} = ?")
                    valores.append(valor)

            if not campos:
                return False, "Nenhum campo válido para atualizar"

            valores.append(user_id)
            query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?"
            
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            conn.close()
            
            return True, "Usuário atualizado com sucesso!"
        
        except Exception as e:
            return False, f"Erro ao atualizar: {str(e)}"
    
    def deletar_usuario(self, user_id: int) -> Tuple[bool, str]:
        """
        Desativa um usuário (soft delete).
        
        Args:
            user_id: ID do usuário
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        return self.atualizar_usuario(user_id, ativo=0)


# Instância global
db_manager = DatabaseManager()


def verificar_credencial_existe(credencial: str) -> bool:
    """Verifica se CPF ou CREF já está cadastrado."""
    try:
        conn = sqlite3.connect(db_manager.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM usuarios WHERE (cpf = ? OR cref = ?) AND ativo = 1',
            (credencial, credencial)
        )
        existe = cursor.fetchone() is not None
        conn.close()
        return existe
    except:
        return False
