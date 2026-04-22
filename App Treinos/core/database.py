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
        """Conecta ao MySQL usando variáveis de ambiente."""
        try:
            self.connection = self.mysql_connector.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                user=os.environ.get("DB_USER", "root"),
                password=os.environ.get("DB_PASS", ""),
                database=os.environ.get("DB_NAME", "app_treinos"),
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

        # Tabela de atletas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atletas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trainer_cref TEXT NOT NULL,
                nome TEXT NOT NULL,
                cpf TEXT,
                email TEXT,
                genero TEXT,
                data_nascimento TEXT,
                peso_atual REAL,
                altura REAL,
                imc_atual REAL,
                esporte_principal TEXT,
                dias_disponibilidade_semana INTEGER,
                limiar_lactato REAL,
                vo2_max REAL,
                frequencia_cardiaca_repouso REAL,
                frequencia_cardiaca_maxima REAL,
                ciclo_menstrual_ativo INTEGER DEFAULT 0,
                problemas_saude TEXT,
                data_criacao TEXT NOT NULL,
                ultimo_atualizado TEXT NOT NULL,
                ativo INTEGER DEFAULT 1,
                UNIQUE(trainer_cref, cpf),
                FOREIGN KEY(trainer_cref) REFERENCES usuarios(cref)
            )
        ''')

        # Tabela de perfil do usuário (com dados encriptados)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                encrypted_cpf TEXT,
                encrypted_phone TEXT,
                birth_date TEXT,
                gender TEXT,
                profile_photo_path TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')

        # Índices para performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_atletas_trainer
            ON atletas(trainer_cref)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_atletas_nome
            ON atletas(nome)
        ''')

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

        # Tabela de atletas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atletas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                trainer_cref VARCHAR(20) NOT NULL,
                nome VARCHAR(255) NOT NULL,
                cpf VARCHAR(11),
                email VARCHAR(255),
                genero VARCHAR(20),
                data_nascimento DATE,
                peso_atual DECIMAL(5, 2),
                altura DECIMAL(5, 2),
                imc_atual DECIMAL(5, 2),
                esporte_principal VARCHAR(100),
                dias_disponibilidade_semana INT,
                limiar_lactato DECIMAL(6, 2),
                vo2_max DECIMAL(6, 2),
                frequencia_cardiaca_repouso DECIMAL(6, 2),
                frequencia_cardiaca_maxima DECIMAL(6, 2),
                ciclo_menstrual_ativo TINYINT DEFAULT 0,
                problemas_saude JSON,
                data_criacao DATETIME NOT NULL,
                ultimo_atualizado DATETIME NOT NULL,
                ativo TINYINT DEFAULT 1,
                UNIQUE(trainer_cref, cpf),
                FOREIGN KEY(trainer_cref) REFERENCES usuarios(cref),
                INDEX idx_atletas_trainer (trainer_cref),
                INDEX idx_atletas_nome (nome)
            )
        ''')

        # Tabela de perfil do usuário (com dados encriptados)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE NOT NULL,
                encrypted_cpf VARCHAR(500),
                encrypted_phone VARCHAR(500),
                birth_date DATE,
                gender VARCHAR(20),
                profile_photo_path VARCHAR(500),
                updated_at DATETIME NOT NULL,
                FOREIGN KEY(user_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        ''')

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
            usuario: CPF ou CREF do admin
            senha: Senha de acesso

        Returns:
            True se autenticado como admin
        """
        success, data = self.autenticar_usuario(usuario, senha)
        return success and data is not None and data.get("tipo") == "admin"

    def needs_initial_setup(self) -> bool:
        """Verifica se o sistema precisa de configuração inicial (sem utilizadores)."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM usuarios')
            count = cursor.fetchone()[0]
            conn.close()
            return count == 0
        except Exception:
            return True

    def criar_admin_inicial(self, cpf: str, cref: str, nome: str,
                            senha: str, email: str = "") -> Tuple[bool, str]:
        """Cria o primeiro administrador do sistema (apenas se não existir nenhum utilizador)."""
        if not self.needs_initial_setup():
            return False, "Sistema já possui utilizadores cadastrados."
        return self.cadastrar_usuario_com_tipo(cpf, cref, nome, senha, email, tipo="admin")
    
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

    def cadastrar_usuario_com_tipo(self, cpf: str, cref: str, nome: str,
                                   senha: str, email: str = "",
                                   tipo: str = "usuario") -> Tuple[bool, str]:
        """Cadastra utilizador com tipo específico (admin ou usuario)."""
        if not senha or len(senha.strip()) < 6:
            return False, "A senha deve ter no mínimo 6 caracteres."
        if not nome or len(nome.strip()) < 2:
            return False, "O nome deve ter no mínimo 2 caracteres."

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

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

            senha_hash = self._hash_password(senha)
            data_cadastro = datetime.now()

            if self.use_mysql:
                cursor.execute('''
                    INSERT INTO usuarios
                    (cpf, cref, nome, email, senha_hash, tipo, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (cpf, cref, nome, email, senha_hash, tipo, data_cadastro))
            else:
                cursor.execute('''
                    INSERT INTO usuarios
                    (cpf, cref, nome, email, senha_hash, tipo, data_cadastro)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (cpf, cref, nome, email, senha_hash, tipo,
                      data_cadastro.isoformat()))

            conn.commit()
            conn.close()
            return True, "Usuário cadastrado com sucesso!"

        except Exception as e:
            return False, f"Erro ao cadastrar: {str(e)}"

    # =====================================================================
    # ATLETAS - CRUD Methods
    # =====================================================================

    def create_athlete(self, trainer_cref: str, athlete_data: dict) -> int:
        """
        Cria novo atleta para um treinador.

        Args:
            trainer_cref: CREF do treinador
            athlete_data: Dicionário com dados do atleta
                - nome (obrigatório): str
                - cpf: str
                - email: str
                - genero: str ('masculino', 'feminino', 'outro')
                - data_nascimento: str (ISO date)
                - peso_atual: float (kg)
                - altura: float (cm)
                - imc_atual: float
                - esporte_principal: str
                - dias_disponibilidade_semana: int (1-7)
                - limiar_lactato: float
                - vo2_max: float
                - frequencia_cardiaca_repouso: float
                - frequencia_cardiaca_maxima: float
                - ciclo_menstrual_ativo: bool
                - problemas_saude: str (JSON)

        Returns:
            ID do atleta criado, ou -1 se falho
        """
        import json

        try:
            if not athlete_data.get('nome'):
                raise ValueError("Nome do atleta é obrigatório")

            conn = self._get_connection()
            cursor = conn.cursor()

            agora = datetime.now().isoformat()

            # Preparar dados com valores padrão
            dados = {
                'trainer_cref': trainer_cref,
                'nome': athlete_data.get('nome'),
                'cpf': athlete_data.get('cpf'),
                'email': athlete_data.get('email'),
                'genero': athlete_data.get('genero'),
                'data_nascimento': athlete_data.get('data_nascimento'),
                'peso_atual': athlete_data.get('peso_atual'),
                'altura': athlete_data.get('altura'),
                'imc_atual': athlete_data.get('imc_atual'),
                'esporte_principal': athlete_data.get('esporte_principal'),
                'dias_disponibilidade_semana': athlete_data.get('dias_disponibilidade_semana'),
                'limiar_lactato': athlete_data.get('limiar_lactato'),
                'vo2_max': athlete_data.get('vo2_max'),
                'frequencia_cardiaca_repouso': athlete_data.get('frequencia_cardiaca_repouso'),
                'frequencia_cardiaca_maxima': athlete_data.get('frequencia_cardiaca_maxima'),
                'ciclo_menstrual_ativo': 1 if athlete_data.get('ciclo_menstrual_ativo') else 0,
                'problemas_saude': json.dumps(athlete_data.get('problemas_saude', [])) if athlete_data.get('problemas_saude') else None,
                'data_criacao': agora,
                'ultimo_atualizado': agora,
                'ativo': 1
            }

            if self.use_mysql:
                campos = ', '.join(dados.keys())
                placeholders = ', '.join(['%s'] * len(dados))
                cursor.execute(
                    f'INSERT INTO atletas ({campos}) VALUES ({placeholders})',
                    tuple(dados.values())
                )
            else:
                campos = ', '.join(dados.keys())
                placeholders = ', '.join(['?'] * len(dados))
                cursor.execute(
                    f'INSERT INTO atletas ({campos}) VALUES ({placeholders})',
                    tuple(dados.values())
                )

            conn.commit()
            athlete_id = cursor.lastrowid
            conn.close()

            return athlete_id

        except Exception as e:
            print(f"[ERROR] Erro ao criar atleta: {e}")
            return -1

    def get_athlete(self, athlete_id: int) -> Optional[Dict]:
        """
        Recupera dados completos de um atleta.

        Args:
            athlete_id: ID do atleta

        Returns:
            Dicionário com dados do atleta, ou None se não encontrado
        """
        import json

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if self.use_mysql:
                cursor.execute('SELECT * FROM atletas WHERE id = %s AND ativo = 1', (athlete_id,))
            else:
                cursor.execute('SELECT * FROM atletas WHERE id = ? AND ativo = 1', (athlete_id,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            # Converter row em dicionário
            colnames = [
                'id', 'trainer_cref', 'nome', 'cpf', 'email', 'genero',
                'data_nascimento', 'peso_atual', 'altura', 'imc_atual',
                'esporte_principal', 'dias_disponibilidade_semana',
                'limiar_lactato', 'vo2_max', 'frequencia_cardiaca_repouso',
                'frequencia_cardiaca_maxima', 'ciclo_menstrual_ativo',
                'problemas_saude', 'data_criacao', 'ultimo_atualizado', 'ativo'
            ]

            atleta = dict(zip(colnames, row))

            # Parse JSON campos
            if atleta.get('problemas_saude'):
                try:
                    atleta['problemas_saude'] = json.loads(atleta['problemas_saude'])
                except:
                    atleta['problemas_saude'] = []

            return atleta

        except Exception as e:
            print(f"[ERROR] Erro ao recuperar atleta: {e}")
            return None

    def get_athletes_by_trainer(self, trainer_cref: str) -> List[Dict]:
        """
        Lista todos os atletas de um treinador.

        Args:
            trainer_cref: CREF do treinador

        Returns:
            Lista de dicionários com dados dos atletas
        """
        import json

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if self.use_mysql:
                cursor.execute(
                    'SELECT * FROM atletas WHERE trainer_cref = %s AND ativo = 1 ORDER BY nome',
                    (trainer_cref,)
                )
            else:
                cursor.execute(
                    'SELECT * FROM atletas WHERE trainer_cref = ? AND ativo = 1 ORDER BY nome',
                    (trainer_cref,)
                )

            rows = cursor.fetchall()
            conn.close()

            colnames = [
                'id', 'trainer_cref', 'nome', 'cpf', 'email', 'genero',
                'data_nascimento', 'peso_atual', 'altura', 'imc_atual',
                'esporte_principal', 'dias_disponibilidade_semana',
                'limiar_lactato', 'vo2_max', 'frequencia_cardiaca_repouso',
                'frequencia_cardiaca_maxima', 'ciclo_menstrual_ativo',
                'problemas_saude', 'data_criacao', 'ultimo_atualizado', 'ativo'
            ]

            atletas = []
            for row in rows:
                atleta = dict(zip(colnames, row))
                if atleta.get('problemas_saude'):
                    try:
                        atleta['problemas_saude'] = json.loads(atleta['problemas_saude'])
                    except:
                        atleta['problemas_saude'] = []
                atletas.append(atleta)

            return atletas

        except Exception as e:
            print(f"[ERROR] Erro ao listar atletas: {e}")
            return []

    def update_athlete(self, athlete_id: int, data: dict) -> bool:
        """
        Atualiza dados de um atleta.

        Args:
            athlete_id: ID do atleta
            data: Dicionário com campos a atualizar

        Returns:
            True se atualizado com sucesso
        """
        import json

        try:
            # Whitelist de campos permitidos
            _CAMPOS_PERMITIDOS = frozenset({
                'nome', 'cpf', 'email', 'genero', 'data_nascimento',
                'peso_atual', 'altura', 'imc_atual', 'esporte_principal',
                'dias_disponibilidade_semana', 'limiar_lactato', 'vo2_max',
                'frequencia_cardiaca_repouso', 'frequencia_cardiaca_maxima',
                'ciclo_menstrual_ativo', 'problemas_saude', 'ativo'
            })

            campos = []
            valores = []

            for campo, valor in data.items():
                if campo in _CAMPOS_PERMITIDOS:
                    if campo == 'ciclo_menstrual_ativo':
                        valor = 1 if valor else 0
                    elif campo == 'problemas_saude' and isinstance(valor, (list, dict)):
                        valor = json.dumps(valor)

                    if self.use_mysql:
                        campos.append(f"{campo} = %s")
                    else:
                        campos.append(f"{campo} = ?")
                    valores.append(valor)

            if not campos:
                return False

            # Adicionar timestamp de atualização
            agora = datetime.now().isoformat()
            if self.use_mysql:
                campos.append("ultimo_atualizado = %s")
            else:
                campos.append("ultimo_atualizado = ?")
            valores.append(agora)
            valores.append(athlete_id)

            conn = self._get_connection()
            cursor = conn.cursor()

            if self.use_mysql:
                query = f"UPDATE atletas SET {', '.join(campos)} WHERE id = %s"
            else:
                query = f"UPDATE atletas SET {', '.join(campos)} WHERE id = ?"

            cursor.execute(query, valores)
            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"[ERROR] Erro ao atualizar atleta: {e}")
            return False

    def delete_athlete(self, athlete_id: int) -> bool:
        """
        Marca atleta como inativo (soft delete).

        Args:
            athlete_id: ID do atleta

        Returns:
            True se deletado com sucesso
        """
        return self.update_athlete(athlete_id, {'ativo': 0})

    def get_athlete_metrics_history(self, athlete_id: int) -> List[Dict]:
        """
        Retorna histórico de métricas do atleta (peso, VO2, etc.).

        NOTA: Versão atual retorna apenas o registro atual.
        Em futuras versões, pode-se criar tabela separada para histórico.

        Args:
            athlete_id: ID do atleta

        Returns:
            Lista com histórico de métricas
        """
        atleta = self.get_athlete(athlete_id)

        if not atleta:
            return []

        # Retornar snapshot atual
        return [{
            'timestamp': atleta.get('ultimo_atualizado'),
            'peso': atleta.get('peso_atual'),
            'vo2_max': atleta.get('vo2_max'),
            'frequencia_cardiaca_repouso': atleta.get('frequencia_cardiaca_repouso'),
            'frequencia_cardiaca_maxima': atleta.get('frequencia_cardiaca_maxima'),
            'limiar_lactato': atleta.get('limiar_lactato'),
            'imc': atleta.get('imc_atual')
        }]

    # ── Gestão de Perfil do Usuário (com encriptação) ───────────────

    def create_default_profile(self, user_id: int) -> bool:
        """
        Cria um perfil vazio para um novo utilizador.

        Args:
            user_id: ID do utilizador

        Returns:
            True se criado, False se erro
        """
        from datetime import datetime

        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO user_profiles (user_id, updated_at)
                       VALUES (?, ?)''',
                    (user_id, datetime.now().isoformat())
                )
                conn.commit()
                conn.close()
            else:
                self.connection.cursor().execute(
                    '''INSERT INTO user_profiles (user_id, updated_at)
                       VALUES (%s, %s)''',
                    (user_id, datetime.now().isoformat())
                )
                self.connection.commit()
            return True
        except Exception:
            return False

    def get_user_profile(self, user_id: int) -> dict:
        """
        Obtém perfil do utilizador (com dados ainda encriptados).

        Args:
            user_id: ID do utilizador

        Returns:
            Dicionário com dados do perfil ou {} se não existe
        """
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT id, user_id, encrypted_cpf, encrypted_phone,
                             birth_date, gender, profile_photo_path, updated_at
                       FROM user_profiles WHERE user_id = ?''',
                    (user_id,)
                )
                row = cursor.fetchone()
                conn.close()
            else:
                cursor = self.connection.cursor()
                cursor.execute(
                    '''SELECT id, user_id, encrypted_cpf, encrypted_phone,
                             birth_date, gender, profile_photo_path, updated_at
                       FROM user_profiles WHERE user_id = %s''',
                    (user_id,)
                )
                row = cursor.fetchone()

            if not row:
                return {}

            return {
                'id': row[0],
                'user_id': row[1],
                'encrypted_cpf': row[2],
                'encrypted_phone': row[3],
                'birth_date': row[4],
                'gender': row[5],
                'profile_photo_path': row[6],
                'updated_at': row[7],
            }
        except Exception:
            return {}

    def update_user_profile(self, user_id: int, profile_data: dict) -> tuple:
        """
        Atualiza perfil do utilizador com dados encriptados.

        Args:
            user_id: ID do utilizador
            profile_data: Dicionário com dados (pode incluir encrypted_cpf, encrypted_phone, etc.)

        Returns:
            (success: bool, message: str)
        """
        from datetime import datetime

        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                # Construir UPDATE dinamicamente baseado nos campos fornecidos
                update_fields = []
                update_values = []

                for field in ['encrypted_cpf', 'encrypted_phone', 'birth_date', 'gender', 'profile_photo_path']:
                    if field in profile_data:
                        update_fields.append(f"{field} = ?")
                        update_values.append(profile_data[field])

                if update_fields:
                    update_fields.append("updated_at = ?")
                    update_values.append(datetime.now().isoformat())
                    update_values.append(user_id)

                    sql = f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = ?"
                    cursor.execute(sql, tuple(update_values))
                    conn.commit()

                conn.close()
            else:
                cursor = self.connection.cursor()
                update_fields = []
                update_values = []

                for field in ['encrypted_cpf', 'encrypted_phone', 'birth_date', 'gender', 'profile_photo_path']:
                    if field in profile_data:
                        update_fields.append(f"{field} = %s")
                        update_values.append(profile_data[field])

                if update_fields:
                    update_fields.append("updated_at = %s")
                    update_values.append(datetime.now().isoformat())
                    update_values.append(user_id)

                    sql = f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = %s"
                    cursor.execute(sql, tuple(update_values))
                    self.connection.commit()

            return (True, "Perfil atualizado com sucesso")
        except Exception as e:
            return (False, f"Erro ao atualizar perfil: {str(e)[:100]}")


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
