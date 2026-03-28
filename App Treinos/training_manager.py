"""
Sistema de Gerenciamento de Treinos por Profissional
====================================================

Gerencia treinos criados por profissionais de Educação Física,
garantindo que cada profissional acesse apenas seus próprios treinos.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import shutil


@dataclass
class TrainingRecord:
    """Registro de um treino criado."""
    id: str  # ID único do treino (timestamp)
    athlete_name: str
    athlete_data: Dict  # Dados completos do atleta
    sport: str
    distance: str
    weeks: int
    created_at: str
    excel_path: Optional[str] = None
    pdf_path: Optional[str] = None
    last_modified: Optional[str] = None
    
    def to_dict(self):
        """Converte para dicionário."""
        return asdict(self)


@dataclass
class ChangeLogEntry:
    """Entrada no histórico de alterações de um plano."""
    timestamp: str
    action: str       # 'created', 'updated', 'exported', 'deleted'
    details: str
    plan_id: Optional[str] = None

    def to_dict(self):
        return asdict(self)


class TrainingManager:
    """Gerenciador de treinos por profissional."""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Inicializa o gerenciador.
        
        Args:
            base_dir: Diretório base (padrão: data/trainers)
        """
        if base_dir is None:
            project_root = Path(__file__).parent
            self.base_dir = project_root / "data" / "trainers"
        else:
            self.base_dir = Path(base_dir)
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_trainer_id(self, trainer_info) -> str:
        """
        Obtém ID único do treinador (CREF normalizado).
        
        Args:
            trainer_info: Objeto TrainerInfo ou dicionário com 'cref'
        
        Returns:
            CREF normalizado (apenas números e letras)
        
        Raises:
            ValueError: Se trainer_info for None ou CREF estiver vazio
        """
        if trainer_info is None:
            raise ValueError("trainer_info não pode ser None")
        
        if hasattr(trainer_info, 'cref'):
            cref = trainer_info.cref
        elif isinstance(trainer_info, dict):
            cref = trainer_info.get('cref', '')
        else:
            cref = str(trainer_info)
        
        # Normalizar CREF (remover caracteres especiais)
        trainer_id = ''.join(filter(str.isalnum, cref))
        
        if not trainer_id:
            raise ValueError("CREF do treinador não pode ser vazio")
        
        return trainer_id
    
    def _get_trainer_dir(self, trainer_info) -> Path:
        """
        Obtém diretório do treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Path do diretório do treinador
        """
        trainer_id = self._get_trainer_id(trainer_info)
        trainer_dir = self.base_dir / trainer_id
        trainer_dir.mkdir(parents=True, exist_ok=True)
        return trainer_dir
    
    def _get_plans_dir(self, trainer_info) -> Path:
        """
        Obtém diretório de planos do treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Path do diretório de planos
        """
        trainer_dir = self._get_trainer_dir(trainer_info)
        plans_dir = trainer_dir / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)
        return plans_dir
    
    def _get_metadata_path(self, trainer_info) -> Path:
        """
        Obtém caminho do arquivo de metadados.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Path do arquivo metadata.json
        """
        trainer_dir = self._get_trainer_dir(trainer_info)
        return trainer_dir / "metadata.json"
    
    def _load_metadata(self, trainer_info) -> Dict:
        """
        Carrega metadados dos treinos do treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Dicionário com metadados
        """
        metadata_path = self._get_metadata_path(trainer_info)
        
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Erro ao carregar metadados: {e}")
                return {"plans": []}
        
        return {"plans": []}
    
    def _save_metadata(self, trainer_info, metadata: Dict):
        """
        Salva metadados dos treinos do treinador.
        
        Args:
            trainer_info: Informações do treinador
            metadata: Dicionário com metadados
        """
        metadata_path = self._get_metadata_path(trainer_info)
        
        try:
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar metadados: {e}")

    def _get_changelog_path(self, trainer_info) -> Path:
        """Obtém caminho do arquivo de changelog."""
        trainer_dir = self._get_trainer_dir(trainer_info)
        return trainer_dir / "changelog.json"

    def _log_change(self, trainer_info, action: str, details: str, plan_id: Optional[str] = None):
        """Registra uma entrada no histórico de alterações."""
        path = self._get_changelog_path(trainer_info)
        entries = []
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except Exception:
                entries = []

        entry = ChangeLogEntry(
            timestamp=datetime.now().isoformat(),
            action=action,
            details=details,
            plan_id=plan_id,
        )
        entries.append(entry.to_dict())

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(entries, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar changelog: {e}")

    def get_changelog(self, trainer_info, limit: int = 50) -> List[ChangeLogEntry]:
        """Obtém as últimas entradas do histórico de alterações."""
        path = self._get_changelog_path(trainer_info)
        if not path.exists():
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            entries = [ChangeLogEntry(**e) for e in raw]
            entries.sort(key=lambda e: e.timestamp, reverse=True)
            return entries[:limit]
        except Exception:
            return []

    def register_training(self, trainer_info, athlete, excel_path: Optional[str] = None, 
                         pdf_path: Optional[str] = None) -> TrainingRecord:
        """
        Registra um novo treino criado pelo profissional.
        
        Args:
            trainer_info: Informações do treinador
            athlete: Objeto Athlete
            excel_path: Caminho do arquivo Excel (opcional)
            pdf_path: Caminho do arquivo PDF (opcional)
        
        Returns:
            TrainingRecord criado
        """
        # Gerar ID único baseado em timestamp
        training_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Criar registro
        record = TrainingRecord(
            id=training_id,
            athlete_name=athlete.nome,
            athlete_data={
                'nome': athlete.nome,
                'idade': athlete.idade,
                'genero': athlete.genero,
                'peso': athlete.peso,
                'altura': athlete.altura,
                'imc': athlete.imc
            },
            sport=athlete.esporte,
            distance=athlete.distancia_prova,
            weeks=athlete.semanas_ate_prova,
            created_at=datetime.now().isoformat(),
            excel_path=excel_path,
            pdf_path=pdf_path,
            last_modified=datetime.now().isoformat()
        )
        
        # Carregar metadados existentes
        metadata = self._load_metadata(trainer_info)
        
        # Adicionar novo registro
        metadata['plans'].append(record.to_dict())
        
        # Salvar metadados
        self._save_metadata(trainer_info, metadata)

        self._log_change(
            trainer_info,
            action='created',
            details=f"Plano criado para {athlete.nome} ({athlete.esporte}, {athlete.distancia_prova})",
            plan_id=training_id,
        )
        
        return record
    
    def get_trainer_plans(self, trainer_info) -> List[TrainingRecord]:
        """
        Obtém todos os planos de um treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Lista de TrainingRecord
        """
        metadata = self._load_metadata(trainer_info)
        plans = []
        
        for plan_data in metadata.get('plans', []):
            plans.append(TrainingRecord(**plan_data))
        
        # Ordenar por data de criação (mais recentes primeiro)
        plans.sort(key=lambda x: x.created_at, reverse=True)
        
        return plans
    
    def get_plan_by_id(self, trainer_info, plan_id: str) -> Optional[TrainingRecord]:
        """
        Obtém um plano específico por ID.
        
        Args:
            trainer_info: Informações do treinador
            plan_id: ID do plano
        
        Returns:
            TrainingRecord ou None se não encontrado
        """
        plans = self.get_trainer_plans(trainer_info)
        
        for plan in plans:
            if plan.id == plan_id:
                return plan
        
        return None
    
    def verify_ownership(self, trainer_info, plan_id: str) -> bool:
        """
        Verifica se o treinador é dono do plano.
        
        Args:
            trainer_info: Informações do treinador
            plan_id: ID do plano
        
        Returns:
            True se o treinador é dono, False caso contrário
        """
        plan = self.get_plan_by_id(trainer_info, plan_id)
        return plan is not None
    
    def delete_plan(self, trainer_info, plan_id: str) -> Tuple[bool, str]:
        """
        Deleta um plano (apenas se o treinador for o dono).
        
        Args:
            trainer_info: Informações do treinador
            plan_id: ID do plano
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        # Verificar propriedade
        if not self.verify_ownership(trainer_info, plan_id):
            return False, "Você não tem permissão para deletar este plano."
        
        # Carregar metadados
        metadata = self._load_metadata(trainer_info)
        
        # Encontrar e remover plano
        plan_found = None
        for i, plan_data in enumerate(metadata['plans']):
            if plan_data['id'] == plan_id:
                plan_found = metadata['plans'].pop(i)
                break
        
        if not plan_found:
            return False, "Plano não encontrado."
        
        # Deletar arquivos físicos
        try:
            if plan_found.get('excel_path') and os.path.exists(plan_found['excel_path']):
                os.remove(plan_found['excel_path'])
            
            if plan_found.get('pdf_path') and os.path.exists(plan_found['pdf_path']):
                os.remove(plan_found['pdf_path'])
        except Exception as e:
            print(f"⚠️ Erro ao deletar arquivos: {e}")
        
        # Salvar metadados atualizados
        self._save_metadata(trainer_info, metadata)

        athlete_name = plan_found.get('athlete_name', 'desconhecido')
        self._log_change(
            trainer_info,
            action='deleted',
            details=f"Plano de {athlete_name} removido",
            plan_id=plan_id,
        )
        
        return True, "Plano deletado com sucesso!"
    
    def update_plan_paths(self, trainer_info, plan_id: str, 
                         excel_path: Optional[str] = None, pdf_path: Optional[str] = None) -> bool:
        """
        Atualiza caminhos de arquivos de um plano.
        
        Args:
            trainer_info: Informações do treinador
            plan_id: ID do plano
            excel_path: Novo caminho Excel (opcional)
            pdf_path: Novo caminho PDF (opcional)
        
        Returns:
            True se atualizado com sucesso
        """
        # Verificar propriedade
        if not self.verify_ownership(trainer_info, plan_id):
            return False
        
        # Carregar metadados
        metadata = self._load_metadata(trainer_info)
        
        # Atualizar plano
        for plan_data in metadata['plans']:
            if plan_data['id'] == plan_id:
                if excel_path:
                    plan_data['excel_path'] = excel_path
                if pdf_path:
                    plan_data['pdf_path'] = pdf_path
                plan_data['last_modified'] = datetime.now().isoformat()
                break
        
        # Salvar metadados
        self._save_metadata(trainer_info, metadata)

        parts = []
        if excel_path:
            parts.append('Excel')
        if pdf_path:
            parts.append('PDF')
        self._log_change(
            trainer_info,
            action='exported',
            details=f"Exportado {', '.join(parts)} do plano",
            plan_id=plan_id,
        )
        
        return True
    
    def get_plans_directory(self, trainer_info) -> str:
        """
        Obtém o diretório de planos do treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Caminho absoluto do diretório
        """
        return str(self._get_plans_dir(trainer_info))
    
    def get_statistics(self, trainer_info) -> Dict:
        """
        Obtém estatísticas dos treinos do treinador.
        
        Args:
            trainer_info: Informações do treinador
        
        Returns:
            Dicionário com estatísticas
        """
        plans = self.get_trainer_plans(trainer_info)
        
        # Contar por esporte
        sports_count = {}
        for plan in plans:
            sport = plan.sport
            sports_count[sport] = sports_count.get(sport, 0) + 1
        
        # Contar atletas únicos
        unique_athletes = set(plan.athlete_name for plan in plans)
        
        return {
            'total_plans': len(plans),
            'unique_athletes': len(unique_athletes),
            'sports_distribution': sports_count,
            'latest_plan': plans[0].created_at if plans else None
        }

    def get_athletes_summary(self, trainer_info) -> List[Dict]:
        """
        Agrupa planos por atleta para exibição em hero cards.

        Returns:
            Lista de dicts, um por atleta, ordenada por última atividade:
            {
                'athlete_name': str,
                'athlete_data': dict,          # dados do plano mais recente
                'plans': [TrainingRecord, ...], # todos os planos do atleta
                'latest_sport': str,
                'total_weeks': int,             # soma de semanas de todos os planos
                'current_week': int,            # semana atual do plano mais recente
                'status': str,                  # 'active' | 'completed'
            }
        """
        plans = self.get_trainer_plans(trainer_info)

        groups: Dict[str, List[TrainingRecord]] = {}
        for p in plans:
            groups.setdefault(p.athlete_name, []).append(p)

        result = []
        now = datetime.now()
        for name, athlete_plans in groups.items():
            # planos já ordenados (mais recente primeiro)
            latest = athlete_plans[0]
            total_weeks = sum(p.weeks for p in athlete_plans)

            # Calcular semana atual do plano mais recente
            try:
                created = datetime.fromisoformat(latest.created_at)
                elapsed_days = (now - created).days
                current_week = min(max(elapsed_days // 7 + 1, 1), latest.weeks)
            except (ValueError, TypeError):
                current_week = 1

            status = "completed" if current_week >= latest.weeks else "active"

            result.append({
                'athlete_name': name,
                'athlete_data': latest.athlete_data,
                'plans': athlete_plans,
                'latest_sport': latest.sport,
                'total_weeks': total_weeks,
                'current_week': current_week,
                'status': status,
            })

        # Ordenar: ativos primeiro, depois por data do plano mais recente
        result.sort(key=lambda a: (a['status'] != 'active', a['plans'][0].created_at), reverse=False)
        # inverter para que ativos (False < True) fiquem primeiro
        result.sort(key=lambda a: (a['status'] != 'active',))

        return result

    # ── Calendário & Overrides ───────────────────────────────────

    def _get_calendar_path(self, trainer_info, plan_id: str) -> Path:
        """Caminho do ficheiro de calendário de um plano."""
        return self._get_plans_dir(trainer_info) / f"{plan_id}_calendar.json"

    def _get_overrides_path(self, trainer_info, plan_id: str) -> Path:
        """Caminho do ficheiro de overrides de treinos."""
        return self._get_plans_dir(trainer_info) / f"{plan_id}_overrides.json"

    def map_sessions_to_calendar(
        self, trainer_info, plan_id: str,
        sessions: List[Dict], start_date: str
    ) -> Dict[str, List[Dict]]:
        """
        Mapeia sessões de treino para datas concretas de calendário.

        Args:
            trainer_info: Informações do treinador
            plan_id: ID do plano
            sessions: Lista de sessões de get_full_training_plan()
                      Cada sessão: {dia, modalidade, duracao, tipo, zona, descricao, semana, fase, tipo_semana}
            start_date: Data de início no formato ISO (YYYY-MM-DD)

        Returns:
            Dict[str(YYYY-MM-DD), List[session_dict]]
        """
        from datetime import date, timedelta

        day_map = {
            'Segunda': 0, 'Terça': 1, 'Quarta': 2,
            'Quinta': 3, 'Sexta': 4, 'Sábado': 5, 'Domingo': 6,
        }

        base = date.fromisoformat(start_date)
        # Alinhar ao início da semana (segunda)
        base_monday = base - timedelta(days=base.weekday())

        calendar: Dict[str, List[Dict]] = {}

        for session in sessions:
            week_num = session.get('semana', 1)
            day_name = session.get('dia', 'Segunda')
            day_offset = day_map.get(day_name, 0)

            target_date = base_monday + timedelta(weeks=week_num - 1, days=day_offset)
            key = target_date.isoformat()

            calendar.setdefault(key, []).append(session)

        # Persistir
        cal_path = self._get_calendar_path(trainer_info, plan_id)
        try:
            with open(cal_path, 'w', encoding='utf-8') as f:
                json.dump(calendar, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar calendário: {e}")

        return calendar

    def get_calendar(self, trainer_info, plan_id: str) -> Dict[str, List[Dict]]:
        """Carrega calendário persistido de um plano."""
        cal_path = self._get_calendar_path(trainer_info, plan_id)
        if cal_path.exists():
            try:
                with open(cal_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def save_workout_override(
        self, trainer_info, plan_id: str, date_key: str, session_index: int, data: Dict
    ) -> bool:
        """
        Salva uma edição manual (override) de um treino num dia específico.

        Args:
            date_key: 'YYYY-MM-DD'
            session_index: índice da sessão nesse dia
            data: dict com campos editados (tipo, zona, duracao, descricao, modalidade)
        """
        path = self._get_overrides_path(trainer_info, plan_id)
        overrides = {}
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)
            except Exception:
                overrides = {}

        overrides.setdefault(date_key, {})
        overrides[date_key][str(session_index)] = data

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(overrides, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def get_workout_for_date(
        self, trainer_info, plan_id: str, date_key: str
    ) -> List[Dict]:
        """
        Retorna sessões de um dia, aplicando overrides sobre o calendário base.
        """
        calendar = self.get_calendar(trainer_info, plan_id)
        base_sessions = [dict(s) for s in calendar.get(date_key, [])]

        # Aplicar overrides
        path = self._get_overrides_path(trainer_info, plan_id)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    overrides = json.load(f)
                day_overrides = overrides.get(date_key, {})
                for idx_str, changes in day_overrides.items():
                    idx = int(idx_str)
                    if 0 <= idx < len(base_sessions):
                        base_sessions[idx].update(changes)
            except Exception:
                pass

        return base_sessions

    def reset_workout_override(
        self, trainer_info, plan_id: str, date_key: str, session_index: Optional[int] = None
    ) -> bool:
        """
        Remove override(s) de um dia (volta ao treino gerado automaticamente).

        Se session_index é None, remove todos os overrides do dia.
        """
        path = self._get_overrides_path(trainer_info, plan_id)
        if not path.exists():
            return True
        try:
            with open(path, 'r', encoding='utf-8') as f:
                overrides = json.load(f)
        except Exception:
            return True

        if date_key not in overrides:
            return True

        if session_index is None:
            del overrides[date_key]
        else:
            overrides[date_key].pop(str(session_index), None)
            if not overrides[date_key]:
                del overrides[date_key]

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(overrides, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def move_workout(
        self, trainer_info, plan_id: str,
        from_date: str, session_index: int, to_date: str
    ) -> bool:
        """
        Move uma sessão de um dia para outro (drag & drop).

        Persiste como overrides: remove sessão do dia origem,
        adiciona ao dia destino.
        """
        calendar = self.get_calendar(trainer_info, plan_id)
        from_sessions = calendar.get(from_date, [])

        if session_index < 0 or session_index >= len(from_sessions):
            return False

        session = from_sessions.pop(session_index)
        calendar.setdefault(to_date, []).append(session)

        # Re-persistir calendário completo
        cal_path = self._get_calendar_path(trainer_info, plan_id)
        try:
            with open(cal_path, 'w', encoding='utf-8') as f:
                json.dump(calendar, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    # ── Templates de Treino ──────────────────────────────────────

    def _get_templates_path(self, trainer_info) -> Path:
        """Caminho do ficheiro de templates do treinador."""
        return self._get_plans_dir(trainer_info) / "templates.json"

    def get_templates(self, trainer_info) -> List[Dict]:
        """Carrega todos os templates do treinador."""
        path = self._get_templates_path(trainer_info)
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def save_template(self, trainer_info, template: Dict) -> bool:
        """
        Salva um novo template de treino.

        template: {name, sport, type, zone, duration, modality, description}
        """
        templates = self.get_templates(trainer_info)
        template["id"] = f"tmpl_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(templates)}"
        template["created_at"] = datetime.now().isoformat()
        templates.append(template)

        path = self._get_templates_path(trainer_info)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def delete_template(self, trainer_info, template_id: str) -> bool:
        """Remove um template pelo ID."""
        templates = self.get_templates(trainer_info)
        templates = [t for t in templates if t.get("id") != template_id]

        path = self._get_templates_path(trainer_info)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False


# Instância global
training_manager = TrainingManager()
