"""
Sistema de Geração de Planilhas de Treinamento Esportivo
Modalidades: Triathlon, Corrida, Natação e Ciclismo
"""

import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import os


@dataclass
class HealthIssue:
    """Classe para armazenar problemas de saúde"""
    tipo: str  # ortopédico, cardíaco, respiratório, metabólico
    descricao: str
    membro_afetado: Optional[str] = None  # joelho_direito, ombro_esquerdo, etc.
    gravidade: str = "leve"  # leve, moderado, grave
    restricoes: List[str] = field(default_factory=list)


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
    problemas_saude: List[HealthIssue] = field(default_factory=list)
    
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
    
    def get_weekly_training(self) -> List[Dict]:
        """Gera treinos para uma semana"""
        # Gerar treinos base
        if self.athlete.esporte.lower() == 'triathlon':
            treinos = self._generate_triathlon_week()
        elif self.athlete.esporte.lower() == 'corrida':
            treinos = self._generate_running_week()
        elif self.athlete.esporte.lower() == 'natação':
            treinos = self._generate_swimming_week()
        elif self.athlete.esporte.lower() == 'ciclismo':
            treinos = self._generate_cycling_week()
        else:
            raise ValueError("Esporte não reconhecido")
        
        # Aplicar adequações baseadas em problemas de saúde
        if self.athlete.tem_restricoes:
            treinos = self._apply_health_adjustments(treinos)
        
        return treinos
    
    def _apply_health_adjustments(self, treinos: List[Dict]) -> List[Dict]:
        """Aplica adequações aos treinos baseadas em problemas de saúde"""
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
            
            treinos_ajustados.append(treino_ajustado)
        
        return treinos_ajustados
    
    def _generate_triathlon_week(self) -> List[Dict]:
        """Gera treinos de triathlon"""
        volume = self.distance_config.get(self.athlete.distancia_prova, {}).get('volume', 'médio')
        
        # Templates baseados nos dias disponíveis
        if self.athlete.dias_semana >= 6:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquecimento + 8x100m técnica + 500m volta à calma'},
                {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 6x800m (rec 2min) + 10min desaq'},
                {'dia': 'Quarta', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante em terreno plano'},
                {'dia': 'Quinta', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Intervalado', 'zona': 'Z3 - Tempo', 'descricao': '500m aquec + 10x200m (rec 30s) + 300m desaq'},
                {'dia': 'Sexta', 'modalidade': 'Corrida', 'duracao': '40 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve e contínua'},
                {'dia': 'Sábado', 'modalidade': 'Ciclismo', 'duracao': '120 min', 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo com simulação de prova'},
                {'dia': 'Domingo', 'modalidade': 'Brick', 'duracao': '90 min', 'tipo': 'Combinado', 'zona': 'Z3 - Tempo', 'descricao': '60min bike Z2 + 30min corrida Z3'}
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
    
    def _generate_running_week(self) -> List[Dict]:
        """Gera treinos de corrida"""
        volume = self.distance_config.get(self.athlete.distancia_prova, {}).get('volume', 'médio')
        
        if self.athlete.dias_semana >= 5:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Corrida', 'duracao': '40 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve e regenerativa'},
                {'dia': 'Terça', 'modalidade': 'Corrida', 'duracao': '60 min', 'tipo': 'Intervalado', 'zona': 'Z5 - VO2max', 'descricao': '15min aquec + 10x400m (rec 90s) + 10min desaq'},
                {'dia': 'Quarta', 'modalidade': 'Corrida', 'duracao': '45 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida contínua em ritmo confortável'},
                {'dia': 'Quinta', 'modalidade': 'Corrida', 'duracao': '50 min', 'tipo': 'Tempo Run', 'zona': 'Z4 - Limiar', 'descricao': '15min aquec + 20min no limiar + 15min desaq'},
                {'dia': 'Sábado', 'modalidade': 'Corrida', 'duracao': '30 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Corrida leve opcional'},
                {'dia': 'Domingo', 'modalidade': 'Corrida', 'duracao': '90 min', 'tipo': 'Long Run', 'zona': 'Z2 - Aeróbico', 'descricao': 'Corrida longa em ritmo controlado'}
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
    
    def _generate_swimming_week(self) -> List[Dict]:
        """Gera treinos de natação"""
        if self.athlete.dias_semana >= 5:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Técnica', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquec + 8x50m drill + 10x100m técnica + 300m desaq'},
                {'dia': 'Terça', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Velocidade', 'zona': 'Z5 - VO2max', 'descricao': '800m aquec + 12x50m sprint (rec 30s) + 400m desaq'},
                {'dia': 'Quarta', 'modalidade': 'Natação', 'duracao': '50 min', 'tipo': 'Aeróbico', 'zona': 'Z2 - Aeróbico', 'descricao': '2500m contínuo em ritmo confortável'},
                {'dia': 'Quinta', 'modalidade': 'Natação', 'duracao': '60 min', 'tipo': 'Intervalado', 'zona': 'Z4 - Limiar', 'descricao': '600m aquec + 10x200m (rec 30s) + 400m desaq'},
                {'dia': 'Sexta', 'modalidade': 'Natação', 'duracao': '45 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': '2000m contínuo suave'},
                {'dia': 'Sábado', 'modalidade': 'Natação', 'duracao': '70 min', 'tipo': 'Volume', 'zona': 'Z2 - Aeróbico', 'descricao': '1000m aquec + 20x100m (rec 15s) + 500m desaq'}
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
    
    def _generate_cycling_week(self) -> List[Dict]:
        """Gera treinos de ciclismo"""
        if self.athlete.dias_semana >= 5:
            treinos = [
                {'dia': 'Segunda', 'modalidade': 'Ciclismo', 'duracao': '60 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Pedalada suave em terreno plano'},
                {'dia': 'Terça', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Intervalado', 'zona': 'Z5 - VO2max', 'descricao': '20min aquec + 6x5min alta intensidade (rec 3min) + 15min desaq'},
                {'dia': 'Quarta', 'modalidade': 'Ciclismo', 'duracao': '75 min', 'tipo': 'Base', 'zona': 'Z2 - Aeróbico', 'descricao': 'Ritmo constante em terreno variado'},
                {'dia': 'Quinta', 'modalidade': 'Ciclismo', 'duracao': '90 min', 'tipo': 'Sweet Spot', 'zona': 'Z4 - Limiar', 'descricao': '20min aquec + 3x15min no limiar (rec 5min) + 15min desaq'},
                {'dia': 'Sexta', 'modalidade': 'Ciclismo', 'duracao': '60 min', 'tipo': 'Recuperação', 'zona': 'Z1 - Recuperação', 'descricao': 'Pedalada regenerativa'},
                {'dia': 'Domingo', 'modalidade': 'Ciclismo', 'duracao': '180 min', 'tipo': 'Long Ride', 'zona': 'Z2 - Aeróbico', 'descricao': 'Pedal longo com simulação de prova'}
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
    
    def __init__(self, athlete: Athlete, training_plan: List[Dict]):
        self.athlete = athlete
        self.training_plan = training_plan
        self.zones = TrainingZones(athlete.limiar_lactato, athlete.vo2_max)
    
    def export_to_excel(self, filename: str = None):
        """Exporta o plano para Excel com formatação profissional"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Plano_Treinamento_{self.athlete.nome.replace(' ', '_')}_{timestamp}.xlsx"
        
        # Criar DataFrame principal
        df_treinos = pd.DataFrame(self.training_plan)
        
        # Adicionar coluna de intensidade
        df_treinos['Intensidade'] = df_treinos['zona'].apply(
            lambda x: self.zones.get_intensity_value(x)
        )
        
        # Reordenar colunas
        df_treinos = df_treinos[['dia', 'modalidade', 'duracao', 'tipo', 'zona', 'Intensidade', 'descricao']]
        df_treinos.columns = ['Dia', 'Modalidade', 'Duração', 'Tipo', 'Zona', 'Intensidade (FC)', 'Descrição do Treino']
        
        # Criar DataFrame com informações do atleta
        info_atleta = {
            'Campo': [
                'Nome', 'Idade', 'Peso', 'Altura', 'IMC', 'Esporte', 
                'Distância da Prova', 'Dias por Semana', 'Limiar de Lactato', 'VO2 Max'
            ],
            'Valor': [
                self.athlete.nome,
                f"{self.athlete.idade} anos",
                f"{self.athlete.peso} kg",
                f"{self.athlete.altura} cm",
                f"{self.athlete.imc}",
                self.athlete.esporte,
                self.athlete.distancia_prova,
                f"{self.athlete.dias_semana} dias",
                f"{self.athlete.limiar_lactato} bpm",
                f"{self.athlete.vo2_max} ml/kg/min"
            ]
        }
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
        
        # Exportar para Excel com múltiplas abas
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Aba de informações
            df_info.to_excel(writer, sheet_name='Informações do Atleta', index=False)
            
            # Aba do plano de treinamento
            df_treinos.to_excel(writer, sheet_name='Plano Semanal', index=False)
            
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
        
        return filename


def main():
    """Função principal para execução do programa"""
    print("=" * 70)
    print("SISTEMA DE GERAÇÃO DE PLANILHAS DE TREINAMENTO ESPORTIVO")
    print("=" * 70)
    print("\nModalidades disponíveis: Triathlon, Corrida, Natação, Ciclismo")
    print()
    
    # Coleta de dados do atleta
    nome = input("Nome do atleta: ").strip()
    
    while True:
        try:
            idade = int(input("Idade: "))
            if 10 <= idade <= 100:
                break
            print("Por favor, insira uma idade válida (10-100 anos).")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        try:
            peso = float(input("Peso (kg): "))
            if 30 <= peso <= 200:
                break
            print("Por favor, insira um peso válido (30-200 kg).")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        try:
            altura = float(input("Altura (cm): "))
            if 100 <= altura <= 250:
                break
            print("Por favor, insira uma altura válida (100-250 cm).")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        esporte = input("Esporte (Triathlon/Corrida/Natação/Ciclismo): ").strip().capitalize()
        if esporte in ['Triathlon', 'Corrida', 'Natação', 'Ciclismo']:
            break
        print("Por favor, escolha uma modalidade válida.")
    
    while True:
        try:
            dias_semana = int(input("Quantos dias por semana pode treinar? (2-7): "))
            if 2 <= dias_semana <= 7:
                break
            print("Por favor, insira um número entre 2 e 7.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    # Distâncias disponíveis por esporte
    distancias_opcoes = {
        'Triathlon': ['Sprint', 'Olímpico', 'Meio Ironman', 'Ironman'],
        'Corrida': ['5K', '10K', 'Meia Maratona', 'Maratona'],
        'Natação': ['1500m', '3000m', '5000m'],
        'Ciclismo': ['40K', '80K', '160K']
    }
    
    print(f"\nDistâncias disponíveis para {esporte}:")
    for i, dist in enumerate(distancias_opcoes[esporte], 1):
        print(f"{i}. {dist}")
    
    while True:
        try:
            escolha = int(input("Escolha a distância (número): "))
            if 1 <= escolha <= len(distancias_opcoes[esporte]):
                distancia_prova = distancias_opcoes[esporte][escolha - 1]
                break
            print("Por favor, escolha uma opção válida.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        try:
            limiar_lactato = float(input("Limiar de Lactato (bpm): "))
            if 100 <= limiar_lactato <= 220:
                break
            print("Por favor, insira um valor entre 100 e 220 bpm.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    while True:
        try:
            vo2_max = float(input("VO2 Max (ml/kg/min): "))
            if 20 <= vo2_max <= 90:
                break
            print("Por favor, insira um valor entre 20 e 90 ml/kg/min.")
        except ValueError:
            print("Por favor, insira um número válido.")
    
    # Coleta de problemas de saúde
    print("\n" + "=" * 70)
    print("INFORMAÇÕES DE SAÚDE")
    print("=" * 70)
    
    problemas_saude = []
    
    while True:
        tem_problema = input("\nO atleta possui algum problema de saúde? (s/n): ").strip().lower()
        if tem_problema in ['s', 'n']:
            break
        print("Por favor, responda 's' para sim ou 'n' para não.")
    
    if tem_problema == 's':
        print("\nTipos de problemas disponíveis:")
        print("1. Ortopédico (lesões musculares, articulares, ósseas)")
        print("2. Asma ou problemas respiratórios")
        print("3. Diabetes")
        print("4. Hipertensão")
        print("5. Outro")
        
        while True:
            adicionar_mais = True
            
            while True:
                try:
                    tipo_problema = int(input("\nTipo de problema (1-5): "))
                    if 1 <= tipo_problema <= 5:
                        break
                    print("Por favor, escolha entre 1 e 5.")
                except ValueError:
                    print("Por favor, insira um número válido.")
            
            tipos_map = {
                1: 'ortopédico',
                2: 'asma',
                3: 'diabetes',
                4: 'hipertensão',
                5: 'outro'
            }
            
            tipo = tipos_map[tipo_problema]
            descricao = input("Descrição do problema: ").strip()
            
            membro_afetado = None
            if tipo == 'ortopédico':
                print("\nQual membro/região é afetado(a)?")
                print("Exemplos: joelho_direito, ombro_esquerdo, tornozelo_direito, lombar, quadril_esquerdo, pé_direito")
                membro_afetado = input("Membro afetado: ").strip().lower()
            
            print("\nGravidade do problema:")
            print("1. Leve (desconforto ocasional)")
            print("2. Moderado (dor regular, requer cuidados)")
            print("3. Grave (limitação significativa)")
            
            while True:
                try:
                    grav = int(input("Gravidade (1-3): "))
                    if 1 <= grav <= 3:
                        break
                    print("Por favor, escolha entre 1 e 3.")
                except ValueError:
                    print("Por favor, insira um número válido.")
            
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
                mais = input("\nAdicionar outro problema de saúde? (s/n): ").strip().lower()
                if mais in ['s', 'n']:
                    adicionar_mais = (mais == 's')
                    break
                print("Por favor, responda 's' para sim ou 'n' para não.")
            
            if not adicionar_mais:
                break
    
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
        problemas_saude=problemas_saude
    )
    
    print("\n" + "=" * 70)
    print("GERANDO PLANO DE TREINAMENTO...")
    print("=" * 70)
    
    # Mostrar dados antropométricos
    print(f"\n📊 Dados do Atleta:")
    print(f"   Nome: {nome}")
    print(f"   Idade: {idade} anos | Peso: {peso} kg | Altura: {altura} cm")
    print(f"   IMC: {atleta.imc} kg/m²")
    
    # Gerar plano de treinamento
    generator = TrainingPlanGenerator(atleta)
    plano_semanal = generator.get_weekly_training()
    
    # Exibir recomendações de saúde se houver
    if atleta.tem_restricoes and generator.health_analysis['recomendacoes']:
        print("\n" + "━" * 70)
        print("🏥 RECOMENDAÇÕES MÉDICAS APLICADAS AO TREINAMENTO:")
        print("━" * 70)
        for rec in generator.health_analysis['recomendacoes']:
            print(rec)
        print("━" * 70)
    
    # Exibir prévia do plano
    print(f"\n📋 Plano de treinamento para {nome}:")
    print(f"Esporte: {esporte} - Distância: {distancia_prova}")
    print(f"Treinos por semana: {len(plano_semanal)}\n")
    
    for treino in plano_semanal:
        print(f"📅 {treino['dia']} - {treino['modalidade']}")
        print(f"   ⏱️  Duração: {treino['duracao']}")
        print(f"   🎯 Tipo: {treino['tipo']} ({treino['zona']})")
        print(f"   📝 {treino['descricao']}")
        print()
    
    # Exportar para Excel
    exporter = ExcelExporter(atleta, plano_semanal)
    
    while True:
        exportar = input("Deseja exportar para Excel? (s/n): ").strip().lower()
        if exportar in ['s', 'n']:
            break
        print("Por favor, responda 's' para sim ou 'n' para não.")
    
    if exportar == 's':
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
