# POLITICA DE PRIVACIDADE — Velix

**Ultima atualizacao:** 14/04/2026

Esta Politica de Privacidade descreve como o Velix ("Software") coleta, armazena e utiliza dados pessoais.

---

## 1. Dados Coletados

### 1.1 Dados do Profissional
- CPF (usado como identificador de login)
- CREF (registro profissional)
- Nome completo
- Email (opcional)
- Senha (armazenada como hash PBKDF2-SHA256, nunca em texto claro)

### 1.2 Dados dos Atletas
- Nome e dados de identificacao
- Planos de treino e periodizacoes
- Informacoes de saude (condicoes ortopedicas, ciclo menstrual)
- Historico de progressao

### 1.3 Dados Tecnicos
- Preferencias de interface (idioma, tema)
- Configuracoes de IA (provedor selecionado, limites de tokens)
- Chaves de API de IA (armazenadas com criptografia AES/Fernet)

## 2. Armazenamento

Todos os dados sao armazenados **exclusivamente no computador do usuario**, em banco de dados SQLite local no diretorio do Software. **Nenhum dado e transmitido a servidores do Velix.**

Os dados de treino de cada profissional sao isolados pelo seu numero de CREF, impedindo acesso por outros utilizadores do mesmo computador.

## 3. Compartilhamento de Dados

O Velix **NAO compartilha dados pessoais** com terceiros, com as seguintes excecoes voluntarias:

### 3.1 Integracao com IA (opcional)
Quando o usuario ativa a funcionalidade de IA, dados de treino sao enviados ao provedor selecionado (OpenAI, Anthropic, Google Gemini ou DeepSeek) para processamento. O usuario e responsavel por:
- Avaliar a politica de privacidade do provedor escolhido
- Decidir quais dados incluir nas consultas de IA

### 3.2 Integracoes Externas (opcionais)
Dados de treino podem ser exportados para Strava ou Garmin Connect quando o usuario ativa estas integracoes.

## 4. Seguranca

- Senhas protegidas com PBKDF2-SHA256 (100.000 iteracoes + salt aleatorio)
- Chaves de API criptografadas com Fernet (AES-128-CBC + HMAC-SHA256)
- Dados isolados por profissional (CREF)

## 5. Direitos do Usuario

Em conformidade com a Lei Geral de Protecao de Dados (LGPD — Lei 13.709/2018), o usuario pode:
- **Acessar** todos os seus dados atraves do Software
- **Corrigir** dados incorretos via interface do Software
- **Excluir** sua conta e todos os dados associados
- **Exportar** seus planos de treino em formato Excel ou PDF

Como os dados sao armazenados localmente, o usuario tem controle total sobre eles, podendo apagar o banco de dados a qualquer momento.

## 6. Retencao de Dados

Os dados permanecem armazenados localmente enquanto o Software estiver instalado. Ao desinstalar o Software, os ficheiros de dados podem permanecer no computador ate que o usuario os apague manualmente.

## 7. Alteracoes nesta Politica

O autor reserva-se o direito de atualizar esta Politica de Privacidade. Alteracoes relevantes serao comunicadas atraves de notas de atualizacao do Software.

## 8. Contacto

Para questoes sobre esta politica ou sobre seus dados, entre em contacto pelo email indicado na secao "Sobre" do Software.

---

**Velix v3.1.0** — Planejador Inteligente de Treinos Esportivos
