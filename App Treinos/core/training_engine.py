"""
Sistema de Geração de Planilhas de Treinamento Esportivo
Modalidades: Triathlon, Corrida, Natação e Ciclismo
"""

import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path
import os
import math


def calcular_semanas_ate_prova(data_prova_str: str) -> int:
    """
    Calcula quantas semanas faltam até a data da prova.
    
    Args:
        data_prova_str: Data da prova no formato DD/MM/AAAA
        
    Returns:
        Número de semanas até a prova (arredondado para cima)
        
    Raises:
        ValueError: Se a data for inválida ou estiver no passado
    """
    try:
        # Parsear a data da prova
        data_prova = datetime.strptime(data_prova_str, "%d/%m/%Y")
        
        # Obter data atual (sem hora para comparação justa)
        data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        data_prova = data_prova.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Verificar se a data não está no passado
        if data_prova < data_atual:
            raise ValueError("A data da prova não pode estar no passado!")
        
        # Calcular diferença em dias
        diferenca_dias = (data_prova - data_atual).days
        
        # Converter para semanas (arredondar para cima)
        semanas = math.ceil(diferenca_dias / 7)
        
        # Garantir pelo menos 1 semana
        return max(1, semanas)
        
    except ValueError as e:
        if "time data" in str(e) or "does not match format" in str(e):
            raise ValueError("Formato de data inválido! Use DD/MM/AAAA (ex: 15/08/2026)")
        raise


@dataclass
class HealthIssue:
    """Classe para armazenar problemas de saúde"""
    tipo: str  # ortopédico, cardíaco, respiratório, metabólico
    descricao: str
    membro_afetado: Optional[str] = None  # joelho_direito, ombro_esquerdo, etc.
    gravidade: str = "leve"  # leve, moderado, grave
    restricoes: List[str] = field(default_factory=list)


@dataclass
class TrainerInfo:
    """Classe para armazenar dados do profissional de Educação Física"""
    nome_completo: str
    cpf: str
    cref: str  # Conselho Regional de Educação Física
    
    def __post_init__(self):
        """Valida os dados do treinador após inicialização"""
        if not self.nome_completo or len(self.nome_completo.strip()) < 5:
            raise ValueError("Nome completo deve ter pelo menos 5 caracteres")
        
        if not self._validar_cpf(self.cpf):
            raise ValueError("CPF inválido")
        
        if not self._validar_cref(self.cref):
            raise ValueError("CREF inválido")
    
    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """Valida CPF usando algoritmo oficial"""
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # CPF deve ter 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais (CPF inválido)
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula o primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # Calcula o segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == digito2
    
    @staticmethod
    def _validar_cref(cref: str) -> bool:
        """Valida formato do CREF (ex: 123456-G/SP, CREF1 123456-G/SP)"""
        import re
        # Remove espaços extras
        cref = cref.strip()
        
        # Aceita formatos: 123456-G/SP, CREF1 123456-G/SP, 123456G/SP
        pattern = r'^(CREF\d?\s?)?\d{4,6}[-\s]?[A-Z]/[A-Z]{2}$'
        return bool(re.match(pattern, cref.upper()))
    
    def formatar_cpf(self) -> str:
        """Retorna CPF formatado: 000.000.000-00"""
        cpf = ''.join(filter(str.isdigit, self.cpf))
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def formatar_cref(self) -> str:
        """Retorna CREF formatado"""
        return self.cref.upper()


@dataclass
class Athlete:
    """Classe para armazenar dados do atleta"""
    nome: str
    idade: int
    peso: float  # kg
    altura: float  # cm
    esporte: str
    dias_semana: int
    distancia_prova: str
    limiar_lactato: float
    vo2_max: float
    genero: str  # masculino, feminino
    trainer: TrainerInfo  # Profissional responsável pelo plano
    semanas_ate_prova: int = 1  # número de semanas até a prova
    problemas_saude: List[HealthIssue] = field(default_factory=list)
    fase_menstrual: Optional[str] = None  # menstrual, folicular, ovulatoria, lutea
    
    @property
    def imc(self) -> float:
        """Calcula o IMC do atleta"""
        altura_m = self.altura / 100
        return round(self.peso / (altura_m ** 2), 1)
    
    @property
    def tem_restricoes(self) -> bool:
        """Verifica se o atleta tem alguma restrição de saúde"""
        return len(self.problemas_saude) > 0


class HealthAdvisor:
    """Sistema de IA para adequações de treinamento baseadas em problemas de saúde"""
    
    def __init__(self):
        # Base de conhecimento para recomendações
        self.knowledge_base = {
            'joelho': {
                'restricoes': ['impacto alto', 'descidas íngremes', 'sprints máximos'],
                'recomendacoes': [
                    'Prefira terrenos planos ou levemente ondulados',
                    'Substitua corridas longas por ciclismo ou natação',
                    'Use tênis com amortecimento adequado',
                    'Fortaleça musculatura do quadríceps e posterior de coxa',
                    'Evite aumentos súbitos de volume (regra dos 10%)'
                ],
                'alternativas': {
                    'corrida': 'Reduzir 30-50% do volume, substituir por elíptico/bike',
                    'ciclismo': 'Ajustar altura do selim, evitar subidas muito íngremes',
                    'natação': 'Evitar nado peito excessivo (estresse no joelho)'
                }
            },
            'tornozelo': {
                'restricoes': ['terrenos irregulares', 'mudanças bruscas de direção'],
                'recomendacoes': [
                    'Prefira superfícies regulares e previsíveis',
                    'Trabalhe propriocepção e fortalecimento',
                    'Use tornozeleira de suporte se necessário',
                    'Evite treinos técnicos de velocidade inicialmente'
                ],
                'alternativas': {
                    'corrida': 'Pista ou esteira, evitar trilhas',
                    'ciclismo': 'Sem restrições significativas',
                    'natação': 'Sem restrições'
                }
            },
            'ombro': {
                'restricoes': ['braçadas forçadas', 'volume excessivo de natação'],
                'recomendacoes': [
                    'Trabalhe técnica de nado para reduzir sobrecarga',
                    'Fortaleça manguito rotador',
                    'Faça aquecimento adequado antes de nadar',
                    'Use pull buoy para reduzir carga no ombro',
                    'Evite nado borboleta se houver dor'
                ],
                'alternativas': {
                    'natação': 'Reduzir volume em 40%, focar em pernas com pull buoy',
                    'corrida': 'Sem restrições',
                    'ciclismo': 'Ajustar posição do guidão (evitar muita flexão)'
                }
            },
            'quadril': {
                'restricoes': ['amplitudes extremas', 'impacto repetitivo'],
                'recomendacoes': [
                    'Fortaleça glúteos e core',
                    'Trabalhe mobilidade de quadril',
                    'Ajuste biomecânica da passada',
                    'Prefira volumes moderados com mais frequência'
                ],
                'alternativas': {
                    'corrida': 'Reduzir 20-30% do volume, preferir terrenos planos',
                    'ciclismo': 'Ajustar altura e posição do selim',
                    'natação': 'Evitar excesso de batimento de pernas'
                }
            },
            'lombar': {
                'restricoes': ['flexões extremas', 'posições aerodinâmicas prolongadas'],
                'recomendacoes': [
                    'Fortaleça musculatura do core',
                    'Trabalhe flexibilidade de posterior de coxa',
                    'Mantenha postura neutra durante exercícios',
                    'Evite cargas axiais excessivas'
                ],
                'alternativas': {
                    'ciclismo': 'Ajustar bike fit, levantar guidão, evitar posição aero prolongada',
                    'corrida': 'Preferir terrenos planos, evitar mochilas pesadas',
                    'natação': 'Evitar hiperextensão lombar, focar em rotação do corpo'
                }
            },
            'pé': {
                'restricoes': ['impacto alto', 'meias longas sem recuperação'],
                'recomendacoes': [
                    'Use calçados adequados ao tipo de pisada',
                    'Considere palmilhas personalizadas',
                    'Fortaleça musculatura intrínseca do pé',
                    'Faça liberação miofascial regular'
                ],
                'alternativas': {
                    'corrida': 'Reduzir volume, intercalar com treinos sem impacto',
                    'ciclismo': 'Ajustar trava da sapatilha',
                    'natação': 'Sem restrições significativas'
                }
            },
            'coxa': {
                'restricoes': ['acelerações máximas', 'alongamentos extremos'],
                'recomendacoes': [
                    'Aquecimento dinâmico é essencial',
                    'Fortaleça musculatura posterior',
                    'Evite sprints máximos até recuperação completa',
                    'Trabalhe flexibilidade gradualmente'
                ],
                'alternativas': {
                    'corrida': 'Reduzir intensidade, focar em Z2-Z3',
                    'ciclismo': 'Reduzir resistência em subidas',
                    'natação': 'Sem restrições significativas'
                }
            }
        }
        
        # Problemas sistêmicos
        self.systemic_conditions = {
            'asma': [
                'Tenha broncodilatador sempre disponível',
                'Aquecimento gradual é essencial (15-20min)',
                'Evite treinos intensos em ar muito frio ou seco',
                'Natação é geralmente bem tolerada (ar úmido)',
                'Monitore sintomas e ajuste intensidade conforme necessário'
            ],
            'diabetes': [
                'Monitore glicemia antes, durante e após treinos longos',
                'Tenha carboidratos de rápida absorção disponíveis',
                'Ajuste insulina conforme orientação médica',
                'Prefira treinos em horários regulares',
                'Comunique ao treinador sobre sua condição'
            ],
            'hipertensão': [
                'Evite apneia durante exercícios de força',
                'Priorize treinos aeróbicos de intensidade moderada',
                'Monitore pressão arterial regularmente',
                'Mantenha hidratação adequada',
                'Não interrompa medicação sem orientação médica'
            ],
            'cardíaco': [
                'ATENÇÃO: Siga rigorosamente orientação médica',
                'Evite exercícios de alta intensidade sem liberação',
                'Monitore frequência cardíaca constantemente',
                'Não ultrapasse zonas prescritas pelo cardiologista',
                'Tenha plano de emergência sempre definido'
            ]
        }
        
        # Recomendações por fase do ciclo menstrual
        self.menstrual_cycle_knowledge = {
            'menstrual': {
                'dias': '1-5',
                'caracteristicas': 'Menstruação, baixos níveis hormonais',
                'recomendacoes': [
                    'Reduza intensidade e volume em 20-30% se houver desconforto',
                    'Priorize treinos de baixa/moderada intensidade (Z1-Z2)',
                    'Alongamentos e yoga podem ajudar com cólicas',
                    'Hidratação extra é importante (maior perda de fluidos)',
                    'Considere suplementação de ferro se fluxo for intenso'
                ],
                'ajustes': {
                    'volume': 0.75,  # Reduzir para 75%
                    'intensidade': 'reduzir_alta',  # Converter Z4-Z5 para Z2-Z3
                    'recuperacao': 1.3  # 30% mais recuperação
                }
            },
            'folicular': {
                'dias': '6-14',
                'caracteristicas': 'Pós-menstruação, estrogênio crescente',
                'recomendacoes': [
                    'Fase ideal para treinos de alta intensidade',
                    'Aproveite para trabalhos de força e potência',
                    'Ótima fase para intervalados e VO2max',
                    'Recuperação muscular é mais rápida',
                    'Tolerância à dor está aumentada'
                ],
                'ajustes': {
                    'volume': 1.0,  # Volume normal
                    'intensidade': 'normal',
                    'recuperacao': 1.0
                }
            },
            'ovulatoria': {
                'dias': '13-16',
                'caracteristicas': 'Ovulação, pico de estrogênio',
                'recomendacoes': [
                    'Excelente fase para performance máxima',
                    'Aproveite para testes e treinos chave',
                    'Força e coordenação estão no auge',
                    'Atenção: ligeiro aumento no risco de lesões ligamentares',
                    'Aquecimento mais completo é recomendado'
                ],
                'ajustes': {
                    'volume': 1.0,
                    'intensidade': 'normal',
                    'recuperacao': 1.0
                }
            },
            'lutea': {
                'dias': '17-28',
                'caracteristicas': 'Pré-menstrual, progesterona alta',
                'recomendacoes': [
                    'Possível retenção de líquidos e fadiga',
                    'Reduza intensidade em 10-15% se necessário',
                    'Priorize treinos aeróbicos de base (Z2)',
                    'Aumente carboidratos (metabolismo mais acelerado)',
                    'TPM pode afetar motivação - seja flexível',
                    'Temperatura corporal mais elevada - hidrate-se mais'
                ],
                'ajustes': {
                    'volume': 0.9,  # Reduzir para 90%
                    'intensidade': 'reduzir_moderada',  # Preferir Z2-Z3
                    'recuperacao': 1.2  # 20% mais recuperação
                }
            }
        }
    
    def analyze_menstrual_cycle(self, fase: str) -> Dict:
        """Analisa fase do ciclo menstrual e retorna recomendações"""
        if not fase or fase not in self.menstrual_cycle_knowledge:
            return {'status': 'sem_analise', 'recomendacoes': [], 'ajustes': {}}
        
        info = self.menstrual_cycle_knowledge[fase]
        
        recomendacoes = [
            f"🌸 FASE: {fase.upper()} (Dias {info['dias']} do ciclo)",
            f"   {info['caracteristicas']}",
            ""
        ]
        recomendacoes.extend([f"  • {rec}" for rec in info['recomendacoes']])
        
        return {
            'status': 'analisado',
            'fase': fase,
            'recomendacoes': recomendacoes,
            'ajustes': info['ajustes']
        }
    
    def analyze_health_issues(self, problemas: List[HealthIssue], esporte: str) -> Dict:
        """Analisa problemas de saúde e retorna recomendações personalizadas"""
        if not problemas:
            return {'status': 'sem_restricoes', 'recomendacoes': [], 'adequacoes': {}}
        
        recomendacoes_gerais = []
        adequacoes = {}
        restricoes_criticas = []
        
        for problema in problemas:
            if problema.tipo.lower() == 'ortopédico' and problema.membro_afetado:
                # Extrair região do membro (ex: joelho_direito -> joelho)
                regiao = problema.membro_afetado.split('_')[0].lower()
                
                if regiao in self.knowledge_base:
                    kb = self.knowledge_base[regiao]
                    
                    # Adicionar recomendações específicas
                    recomendacoes_gerais.extend([
                        f"⚠️ {problema.descricao} ({problema.membro_afetado.replace('_', ' ').title()}):"
                    ])
                    recomendacoes_gerais.extend([f"  • {rec}" for rec in kb['recomendacoes']])
                    
                    # Adicionar restrições
                    restricoes_criticas.extend(kb['restricoes'])
                    
                    # Adequações por esporte
                    esporte_lower = esporte.lower()
                    if esporte_lower in kb['alternativas']:
                        adequacoes[problema.membro_afetado] = kb['alternativas'][esporte_lower]
                    
                    # Adequações para triathlon (todas as modalidades)
                    if esporte_lower == 'triathlon':
                        for mod, alt in kb['alternativas'].items():
                            adequacoes[f"{problema.membro_afetado}_{mod}"] = alt
            
            elif problema.tipo.lower() in self.systemic_conditions:
                condicao = problema.tipo.lower()
                recomendacoes_gerais.append(f"\n⚠️ {problema.descricao}:")
                recomendacoes_gerais.extend([f"  • {rec}" for rec in self.systemic_conditions[condicao]])
        
        return {
            'status': 'com_restricoes',
            'recomendacoes': recomendacoes_gerais,
            'adequacoes': adequacoes,
            'restricoes': restricoes_criticas
        }
    
    def adjust_training_for_menstrual_cycle(self, treino: Dict, fase: str) -> Dict:
        """Ajusta treino baseado na fase do ciclo menstrual"""
        if not fase or fase not in self.menstrual_cycle_knowledge:
            return treino
        
        treino_ajustado = treino.copy()
        ajustes = self.menstrual_cycle_knowledge[fase]['ajustes']
        
        # Ajustar volume
        if ajustes['volume'] < 1.0:
            duracao_original = int(treino['duracao'].split()[0])
            nova_duracao = int(duracao_original * ajustes['volume'])
            treino_ajustado['duracao'] = f"{nova_duracao} min"
        
        # Ajustar intensidade
        if ajustes['intensidade'] == 'reduzir_alta':
            # Fase menstrual: reduzir treinos intensos
            if treino['zona'] in ['Z4 - Limiar', 'Z5 - VO2max']:
                treino_ajustado['zona'] = 'Z2 - Aeróbico'
                treino_ajustado['tipo'] = 'Base Moderada'
                treino_ajustado['descricao'] = f"{treino['descricao']} | 🌸 AJUSTADO: Intensidade reduzida (fase menstrual)"
            else:
                treino_ajustado['descricao'] = f"{treino['descricao']} | 🌸 Fase menstrual - mantenha conforto"
        
        elif ajustes['intensidade'] == 'reduzir_moderada':
            # Fase lútea: reduzir moderadamente
            if treino['zona'] == 'Z5 - VO2max':
                treino_ajustado['zona'] = 'Z3 - Tempo'
                treino_ajustado['descricao'] = f"{treino['descricao']} | 🌸 AJUSTADO: Intensidade moderada (fase lútea)"
            elif treino['zona'] == 'Z4 - Limiar':
                treino_ajustado['zona'] = 'Z3 - Tempo'
                treino_ajustado['descricao'] = f"{treino['descricao']} | 🌸 AJUSTADO: Redução leve (fase lútea)"
            else:
                treino_ajustado['descricao'] = f"{treino['descricao']} | 🌸 Fase lútea - hidratação extra"
        
        return treino_ajustado
    
    def adjust_training(self, treino: Dict, health_analysis: Dict, problema: HealthIssue) -> Dict:
        """Ajusta um treino específico baseado em problemas de saúde"""
        treino_ajustado = treino.copy()
        modalidade = treino['modalidade'].lower()
        
        if problema.tipo.lower() == 'ortopédico' and problema.membro_afetado:
            regiao = problema.membro_afetado.split('_')[0].lower()
            
            # Ajustes específicos por região e modalidade
            if regiao == 'joelho' and modalidade == 'corrida':
                # Reduzir duração e intensidade
                duracao_original = int(treino['duracao'].split()[0])
                nova_duracao = int(duracao_original * 0.7)
                treino_ajustado['duracao'] = f"{nova_duracao} min"
                treino_ajustado['descricao'] += " | ⚕️ AJUSTADO: Volume reduzido para proteção do joelho"
                
                if 'Intervalado' in treino['tipo'] or 'Sprint' in treino['tipo']:
                    treino_ajustado['tipo'] = 'Base Moderada'
                    treino_ajustado['zona'] = 'Z2 - Aeróbico'
                    treino_ajustado['descricao'] = "Corrida contínua em ritmo controlado (ajustado por lesão no joelho)"
            
            elif regiao == 'ombro' and modalidade == 'natação':
                duracao_original = int(treino['duracao'].split()[0])
                nova_duracao = int(duracao_original * 0.6)
                treino_ajustado['duracao'] = f"{nova_duracao} min"
                treino_ajustado['descricao'] += " | ⚕️ AJUSTADO: Use pull buoy e reduza braçadas forçadas"
            
            elif regiao == 'lombar' and modalidade == 'ciclismo':
                treino_ajustado['descricao'] += " | ⚕️ AJUSTADO: Mantenha postura ereta, evite posição aero"
            
            elif regiao in ['pé', 'tornozelo'] and modalidade == 'corrida':
                duracao_original = int(treino['duracao'].split()[0])
                nova_duracao = int(duracao_original * 0.75)
                treino_ajustado['duracao'] = f"{nova_duracao} min"
                treino_ajustado['descricao'] += f" | ⚕️ AJUSTADO: Volume reduzido por problema no {regiao}"
        
        return treino_ajustado


class PeriodizationPlanner:
    """Gerencia a periodização do treinamento em ciclos (mesociclos)"""
    
    def __init__(self, semanas_totais: int, esporte: str):
        self.semanas_totais = semanas_totais
        self.esporte = esporte
        
        # Fases da periodização (ordem cronológica)
        self.fases_periodizacao = [
            'base',           # Construção aeróbica
            'resistencia',    # Resistência específica
            'velocidade',     # Desenvolvimento de velocidade
            'potencia',       # Potência e VO2max
            'polimento'       # Taper/Polimento final
        ]
        
        # Configuração de cada fase
        self.fase_config = {
            'base': {
                'nome': 'Base Aeróbica',
                'descricao': 'Construção de base aeróbica e adaptação muscular',
                'volume': 1.0,
                'intensidade': 'baixa',  # Z1-Z2 predominante
                'tipos_treino': ['Base', 'Long Run/Ride', 'Recuperação', 'Técnica'],
                'zonas_principais': ['Z1 - Recuperação', 'Z2 - Aeróbico'],
                'porcentagem_intenso': 0.15  # 15% de treinos intensos
            },
            'resistencia': {
                'nome': 'Resistência Específica',
                'descricao': 'Desenvolvimento de resistência específica da prova',
                'volume': 1.2,
                'intensidade': 'moderada',  # Z2-Z3 predominante
                'tipos_treino': ['Tempo Run', 'Sweet Spot', 'Long Run/Ride', 'Base'],
                'zonas_principais': ['Z2 - Aeróbico', 'Z3 - Tempo'],
                'porcentagem_intenso': 0.25  # 25% de treinos intensos
            },
            'velocidade': {
                'nome': 'Desenvolvimento de Velocidade',
                'descricao': 'Melhoria de velocidade e economia de movimento',
                'volume': 1.1,
                'intensidade': 'alta',  # Z3-Z4 predominante
                'tipos_treino': ['Intervalado', 'Tempo Run', 'Fartlek', 'Técnica'],
                'zonas_principais': ['Z3 - Tempo', 'Z4 - Limiar'],
                'porcentagem_intenso': 0.35  # 35% de treinos intensos
            },
            'potencia': {
                'nome': 'Potência e VO2max',
                'descricao': 'Desenvolvimento de potência máxima e VO2max',
                'volume': 1.0,
                'intensidade': 'muito_alta',  # Z4-Z5 predominante
                'tipos_treino': ['Intervalado', 'VO2max', 'Sprint', 'Tempo Run'],
                'zonas_principais': ['Z4 - Limiar', 'Z5 - VO2max'],
                'porcentagem_intenso': 0.40  # 40% de treinos intensos
            },
            'polimento': {
                'nome': 'Polimento/Taper',
                'descricao': 'Redução de volume e manutenção de intensidade',
                'volume': 0.6,  # 60% do volume
                'intensidade': 'moderada',  # Manter intensidade, reduzir volume
                'tipos_treino': ['Recuperação', 'Técnica', 'Tempo Run curto', 'Base'],
                'zonas_principais': ['Z1 - Recuperação', 'Z2 - Aeróbico', 'Z3 - Tempo'],
                'porcentagem_intenso': 0.20  # 20% de treinos intensos
            }
        }
    
    def calcular_distribuicao_fases(self) -> List[Dict]:
        """Calcula a distribuição de semanas por fase de periodização"""
        total = self.semanas_totais
        
        # Última semana sempre é polimento
        if total <= 4:
            # Plano muito curto - apenas base e polimento
            return [
                {'fase': 'base', 'semana_inicio': 1, 'semana_fim': total - 1},
                {'fase': 'polimento', 'semana_inicio': total, 'semana_fim': total}
            ]
        
        elif total <= 8:
            # Plano curto - base, velocidade, polimento
            semanas_polimento = 1
            semanas_restantes = total - semanas_polimento
            semanas_base = semanas_restantes // 2
            semanas_velocidade = semanas_restantes - semanas_base
            
            return [
                {'fase': 'base', 'semana_inicio': 1, 'semana_fim': semanas_base},
                {'fase': 'velocidade', 'semana_inicio': semanas_base + 1, 'semana_fim': semanas_base + semanas_velocidade},
                {'fase': 'polimento', 'semana_inicio': total, 'semana_fim': total}
            ]
        
        elif total <= 16:
            # Plano médio - base, resistência, velocidade, polimento
            semanas_polimento = 2
            semanas_restantes = total - semanas_polimento
            semanas_base = int(semanas_restantes * 0.40)  # 40% base
            semanas_resistencia = int(semanas_restantes * 0.30)  # 30% resistência
            semanas_velocidade = semanas_restantes - semanas_base - semanas_resistencia
            
            return [
                {'fase': 'base', 'semana_inicio': 1, 'semana_fim': semanas_base},
                {'fase': 'resistencia', 'semana_inicio': semanas_base + 1, 'semana_fim': semanas_base + semanas_resistencia},
                {'fase': 'velocidade', 'semana_inicio': semanas_base + semanas_resistencia + 1, 'semana_fim': total - semanas_polimento},
                {'fase': 'polimento', 'semana_inicio': total - semanas_polimento + 1, 'semana_fim': total}
            ]
        
        else:
            # Plano longo - todas as fases
            semanas_polimento = 3
            semanas_restantes = total - semanas_polimento
            semanas_base = int(semanas_restantes * 0.35)  # 35% base
            semanas_resistencia = int(semanas_restantes * 0.25)  # 25% resistência
            semanas_velocidade = int(semanas_restantes * 0.20)  # 20% velocidade
            semanas_potencia = semanas_restantes - semanas_base - semanas_resistencia - semanas_velocidade
            
            return [
                {'fase': 'base', 'semana_inicio': 1, 'semana_fim': semanas_base},
                {'fase': 'resistencia', 'semana_inicio': semanas_base + 1, 'semana_fim': semanas_base + semanas_resistencia},
                {'fase': 'velocidade', 'semana_inicio': semanas_base + semanas_resistencia + 1, 'semana_fim': semanas_base + semanas_resistencia + semanas_velocidade},
                {'fase': 'potencia', 'semana_inicio': semanas_base + semanas_resistencia + semanas_velocidade + 1, 'semana_fim': total - semanas_polimento},
                {'fase': 'polimento', 'semana_inicio': total - semanas_polimento + 1, 'semana_fim': total}
            ]
    
    def get_fase_da_semana(self, numero_semana: int) -> str:
        """Retorna a fase de periodização para uma semana específica"""
        distribuicao = self.calcular_distribuicao_fases()
        
        for bloco in distribuicao:
            if bloco['semana_inicio'] <= numero_semana <= bloco['semana_fim']:
                return bloco['fase']
        
        return 'base'  # Fallback
    
    def is_semana_recuperacao(self, numero_semana: int) -> bool:
        """Verifica se é semana de recuperação (última de cada ciclo de 4 semanas)"""
        # Não aplicar em semanas de polimento
        fase = self.get_fase_da_semana(numero_semana)
        if fase == 'polimento':
            return False
        
        # Última semana de cada bloco de 4 semanas
        return numero_semana % 4 == 0
    
    def get_multiplicador_volume(self, numero_semana: int) -> float:
        """Retorna o multiplicador de volume para a semana"""
        fase = self.get_fase_da_semana(numero_semana)
        config = self.fase_config[fase]
        
        # Semana de recuperação: 70% do volume
        if self.is_semana_recuperacao(numero_semana):
            return config['volume'] * 0.7
        
        return config['volume']
    
    def get_info_semana(self, numero_semana: int) -> Dict:
        """Retorna informações completas sobre uma semana específica"""
        fase = self.get_fase_da_semana(numero_semana)
        config = self.fase_config[fase]
        is_recuperacao = self.is_semana_recuperacao(numero_semana)
        
        return {
            'numero': numero_semana,
            'fase': fase,
            'nome_fase': config['nome'],
            'descricao_fase': config['descricao'],
            'is_recuperacao': is_recuperacao,
            'tipo_semana': 'Recuperação Ativa' if is_recuperacao else 'Carga',
            'volume_multiplicador': self.get_multiplicador_volume(numero_semana),
            'intensidade': config['intensidade'],
            'tipos_treino_preferidos': config['tipos_treino'],
            'zonas_principais': config['zonas_principais']
        }


class TrainingZones:
    """Calcula zonas de treinamento baseadas em limiar e VO2"""
    
    def __init__(self, limiar_lactato: float, vo2_max: float):
        self.limiar = limiar_lactato
        self.vo2 = vo2_max
        
    def get_zones(self) -> Dict[str, Dict[str, float]]:
        """Retorna as zonas de treinamento em % do limiar"""
        return {
            'Z1 - Recuperação': {'min': 0.50, 'max': 0.65, 'desc': 'Recuperação ativa'},
            'Z2 - Aeróbico': {'min': 0.65, 'max': 0.80, 'desc': 'Base aeróbica'},
            'Z3 - Tempo': {'min': 0.80, 'max': 0.90, 'desc': 'Ritmo moderado'},
            'Z4 - Limiar': {'min': 0.90, 'max': 1.00, 'desc': 'No limiar'},
            'Z5 - VO2max': {'min': 1.00, 'max': 1.10, 'desc': 'Alta intensidade'}
        }
    
    def get_intensity_value(self, zone: str) -> str:
        """Retorna o valor de intensidade para cada zona"""
        zones = self.get_zones()
        if zone in zones:
            z = zones[zone]
            min_val = round(self.limiar * z['min'], 1)
            max_val = round(self.limiar * z['max'], 1)
            return f"{min_val}-{max_val} bpm"
        return "N/A"


class TrainingPlanGenerator:
    """Gera planos de treinamento personalizados"""
    
    def __init__(self, athlete: Athlete):
        self.athlete = athlete
        self.zones = TrainingZones(athlete.limiar_lactato, athlete.vo2_max)
        self.health_advisor = HealthAdvisor()
        self.health_analysis = self.health_advisor.analyze_health_issues(
            athlete.problemas_saude, 
            athlete.esporte
        )
        self.menstrual_analysis = None
        if athlete.genero.lower() == 'feminino' and athlete.fase_menstrual:
            self.menstrual_analysis = self.health_advisor.analyze_menstrual_cycle(
                athlete.fase_menstrual
            )
        
        # Periodização
        self.periodization = PeriodizationPlanner(athlete.semanas_ate_prova, athlete.esporte)
        
        # Configurações de distância
        self.distance_config = {
            'Sprint': {'semanas': 8, 'volume': 'baixo'},
            'Olímpico': {'semanas': 12, 'volume': 'médio'},
            'Meio Ironman': {'semanas': 16, 'volume': 'alto'},
            'Ironman': {'semanas': 20, 'volume': 'muito alto'},
            '5K': {'semanas': 8, 'volume': 'baixo'},
            '10K': {'semanas': 10, 'volume': 'médio'},
            'Meia Maratona': {'semanas': 14, 'volume': 'alto'},
            'Maratona': {'semanas': 18, 'volume': 'muito alto'},
            '1500m': {'semanas': 8, 'volume': 'baixo'},
            '3000m': {'semanas': 10, 'volume': 'médio'},
            '40K': {'semanas': 10, 'volume': 'médio'},
            '80K': {'semanas': 14, 'volume': 'alto'},
            '160K': {'semanas': 16, 'volume': 'muito alto'}
        }
    
    def get_weekly_training(self, numero_semana: int = 1) -> List[Dict]:
        """Gera treinos para uma semana específica"""
        # Obter informações da periodização
        info_semana = self.periodization.get_info_semana(numero_semana)
        
        # Gerar treinos base
        if self.athlete.esporte.lower() == 'triathlon':
            treinos = self._generate_triathlon_week(info_semana)
        elif self.athlete.esporte.lower() == 'corrida':
            treinos = self._generate_running_week(info_semana)
        elif self.athlete.esporte.lower() == 'natação':
            treinos = self._generate_swimming_week(info_semana)
        elif self.athlete.esporte.lower() == 'ciclismo':
            treinos = self._generate_cycling_week(info_semana)
        else:
            raise ValueError("Esporte não reconhecido")
        
        # Adicionar informação da semana em cada treino
        for treino in treinos:
            treino['semana'] = numero_semana
            treino['fase'] = info_semana['nome_fase']
            treino['tipo_semana'] = info_semana['tipo_semana']
        
        # Aplicar adequações baseadas em problemas de saúde
        if self.athlete.tem_restricoes:
            treinos = self._apply_health_adjustments(treinos)
        
        return treinos
    
    def get_full_training_plan(self) -> List[Dict]:
        """Gera plano de treinamento completo para todas as semanas"""
        plano_completo = []
        
        for semana in range(1, self.athlete.semanas_ate_prova + 1):
            treinos_semana = self.get_weekly_training(semana)
            plano_completo.extend(treinos_semana)
        
        return plano_completo
    
    def _apply_health_adjustments(self, treinos: List[Dict]) -> List[Dict]:
        """Aplica adequações aos treinos baseadas em problemas de saúde e ciclo menstrual"""
        treinos_ajustados = []
        
        for treino in treinos:
            treino_ajustado = treino.copy()
            
            # Aplicar ajustes para cada problema de saúde
            for problema in self.athlete.problemas_saude:
                treino_ajustado = self.health_advisor.adjust_training(
                    treino_ajustado, 
                    self.health_analysis, 
                    problema
                )
            
            # Aplicar ajustes para ciclo menstrual (se aplicável)
            if self.athlete.genero.lower() == 'feminino' and self.athlete.fase_menstrual:
                treino_ajustado = self.health_advisor.adjust_training_for_menstrual_cycle(
                    treino_ajustado,
                    self.athlete.fase_menstrual
                )
            
            treinos_ajustados.append(treino_ajustado)
        
        return treinos_ajustados
    
    def _generate_triathlon_week(self, info_semana: Dict = None) -> List[Dict]:
        """Gera treinos de triathlon"""
        if info_semana is None:
            info_semana = {
                'fase': 'base',
                'is_recuperacao': False,
                'volume_multiplicador': 1.0
            }
        
        volume_mult = info_semana['volume_multiplicador']
        volume = self.distance_config.get(self.athlete.distancia_prova, {}).get('volume', 'médio')
        
        # Templates baseados nos dias disponíveis
        if self.athlete.dias_semana >= 6:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquecimento + 8x100m técnica + 500m volta à calma'},
                {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 6x800m (rec 2min) + 10min desaq'},
                {'dia': 'Quarta', 'modalidade': 'Ciclismo', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante em terreno plano'},
                {'dia': 'Quinta', 'modalidade': 'Natação', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Intervalado', 'zona': 'Z3 - Tempo', 'descricao': '500m aquec + 10x200m (rec 30s) + 300m desaq'},
                {'dia': 'Sexta', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve e contínua'},
                {'dia': 'Sábado', 'modalidade': 'Ciclismo', 'duracao': f"{int(120 * volume_mult)} min", 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo com simulação de prova'},
                {'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Combinado', 'zona': 'Z3 - Tempo', 'descricao': '60min bike Z2 + 30min corrida Z3'}
            ]
        elif self.athlete.dias_semana >= 4:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquecimento + 6x100m técnica + 400m volta à calma'},
                {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 5x1000m (rec 2min) + 10min desaq'},
                {'dia': 'Sexta', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante em terreno variado'},
                {'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': '120 min', 'tipo': 'Combinado', 'zona': 'Z2 - Aeróbico', 'descricao': '90min bike Z2 + 30min corrida Z2'}
            ]
        else:
            treinos = [
                {'dia': 'Terça', 'modalidade': 'Natação', 'duracao': '50 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '800m aquecimento + 4x100m técnica + 300m volta à calma'},
                {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': '40 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua em ritmo confortável'},
                {'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo em terreno variado'}
            ]
        
        return treinos[:self.athlete.dias_semana]
    
    def _generate_running_week(self, info_semana: Dict = None) -> List[Dict]:
        """Gera treinos de corrida"""
        # Usar info da semana se fornecida, senão usar padrão
        if info_semana is None:
            info_semana = {
                'fase': 'base',
                'is_recuperacao': False,
                'volume_multiplicador': 1.0,
                'intensidade': 'moderada',
                'tipos_treino_preferidos': ['Base', 'Long Run'],
                'zonas_principais': ['Z2 - Aeróbico']
            }
        
        volume_mult = info_semana['volume_multiplicador']
        is_recuperacao = info_semana['is_recuperacao']
        fase = info_semana['fase']
        
        volume = self.distance_config.get(self.athlete.distancia_prova, {}).get('volume', 'médio')
        
        if self.athlete.dias_semana >= 5:
            # Adaptar treinos baseado na fase
            if fase == 'base':
                treinos = [
                    {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve e regenerativa'},
                    {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(50 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua confortável'},
                    {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua em ritmo confortável'},
                    {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': f"{int(50 * volume_mult)} min", 'tipo': 'Fartlek Leve', 'zona': 'Z2 - Aeróbico', 'descricao': '10min aquec + 30min fartlek Z2-Z3 + 10min desaq'},
                    {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': f"{int(35 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve opcional'},
                    {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa em ritmo aeróbico'}
                ]
            elif fase == 'resistencia':
                treinos = [
                    {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida regenerativa'},
                    {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Tempo Run', 'zona': 'Z3 - Tempo', 'descricao': '15min aquec + 30min Z3 + 15min desaq'},
                    {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua moderada'},
                    {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': f"{int(55 * volume_mult)} min", 'tipo': 'Progressivo', 'zona': 'Z2 - Aeróbico', 'descricao': '15min Z2 + 25min Z3 + 15min Z2'},
                    {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': f"{int(30 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve'},
                    {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': f"{int(100 * volume_mult)} min", 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa com 20min finais Z3'}
                ]
            elif fase == 'velocidade':
                treinos = [
                    {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida regenerativa'},
                    {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 6x1km Z4 (rec 2min) + 10min desaq'},
                    {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua confortável'},
                    {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': f"{int(55 * volume_mult)} min", 'tipo': 'Fartlek', 'zona': 'Z3 - Tempo', 'descricao': '15min aquec + 8x(2min Z4 + 2min Z2) + 10min desaq'},
                    {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': f"{int(30 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve'},
                    {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa em ritmo aeróbico'}
                ]
            elif fase == 'potencia':
                treinos = [
                    {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida regenerativa'},
                    {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'VO2max', 'zona': 'Z5 - VO2max', 'descricao': '15min aquec + 5x(4min Z5 + 3min rec) + 10min desaq'},
                    {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua confortável'},
                    {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': f"{int(50 * volume_mult)} min", 'tipo': 'Tempo Run', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 20min Z4 + 15min desaq'},
                    {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': f"{int(30 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve'},
                    {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': f"{int(75 * volume_mult)} min", 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa moderada'}
                ]
            else:  # polimento
                treinos = [
                    {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': f"{int(30 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida muito leve'},
                    {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': f"{int(40 * volume_mult)} min", 'tipo': 'Técnica + Estímulos', 'zona': 'Z3 - Tempo', 'descricao': '15min aquec + 4x(2min Z4 + 3min rec) + 10min desaq'},
                    {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': f"{int(30 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve'},
                    {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': f"{int(35 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida confortável'},
                    {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': f"{int(25 * volume_mult)} min", 'tipo': 'Shakeout', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve + alongamentos'},
                    {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '0 min', 'tipo': 'DIA DA PROVA', 'zona': 'Competição', 'descricao': '🏁 DIA DA MARATONA - Boa sorte!'}
                ]
        elif self.athlete.dias_semana >= 3:
            treinos = [
                {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': '50 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 6x800m (rec 2min) + 10min desaq'},
                {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua moderada'},
                {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '75 min', 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa progressiva'}
            ]
        else:
            treinos = [
                {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '10min aquec + 4x1km (rec 2min) + 10min desaq'},
                {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '60 min', 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa em ritmo confortável'}
            ]
        
        return treinos[:self.athlete.dias_semana]
    
    def _generate_swimming_week(self, info_semana: Dict = None) -> List[Dict]:
        """Gera treinos de natação"""
        if info_semana is None:
            info_semana = {'volume_multiplicador': 1.0}
        
        volume_mult = info_semana['volume_multiplicador']
        
        if self.athlete.dias_semana >= 5:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquec + 8x50m drill + 10x100m técnica + 300m desaq'},
                {'dia': 'Terça', 'modalidade': 'Natação', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Velocidade', 'zona': 'Z5 - VO2max', 'descricao': '800m aquec + 12x50m sprint (rec 30s) + 400m desaq'},
                {'dia': 'Quarta', 'modalidade': 'Natação', 'duracao': f"{int(50 * volume_mult)} min", 'tipo': 'Aeróbico', 'zona': 'Z2 - Aeróbico', 'descricao': '2500m contínuo em ritmo confortável'},
                {'dia': 'Quinta', 'modalidade': 'Natação', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '600m aquec + 10x200m (rec 30s) + 400m desaq'},
                {'dia': 'Sexta', 'modalidade': 'Natação', 'duracao': f"{int(45 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': '2000m contínuo suave'},
                {'dia': 'Sábado', 'modalidade': 'Natação', 'duracao': f"{int(70 * volume_mult)} min", 'tipo': 'Volume', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquec + 20x100m (rec 15s) + 500m desaq'}
            ]
        elif self.athlete.dias_semana >= 3:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '800m aquec + 6x50m drill + 8x100m técnica + 300m desaq'},
                {'dia': 'Quarta', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '600m aquec + 8x200m (rec 30s) + 400m desaq'},
                {'dia': 'Sábado', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Volume', 'zona': 'Z2 - Aeróbico', 'descricao': '3000m contínuo com foco na técnica'}
            ]
        else:
            treinos = [
                {'dia': 'Terça', 'modalidade': 'Natação', 'duracao': '50 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '600m aquec + 5x100m técnica + 200m desaq'},
                {'dia': 'Sábado', 'modalidade': 'Natação', 'duracao': '55 min', 'tipo': 'Volume', 'zona': 'Z2 - Aeróbico', 'descricao': '2500m contínuo moderado'}
            ]
        
        return treinos[:self.athlete.dias_semana]
    
    def _generate_cycling_week(self, info_semana: Dict = None) -> List[Dict]:
        """Gera treinos de ciclismo"""
        if info_semana is None:
            info_semana = {'volume_multiplicador': 1.0}
        
        volume_mult = info_semana['volume_multiplicador']
        
        if self.athlete.dias_semana >= 5:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Ciclismo', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Pedalada suave em terreno plano'},
                {'dia': 'Terça', 'modalidade': 'Ciclismo', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Intervalado', 'zona': 'Z5 - VO2max', 'descricao': '20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq'},
                {'dia': 'Quarta', 'modalidade': 'Ciclismo', 'duracao': f"{int(75 * volume_mult)} min", 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante em terreno variado'},
                {'dia': 'Quinta', 'modalidade': 'Ciclismo', 'duracao': f"{int(90 * volume_mult)} min", 'tipo': 'Sweet Spot', 'zona': 'Z4 - Limiar', 'descricao': '20min aquec + 3x15min no limiar (rec 5min) + 15min desaq'},
                {'dia': 'Sexta', 'modalidade': 'Ciclismo', 'duracao': f"{int(60 * volume_mult)} min", 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Pedalada regenerativa'},
                {'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': f"{int(180 * volume_mult)} min", 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo com simulação de prova'}
            ]
        elif self.athlete.dias_semana >= 3:
            treinos = [
                {'dia': 'Terça', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '20min aquec + 4x10min alta intensidade (rec 4min) + 15min desaq'},
                {'dia': 'Quinta', 'modalidade': 'Ciclismo', 'duracao': '75 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante moderado'},
                {'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': '150 min', 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo progressivo'}
            ]
        else:
            treinos = [
                {'dia': 'Quarta', 'modalidade': 'Ciclismo', 'duracao': '75 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '20min aquec + 3x12min no limiar (rec 4min) + 10min desaq'},
                {'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': '120 min', 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo em ritmo confortável'}
            ]
        
        return treinos[:self.athlete.dias_semana]


class ExcelExporter:
    """Exporta planilhas de treinamento para Excel"""
    
    def __init__(self, athlete: Athlete, training_plan: List[Dict], is_full_plan: bool = False):
        self.athlete = athlete
        self.training_plan = training_plan
        self.zones = TrainingZones(athlete.limiar_lactato, athlete.vo2_max)
        self.is_full_plan = is_full_plan
    
    def export_to_excel(self, filename: str = None):
        """Exporta o plano para Excel com formatação profissional"""
        # Definir diretório de exportação
        export_dir = Path(__file__).parent.parent / 'data' / 'exports'
        export_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Plano_Treinamento_{self.athlete.nome.replace(' ', '_')}_{timestamp}.xlsx"
        
        # Garantir que o filename tenha apenas o nome do arquivo, não o caminho completo
        filename = Path(filename).name
        
        # Caminho completo do arquivo
        filepath = export_dir / filename
        
        # Criar DataFrame principal
        df_treinos = pd.DataFrame(self.training_plan)
        
        # Adicionar coluna de intensidade
        df_treinos['Intensidade'] = df_treinos['zona'].apply(
            lambda x: self.zones.get_intensity_value(x)
        )
        
        # Reordenar colunas baseado se é plano completo ou não
        if self.is_full_plan and 'semana' in df_treinos.columns:
            df_treinos = df_treinos[['semana', 'fase', 'tipo_semana', 'dia', 'modalidade', 'duracao', 'tipo', 'zona', 'Intensidade', 'descricao']]
            df_treinos.columns = ['Semana', 'Fase', 'Tipo Semana', 'Dia', 'Modalidade', 'Duração', 'Tipo', 'Zona', 'Intensidade (FC)', 'Descrição do Treino']
        else:
            # Remover colunas de periodização se existirem (plano de 1 semana)
            cols_to_keep = ['dia', 'modalidade', 'duracao', 'tipo', 'zona', 'Intensidade', 'descricao']
            df_treinos = df_treinos[[col for col in cols_to_keep if col in df_treinos.columns or col == 'Intensidade']]
            df_treinos.columns = ['Dia', 'Modalidade', 'Duração', 'Tipo', 'Zona', 'Intensidade (FC)', 'Descrição do Treino']
        
        # Criar DataFrame com informações do profissional responsável e do atleta
        campos_prof = ['PROFISSIONAL RESPONSÁVEL', '', '', '']
        valores_prof = ['', '', '', '']
        
        campos_prof.extend(['Nome Completo', 'CPF', 'CREF'])
        valores_prof.extend([
            self.athlete.trainer.nome_completo,
            self.athlete.trainer.formatar_cpf(),
            self.athlete.trainer.formatar_cref()
        ])
        
        campos_prof.extend(['', 'DADOS DO ATLETA', '', ''])
        valores_prof.extend(['', '', '', ''])
        
        # Criar DataFrame com informações do atleta
        campos = [
            'Nome', 'Idade', 'Gênero', 'Peso', 'Altura', 'IMC', 'Esporte', 
            'Distância da Prova', 'Dias por Semana', 'Limiar de Lactato', 'VO2 Max'
        ]
        valores = [
            self.athlete.nome,
            f"{self.athlete.idade} anos",
            self.athlete.genero.capitalize(),
            f"{self.athlete.peso} kg",
            f"{self.athlete.altura} cm",
            f"{self.athlete.imc}",
            self.athlete.esporte,
            self.athlete.distancia_prova,
            f"{self.athlete.dias_semana} dias",
            f"{self.athlete.limiar_lactato} bpm",
            f"{self.athlete.vo2_max} ml/kg/min"
        ]
        
        # Adicionar fase menstrual se aplicável
        if self.athlete.genero.lower() == 'feminino' and self.athlete.fase_menstrual:
            campos.append('Fase do Ciclo Menstrual')
            valores.append(self.athlete.fase_menstrual.capitalize())
        
        # Combinar informações do profissional e do atleta
        campos_prof.extend(campos)
        valores_prof.extend(valores)
        
        info_atleta = {'Campo': campos_prof, 'Valor': valores_prof}
        df_info = pd.DataFrame(info_atleta)
        
        # Criar DataFrame com problemas de saúde (se houver)
        df_saude = None
        if self.athlete.tem_restricoes:
            saude_list = []
            for problema in self.athlete.problemas_saude:
                saude_list.append({
                    'Tipo': problema.tipo,
                    'Descrição': problema.descricao,
                    'Membro Afetado': problema.membro_afetado or 'N/A',
                    'Gravidade': problema.gravidade
                })
            df_saude = pd.DataFrame(saude_list)
        
        # Gerar recomendações de saúde
        generator = TrainingPlanGenerator(self.athlete)
        recomendacoes_texto = generator.health_analysis.get('recomendacoes', [])
        
        # Adicionar recomendações de ciclo menstrual se aplicável
        if generator.menstrual_analysis and generator.menstrual_analysis.get('recomendacoes'):
            recomendacoes_texto.extend(['', '─' * 50, ''])
            recomendacoes_texto.extend(generator.menstrual_analysis['recomendacoes'])
        
        df_recomendacoes = None
        if recomendacoes_texto:
            df_recomendacoes = pd.DataFrame({'Recomendações de Saúde': recomendacoes_texto})
        
        # Criar DataFrame com zonas de treinamento
        zonas_list = []
        for zona_nome, zona_data in self.zones.get_zones().items():
            zonas_list.append({
                'Zona': zona_nome,
                'Descrição': zona_data['desc'],
                'Intensidade (FC)': self.zones.get_intensity_value(zona_nome)
            })
        df_zonas = pd.DataFrame(zonas_list)
        
        # Criar DataFrame de periodização se for plano completo
        df_periodizacao = None
        if self.is_full_plan:
            periodization = PeriodizationPlanner(self.athlete.semanas_ate_prova, self.athlete.esporte)
            distribuicao = periodization.calcular_distribuicao_fases()
            
            period_list = []
            for bloco in distribuicao:
                fase_config = periodization.fase_config[bloco['fase']]
                semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
                period_list.append({
                    'Fase': fase_config['nome'],
                    'Semanas': f"{bloco['semana_inicio']}-{bloco['semana_fim']}",
                    'Total de Semanas': semanas,
                    'Descrição': fase_config['descricao'],
                    'Foco': fase_config['intensidade'].replace('_', ' ').title(),
                    'Volume Base': f"{int(fase_config['volume'] * 100)}%"
                })
            df_periodizacao = pd.DataFrame(period_list)
        
        # Exportar para Excel com múltiplas abas
        with pd.ExcelWriter(str(filepath), engine='openpyxl') as writer:
            # Aba de informações
            df_info.to_excel(writer, sheet_name='Informações do Atleta', index=False)
            
            # Aba de periodização (se plano completo)
            if df_periodizacao is not None:
                df_periodizacao.to_excel(writer, sheet_name='Periodização', index=False)
            
            # Aba do plano de treinamento
            sheet_name = 'Plano Completo' if self.is_full_plan else 'Plano Semanal'
            df_treinos.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Aba de zonas de treinamento
            df_zonas.to_excel(writer, sheet_name='Zonas de Treinamento', index=False)
            
            # Aba de problemas de saúde (se houver)
            if df_saude is not None:
                df_saude.to_excel(writer, sheet_name='Problemas de Saúde', index=False)
            
            # Aba de recomendações de saúde (se houver)
            if df_recomendacoes is not None:
                df_recomendacoes.to_excel(writer, sheet_name='Recomendações Médicas', index=False)
            
            # Ajustar largura das colunas
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 60)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return str(filepath)


def main():
    """Função principal para execução do programa"""
    print("=" * 70)
    print("SISTEMA DE GERAÇÃO DE PLANILHAS DE TREINAMENTO ESPORTIVO")
    print("=" * 70)
    print("\nModalidades disponíveis: Triathlon, Corrida, Natação, Ciclismo")
    print()
    
    # Coleta de dados do atleta
    print("\n📝 DADOS BÁSICOS DO ATLETA")
    print("─" * 70)
    nome = input("Nome do atleta [Ex: João Silva, Maria Santos]: ").strip()
    
    while True:
        try:
            idade = int(input("Idade [Número inteiro, 10-100 anos | Ex: 25, 40, 62]: "))
            if 10 <= idade <= 100:
                break
            print("❌ Idade fora do intervalo permitido. Digite um valor entre 10 e 100 anos.")
        except ValueError:
            print("❌ Formato inválido. Digite apenas números (sem vírgulas ou pontos).")
    
    while True:
        try:
            peso = float(input("Peso em kg [Formato: 00.0, 30-200 kg | Ex: 65.5, 72, 80.3]: "))
            if 30 <= peso <= 200:
                break
            print("❌ Peso fora do intervalo permitido. Digite um valor entre 30 e 200 kg.")
        except ValueError:
            print("❌ Formato inválido. Use ponto (.) para decimais. Ex: 72.5")
    
    while True:
        try:
            altura = float(input("Altura em cm [Formato: 000, 100-250 cm | Ex: 170, 182.5, 165]: "))
            if 100 <= altura <= 250:
                break
            print("❌ Altura fora do intervalo permitido. Digite um valor entre 100 e 250 cm.")
        except ValueError:
            print("❌ Formato inválido. Digite apenas números. Ex: 175")
    
    while True:
        genero = input("Gênero [Digite: Masculino OU Feminino | Aceita: M, F, masculino, feminino]: ").strip().capitalize()
        if genero in ['Masculino', 'Feminino', 'M', 'F']:
            genero = 'Masculino' if genero in ['Masculino', 'M'] else 'Feminino'
            break
        print("❌ Opção inválida. Digite 'Masculino' ou 'Feminino' (ou apenas M/F).")
    
    print("\n🏃 MODALIDADE ESPORTIVA")
    print("─" * 70)
    print("Opções disponíveis: 1-Triathlon | 2-Corrida | 3-Natação | 4-Ciclismo")
    while True:
        esporte = input("Esporte [Digite o nome completo ou número | Ex: Triathlon, 1, Corrida, 2]: ").strip().capitalize()
        if esporte in ['Triathlon', 'Corrida', 'Natação', 'Ciclismo', '1', '2', '3', '4']:
            esporte_map = {'1': 'Triathlon', '2': 'Corrida', '3': 'Natação', '4': 'Ciclismo'}
            esporte = esporte_map.get(esporte, esporte)
            break
        print("❌ Modalidade inválida. Escolha: Triathlon, Corrida, Natação ou Ciclismo (ou 1-4).")
    
    print("\n📅 DISPONIBILIDADE DE TREINO")
    print("─" * 70)
    while True:
        try:
            dias_semana = int(input("Dias de treino por semana [Número inteiro, 2-7 dias | Ex: 3, 5, 7]: "))
            if 2 <= dias_semana <= 7:
                break
            print("❌ Valor fora do intervalo. Digite um número entre 2 (mínimo) e 7 (todos os dias).")
        except ValueError:
            print("❌ Formato inválido. Digite apenas um número de 2 a 7.")
    
    # Coletar semanas até a prova (com opção de calcular automaticamente)
    print("\n" + "═" * 70)
    print("📅 CONFIGURAÇÃO DO PERÍODO DE TREINAMENTO")
    print("═" * 70)
    
    while True:
        opcao_semanas = input("\nVocê sabe quantas semanas faltam até a prova? [Digite: S ou N | Aceita: s, n, sim, não]: ").strip().lower()
        if opcao_semanas in ['s', 'n', 'sim', 'nao', 'não']:
            opcao_semanas = 's' if opcao_semanas in ['s', 'sim'] else 'n'
            break
        print("❌ Resposta inválida. Digite 'S' para sim ou 'N' para não.")
    
    if opcao_semanas == 's':
        # Usuário sabe o número de semanas
        while True:
            try:
                semanas_ate_prova = int(input("\nSemanas até a prova [Número inteiro, 1-52 semanas | Ex: 8, 16, 24, 52]: "))
                if 1 <= semanas_ate_prova <= 52:
                    break
                
                # Mensagem de limite excedido
                print("\n" + "⚠" * 70)
                print("⚠️  LIMITE DE PLANEJAMENTO EXCEDIDO")
                print("⚠" * 70)
                print(f"   Valor informado: {semanas_ate_prova} semanas")
                print(f"   Limite do sistema: 52 semanas (aproximadamente 1 ano)")
                print("\n📋 MOTIVO DA LIMITAÇÃO:")
                print("   • O sistema foi projetado para periodização de até 1 ano")
                print("   • Planejamentos acima de 52 semanas requerem reavaliações periódicas")
                print("   • Fatores imprevisíveis aumentam significativamente após 1 ano")
                print("   • Recomenda-se criar planos em ciclos anuais")
                print("\n💡 SUGESTÃO:")
                print("   Planeje até a próxima reavaliação (máximo 52 semanas)")
                print("   Após esse período, gere um novo plano atualizado.")
                print("⚠" * 70)
                print("\nPor favor, insira um valor entre 1 e 52 semanas.\n")
            except ValueError:
                print("\n❌ Erro: Por favor, insira um número válido.")
    else:
        # Calcular automaticamente baseado na data da prova
        print("\n💡 Vamos calcular automaticamente baseado na data da prova!")
        print("   Formato obrigatório: DD/MM/AAAA (dia com 2 dígitos, mês com 2 dígitos, ano com 4 dígitos)")
        
        while True:
            try:
                data_prova = input("\nData da prova [Formato: DD/MM/AAAA | Ex: 15/08/2026, 03/12/2026, 25/04/2027]: ").strip()
                semanas_ate_prova = calcular_semanas_ate_prova(data_prova)
                
                # Validar se está dentro do limite
                if semanas_ate_prova > 52:
                    data_prova_obj = datetime.strptime(data_prova, "%d/%m/%Y")
                    dias_totais = (data_prova_obj - datetime.now()).days
                    meses_aproximados = round(semanas_ate_prova / 4.33, 1)
                    
                    print("\n" + "⚠" * 70)
                    print("⚠️  LIMITE DE PLANEJAMENTO EXCEDIDO")
                    print("⚠" * 70)
                    print(f"   📅 Data da prova informada: {data_prova_obj.strftime('%d/%m/%Y (%A)')}")
                    print(f"   📊 Dias até a prova: {dias_totais} dias")
                    print(f"   📆 Semanas calculadas: {semanas_ate_prova} semanas (~{meses_aproximados} meses)")
                    print(f"   🚫 Limite do sistema: 52 semanas (aproximadamente 1 ano)")
                    print("\n📋 MOTIVO DA LIMITAÇÃO:")
                    print("   • O sistema não está capacitado para planejamentos acima de 1 ano")
                    print("   • Periodização acima de 52 semanas requer acompanhamento profissional contínuo")
                    print("   • Mudanças fisiológicas e de objetivos são muito prováveis nesse período")
                    print("   • A ciência do treinamento recomenda ciclos anuais com reavaliações")
                    print("\n💡 OPÇÕES DISPONÍVEIS:")
                    print("   1. Ajustar para 52 semanas (planejamento até próxima avaliação)")
                    print("   2. Informar uma data mais próxima (até 1 ano a partir de hoje)")
                    print("⚠" * 70)
                    
                    confirmar = input("\n   Deseja usar o limite máximo de 52 semanas? (s/n): ").strip().lower()
                    if confirmar == 's':
                        semanas_ate_prova = 52
                        print("\n✅ Configurado: 52 semanas de treinamento (máximo permitido)")
                        print("   Após esse período, recomenda-se gerar um novo plano atualizado.\n")
                        break
                    print("\n   Por favor, informe uma data dentro do limite de 1 ano.\n")
                    continue
                
                # Mostrar resultado do cálculo
                data_prova_obj = datetime.strptime(data_prova, "%d/%m/%Y")
                dias_totais = (data_prova_obj - datetime.now()).days
                
                print("\n" + "─" * 70)
                print(f"✅ Cálculo realizado com sucesso!")
                print(f"   📅 Data da prova: {data_prova_obj.strftime('%d/%m/%Y (%A)')}")
                print(f"   📊 Dias até a prova: {dias_totais} dias")
                print(f"   📆 Semanas de treinamento: {semanas_ate_prova} semanas")
                print("─" * 70)
                break
                
            except ValueError as e:
                print(f"\n❌ Erro: {e}")
                print("   Tente novamente.")
    
    # Distâncias disponíveis por esporte
    distancias_opcoes = {
        'Triathlon': ['Sprint', 'Olímpico', 'Meio Ironman', 'Ironman'],
        'Corrida': ['5K', '10K', 'Meia Maratona', 'Maratona'],
        'Natação': ['1500m', '3000m', '5000m'],
        'Ciclismo': ['40K', '80K', '160K']
    }
    
    print(f"\n🎯 DISTÂNCIA DA PROVA - {esporte.upper()}")
    print("─" * 70)
    print("Distâncias disponíveis:")
    for i, dist in enumerate(distancias_opcoes[esporte], 1):
        print(f"  {i}. {dist}")
    
    while True:
        try:
            escolha = int(input(f"Escolha a distância [Número 1-{len(distancias_opcoes[esporte])} | Digite apenas o número]: "))
            if 1 <= escolha <= len(distancias_opcoes[esporte]):
                distancia_prova = distancias_opcoes[esporte][escolha - 1]
                break
            print(f"❌ Opção inválida. Digite um número entre 1 e {len(distancias_opcoes[esporte])}.")
        except ValueError:
            print("❌ Formato inválido. Digite apenas o número correspondente à opção desejada.")
    
    print("\n💓 DADOS FISIOLÓGICOS")
    print("─" * 70)
    while True:
        try:
            limiar_lactato = float(input("Limiar de Lactato em bpm [Número, 100-220 | Ex: 165, 172.5, 180]: "))
            if 100 <= limiar_lactato <= 220:
                break
            print("❌ Valor fora do intervalo. O limiar deve estar entre 100 e 220 bpm.")
        except ValueError:
            print("❌ Formato inválido. Digite um número (pode usar ponto para decimais). Ex: 170")
    
    while True:
        try:
            vo2_max = float(input("VO2 Max em ml/kg/min [Número, 20-90 | Ex: 45.5, 52, 68.3]: "))
            if 20 <= vo2_max <= 90:
                break
            print("❌ Valor fora do intervalo. O VO2 Max deve estar entre 20 e 90 ml/kg/min.")
        except ValueError:
            print("❌ Formato inválido. Digite um número (pode usar ponto para decimais). Ex: 55.5")
    
    # Coleta de problemas de saúde
    print("\n" + "=" * 70)
    print("INFORMAÇÕES DE SAÚDE")
    print("=" * 70)
    
    problemas_saude = []
    
    while True:
        tem_problema = input("\nO atleta possui algum problema de saúde? [Digite: S ou N | Aceita: s, n, sim, não]: ").strip().lower()
        if tem_problema in ['s', 'n', 'sim', 'nao', 'não']:
            tem_problema = 's' if tem_problema in ['s', 'sim'] else 'n'
            break
        print("❌ Resposta inválida. Digite 'S' para sim ou 'N' para não.")
    
    if tem_problema == 's':
        print("\n🏥 TIPOS DE PROBLEMAS DE SAÚDE")
        print("─" * 70)
        print("Categorias disponíveis:")
        print("  1. Ortopédico (lesões musculares, articulares, ósseas)")
        print("  2. Asma ou problemas respiratórios")
        print("  3. Diabetes")
        print("  4. Hipertensão")
        print("  5. Outro")
        
        while True:
            adicionar_mais = True
            
            while True:
                try:
                    tipo_problema = int(input("\nTipo de problema [Número 1-5 | Digite apenas o número da categoria]: "))
                    if 1 <= tipo_problema <= 5:
                        break
                    print("❌ Opção inválida. Escolha um número entre 1 e 5.")
                except ValueError:
                    print("❌ Formato inválido. Digite apenas o número correspondente à categoria.")
            
            tipos_map = {
                1: 'ortopédico',
                2: 'asma',
                3: 'diabetes',
                4: 'hipertensão',
                5: 'outro'
            }
            
            tipo = tipos_map[tipo_problema]
            descricao = input("Descrição do problema [Texto livre | Ex: Tendinite patelar, Asma induzida por exercício]: ").strip()
            
            membro_afetado = None
            if tipo == 'ortopédico':
                print("\n🦴 Especificar região afetada:")
                print("   Formato: [região]_[lado] ou apenas [região] se bilateral/central")
                print("   Exemplos válidos: joelho_direito, ombro_esquerdo, tornozelo_direito, ")
                print("                     lombar, quadril_esquerdo, pé_direito, cervical")
                membro_afetado = input("Membro/região afetada [Ex: joelho_direito, lombar]: ").strip().lower()
            
            print("\n⚠️ Nível de gravidade:")
            print("  1. Leve (desconforto ocasional, não impede treinos)")
            print("  2. Moderado (dor regular, requer adaptações nos treinos)")
            print("  3. Grave (limitação significativa, requer supervisão médica)")
            
            while True:
                try:
                    grav = int(input("Gravidade [Número 1-3 | Digite apenas o número]: "))
                    if 1 <= grav <= 3:
                        break
                    print("❌ Opção inválida. Escolha 1 (leve), 2 (moderado) ou 3 (grave).")
                except ValueError:
                    print("❌ Formato inválido. Digite apenas um número de 1 a 3.")
            
            gravidade_map = {1: 'leve', 2: 'moderado', 3: 'grave'}
            
            problema = HealthIssue(
                tipo=tipo,
                descricao=descricao,
                membro_afetado=membro_afetado,
                gravidade=gravidade_map[grav]
            )
            
            problemas_saude.append(problema)
            
            # Análise imediata com IA
            advisor = HealthAdvisor()
            analise = advisor.analyze_health_issues([problema], esporte)
            
            if analise['recomendacoes']:
                print("\n" + "─" * 70)
                print("🤖 ANÁLISE DE IA - RECOMENDAÇÕES:")
                print("─" * 70)
                for rec in analise['recomendacoes']:
                    print(rec)
                print("─" * 70)
            
            while True:
                mais = input("\nAdicionar outro problema de saúde? [Digite: S ou N | Aceita: s, n, sim, não]: ").strip().lower()
                if mais in ['s', 'n', 'sim', 'nao', 'não']:
                    adicionar_mais = (mais in ['s', 'sim'])
                    break
                print("❌ Resposta inválida. Digite 'S' para adicionar mais ou 'N' para finalizar.")
            
            if not adicionar_mais:
                break
    
    # Coleta de fase menstrual (apenas para mulheres)
    fase_menstrual = None
    if genero.lower() == 'feminino':
        print("\n" + "=" * 70)
        print("🌸 INFORMAÇÕES SOBRE CICLO MENSTRUAL")
        print("=" * 70)
        print("\nA IA pode ajustar os treinos baseado na fase do ciclo menstrual.")
        print("Isso ajuda a otimizar performance e prevenir overtraining.\n")
        
        while True:
            informar_fase = input("Deseja informar a fase do ciclo menstrual? [Digite: S ou N | Aceita: s, n, sim, não]: ").strip().lower()
            if informar_fase in ['s', 'n', 'sim', 'nao', 'não']:
                informar_fase = 's' if informar_fase in ['s', 'sim'] else 'n'
                break
            print("❌ Resposta inválida. Digite 'S' para sim ou 'N' para não.")
        
        if informar_fase == 's':
            print("\n📅 Fases do ciclo menstrual:")
            print("─" * 70)
            print("  1. Menstrual (Dias 1-5) - Período menstrual")
            print("  2. Folicular (Dias 6-14) - Fase ideal para treinos intensos")
            print("  3. Ovulatória (Dias 13-16) - Pico de performance")
            print("  4. Lútea (Dias 17-28) - Fase pré-menstrual")
            
            while True:
                try:
                    fase_escolha = int(input("\nFase atual [Número 1-4 | Digite apenas o número da fase]: "))
                    if 1 <= fase_escolha <= 4:
                        fases_map = {1: 'menstrual', 2: 'folicular', 3: 'ovulatoria', 4: 'lutea'}
                        fase_menstrual = fases_map[fase_escolha]
                        break
                    print("❌ Opção inválida. Escolha um número entre 1 e 4.")
                except ValueError:
                    print("❌ Formato inválido. Digite apenas um número de 1 a 4.")
            
            print(f"\n✅ Fase registrada: {fase_menstrual.capitalize()}")
            print("Os treinos serão ajustados automaticamente pela IA.")
    
    # Criar objeto do atleta
    atleta = Athlete(
        nome=nome,
        idade=idade,
        peso=peso,
        altura=altura,
        esporte=esporte,
        dias_semana=dias_semana,
        distancia_prova=distancia_prova,
        limiar_lactato=limiar_lactato,
        vo2_max=vo2_max,
        genero=genero,
        semanas_ate_prova=semanas_ate_prova,
        problemas_saude=problemas_saude,
        fase_menstrual=fase_menstrual
    )
    
    print("\n" + "=" * 70)
    print("GERANDO PLANO DE TREINAMENTO...")
    print("=" * 70)
    
    # Mostrar dados antropométricos
    print(f"\n📊 Dados do Atleta:")
    print(f"   Nome: {nome}")
    print(f"   Idade: {idade} anos | Peso: {peso} kg | Altura: {altura} cm")
    print(f"   IMC: {atleta.imc} kg/m²")
    print(f"   Semanas até a prova: {semanas_ate_prova}")
    
    # Gerar plano de treinamento
    generator = TrainingPlanGenerator(atleta)
    
    # Mostrar distribuição das fases
    print(f"\n📅 PERIODIZAÇÃO DO TREINAMENTO:")
    print("─" * 70)
    distribuicao = generator.periodization.calcular_distribuicao_fases()
    for bloco in distribuicao:
        fase_config = generator.periodization.fase_config[bloco['fase']]
        semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
        print(f"  📌 Semanas {bloco['semana_inicio']}-{bloco['semana_fim']} ({semanas} sem): {fase_config['nome']}")
        print(f"     {fase_config['descricao']}")
    print("─" * 70)
    
    # Gerar plano completo
    plano_completo = generator.get_full_training_plan()
    plano_semanal = generator.get_weekly_training(1)  # Primeira semana para preview
    
    # Exibir recomendações de saúde se houver
    if atleta.tem_restricoes and generator.health_analysis['recomendacoes']:
        print("\n" + "━" * 70)
        print("🏥 RECOMENDAÇÕES MÉDICAS APLICADAS AO TREINAMENTO:")
        print("━" * 70)
        for rec in generator.health_analysis['recomendacoes']:
            print(rec)
        print("━" * 70)
    
    # Exibir recomendações de ciclo menstrual se houver
    if generator.menstrual_analysis and generator.menstrual_analysis.get('recomendacoes'):
        print("\n" + "━" * 70)
        print("🌸 RECOMENDAÇÕES BASEADAS NO CICLO MENSTRUAL:")
        print("━" * 70)
        for rec in generator.menstrual_analysis['recomendacoes']:
            print(rec)
        print("━" * 70)
    
    # Exibir resumo do plano completo
    print(f"\n📋 RESUMO DO PLANO DE TREINAMENTO:")
    print("═" * 70)
    print(f"   Atleta: {nome}")
    print(f"   Esporte: {esporte} - Distância: {distancia_prova}")
    print(f"   Total de semanas: {semanas_ate_prova}")
    print(f"   Total de treinos: {len(plano_completo)}")
    print(f"   Treinos por semana: {len(plano_semanal)}")
    print("═" * 70)
    
    # Exibir preview da primeira semana
    print(f"\n📅 PREVIEW - SEMANA 1 ({plano_semanal[0]['fase']} - {plano_semanal[0]['tipo_semana']}):")
    print("─" * 70)
    
    for treino in plano_semanal:
        print(f"📅 {treino['dia']} - {treino['modalidade']}")
        print(f"   ⏱️  Duração: {treino['duracao']}")
        print(f"   🎯 Tipo: {treino['tipo']} ({treino['zona']})")
        print(f"   📝 {treino['descricao']}")
        print()
    
    print("─" * 70)
    print(f"💡 O plano completo de {semanas_ate_prova} semanas será exportado para Excel")
    print("─" * 70)
    
    # Exportar para Excel
    while True:
        exportar = input("\nDeseja exportar para Excel? (s/n): ").strip().lower()
        if exportar in ['s', 'n']:
            break
        print("Por favor, responda 's' para sim ou 'n' para não.")
    
    if exportar == 's':
        # Escolher entre plano completo ou apenas primeira semana
        if semanas_ate_prova > 1:
            while True:
                tipo_export = input(f"\nExportar plano COMPLETO ({semanas_ate_prova} semanas) ou apenas PRIMEIRA SEMANA? (c/p): ").strip().lower()
                if tipo_export in ['c', 'p']:
                    break
                print("Por favor, responda 'c' para completo ou 'p' para primeira semana.")
            
            if tipo_export == 'c':
                exporter = ExcelExporter(atleta, plano_completo, is_full_plan=True)
                print(f"\n⏳ Gerando planilha completa com {len(plano_completo)} treinos...")
            else:
                exporter = ExcelExporter(atleta, plano_semanal, is_full_plan=False)
        else:
            exporter = ExcelExporter(atleta, plano_semanal, is_full_plan=False)
        
        filename_custom = input("Nome do arquivo (deixe em branco para nome automático): ").strip()
        if filename_custom and not filename_custom.endswith('.xlsx'):
            filename_custom += '.xlsx'
        
        filename = exporter.export_to_excel(filename_custom if filename_custom else None)
        print(f"\n✅ Planilha exportada com sucesso: {filename}")
        print(f"📂 Local: {os.path.abspath(filename)}")
    else:
        print("\nPlanilha não exportada.")
    
    print("\n" + "=" * 70)
    print("Obrigado por usar o Sistema de Treinamento!")
    print("=" * 70)


if __name__ == "__main__":
    main()
