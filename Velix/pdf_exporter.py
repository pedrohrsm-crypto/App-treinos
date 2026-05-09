"""
Sistema de Exportação de Planilhas de Treinamento para PDF
===========================================================

Exporta planos de treinamento em formato PDF profissional com:
- Dados do treinador físico (Nome, CPF, CREF)
- Dados do atleta
- Plano de treinamento detalhado
- Zonas de treinamento
- Recomendações personalizadas
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, PageBreak, Image, KeepTogether
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
from typing import List, Dict
import os
from pathlib import Path

# Importar classes do training_planner
from training_planner import Athlete, TrainingZones, TrainingPlanGenerator, PeriodizationPlanner


class PDFExporter:
    """Exporta planilhas de treinamento para PDF com design profissional."""
    
    def __init__(self, athlete: Athlete, training_plan: List[Dict], is_full_plan: bool = False, output_dir: str = None):
        """
        Inicializa o exportador de PDF.
        
        Args:
            athlete: Objeto Athlete com dados completos
            training_plan: Lista de dicionários com treinos
            is_full_plan: Se True, inclui periodização completa
            output_dir: Diretório de saída (opcional)
        """
        self.athlete = athlete
        self.training_plan = training_plan
        self.zones = TrainingZones(athlete.limiar_lactato, athlete.vo2_max)
        self.is_full_plan = is_full_plan
        self.output_dir = output_dir
        
        # Configurações de cores (identidade visual)
        self.colors = {
            'primary': colors.HexColor('#68b2c2'),      # Azul profissional
            'secondary': colors.HexColor('#f0f8fa'),    # Azul claro
            'accent': colors.HexColor('#4a90a4'),       # Azul escuro
            'text_dark': colors.HexColor('#2c3e50'),    # Cinza escuro
            'text_light': colors.HexColor('#7f8c8d'),   # Cinza médio
            'success': colors.HexColor('#27ae60'),      # Verde
            'warning': colors.HexColor('#f39c12'),      # Laranja
            'error': colors.HexColor('#e74c3c'),        # Vermelho
            'border': colors.HexColor('#dde4e6')        # Cinza claro
        }
        
        # Estilos de texto
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Cria estilos personalizados para o documento."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.colors['primary'],
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.colors['accent'],
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Seção
        self.styles.add(ParagraphStyle(
            name='CustomSection',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=self.colors['text_dark'],
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderPadding=5,
            backColor=self.colors['secondary']
        ))
        
        # Corpo
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.colors['text_dark'],
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Label
        self.styles.add(ParagraphStyle(
            name='CustomLabel',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=self.colors['text_light'],
            fontName='Helvetica-Bold'
        ))
        
        # Valor
        self.styles.add(ParagraphStyle(
            name='CustomValue',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.colors['text_dark'],
            fontName='Helvetica'
        ))
    
    def _create_header_footer(self, canvas_obj, doc):
        """Cria cabeçalho e rodapé em todas as páginas."""
        canvas_obj.saveState()
        
        # Rodapé
        footer_text = f"Plano de Treinamento - {self.athlete.nome} | Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(self.colors['text_light'])
        canvas_obj.drawString(30, 20, footer_text)
        
        # Número da página
        page_num = canvas_obj.getPageNumber()
        canvas_obj.drawRightString(A4[0] - 30, 20, f"Página {page_num}")
        
        canvas_obj.restoreState()
    
    def export_to_pdf(self, filename: str = None) -> str:
        """
        Exporta o plano de treinamento para PDF.
        
        Args:
            filename: Nome do arquivo (opcional, gera automaticamente se None)
        
        Returns:
            Caminho completo do arquivo gerado
        """
        # Gerar nome do arquivo se não fornecido
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"Plano_Treinamento_{self.athlete.nome.replace(' ', '_')}_{timestamp}.pdf"
        
        # Determinar diretório de saída
        if self.output_dir:
            filepath = Path(self.output_dir) / filename
        else:
            # Comportamento padrão: data/exports
            project_root = Path(__file__).parent
            export_dir = project_root / "data" / "exports"
            export_dir.mkdir(parents=True, exist_ok=True)
            filepath = export_dir / filename
        
        # Criar documento
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=50,
            bottomMargin=50
        )
        
        # Container para elementos do documento
        story = []
        
        # Adicionar conteúdo
        story.extend(self._create_title_page())
        story.append(PageBreak())
        story.extend(self._create_trainer_section())
        story.extend(self._create_athlete_section())
        story.append(Spacer(1, 20))
        
        if self.is_full_plan:
            story.extend(self._create_periodization_section())
            story.append(PageBreak())
        
        story.extend(self._create_training_plan_section())
        story.append(PageBreak())
        story.extend(self._create_zones_section())
        
        # Adicionar recomendações se houver
        recommendations = self._create_recommendations_section()
        if recommendations:
            story.append(PageBreak())
            story.extend(recommendations)
        
        # Construir PDF
        doc.build(story, onFirstPage=self._create_header_footer, onLaterPages=self._create_header_footer)
        
        return str(filepath)
    
    def _create_title_page(self) -> List:
        """Cria página de título."""
        elements = []
        
        # Espaço superior
        elements.append(Spacer(1, 80))
        
        # Ícone (emoji como texto)
        title_icon = Paragraph("🏃‍♂️", self.styles['CustomTitle'])
        elements.append(title_icon)
        elements.append(Spacer(1, 20))
        
        # Título
        title = Paragraph("PLANO DE TREINAMENTO", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 10))
        
        # Subtítulo com esporte
        subtitle = Paragraph(
            f"<b>{self.athlete.esporte.upper()}</b><br/>{self.athlete.distancia_prova}",
            self.styles['CustomSubtitle']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 40))
        
        # Linha decorativa
        elements.append(HRFlowable(
            width="50%",
            thickness=2,
            color=self.colors['primary'],
            spaceAfter=40,
            spaceBefore=0,
            hAlign='CENTER'
        ))
        
        # Nome do atleta
        athlete_name = Paragraph(
            f"<b>Atleta:</b> {self.athlete.nome}",
            self.styles['CustomSubtitle']
        )
        elements.append(athlete_name)
        elements.append(Spacer(1, 20))
        
        # Período do plano
        if self.is_full_plan:
            period_text = f"{self.athlete.semanas_ate_prova} semanas de preparação"
        else:
            period_text = "Plano semanal"
        
        period = Paragraph(period_text, self.styles['CustomBody'])
        elements.append(period)
        
        return elements
    
    def _create_trainer_section(self) -> List:
        """Cria seção com dados do treinador físico."""
        elements = []
        
        # Título da seção
        section_title = Paragraph(
            "👨‍⚕️ PROFISSIONAL RESPONSÁVEL",
            self.styles['CustomSection']
        )
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Dados do treinador em tabela
        trainer_data = [
            ['Nome Completo:', self.athlete.trainer.nome_completo],
            ['CPF:', self.athlete.trainer.formatar_cpf()],
            ['CREF:', self.athlete.trainer.formatar_cref()]
        ]
        
        trainer_table = Table(trainer_data, colWidths=[120, 350])
        trainer_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 11),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['text_light']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['text_dark']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, self.colors['border']),
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['secondary'])
        ]))
        
        elements.append(trainer_table)
        elements.append(Spacer(1, 25))
        
        return elements
    
    def _create_athlete_section(self) -> List:
        """Cria seção com dados do atleta."""
        elements = []
        
        # Título da seção
        section_title = Paragraph(
            "👤 DADOS DO ATLETA",
            self.styles['CustomSection']
        )
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Dados básicos
        basic_data = [
            ['Nome:', self.athlete.nome],
            ['Idade:', f"{self.athlete.idade} anos"],
            ['Gênero:', self.athlete.genero.capitalize()],
            ['Peso:', f"{self.athlete.peso} kg"],
            ['Altura:', f"{self.athlete.altura} cm"],
            ['IMC:', f"{self.athlete.imc:.1f}"]
        ]
        
        # Adicionar fase menstrual se aplicável
        if self.athlete.genero.lower() == 'feminino' and self.athlete.fase_menstrual:
            basic_data.append(['Fase do Ciclo:', self.athlete.fase_menstrual.capitalize()])
        
        basic_table = Table(basic_data, colWidths=[120, 150])
        basic_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['text_light']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['text_dark']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, self.colors['border'])
        ]))
        
        elements.append(basic_table)
        elements.append(Spacer(1, 15))
        
        # Dados de treinamento
        training_data = [
            ['Esporte:', self.athlete.esporte],
            ['Distância da Prova:', self.athlete.distancia_prova],
            ['Dias por Semana:', f"{self.athlete.dias_semana} dias"],
            ['Limiar de Lactato:', f"{self.athlete.limiar_lactato} bpm"],
            ['VO2 Max:', f"{self.athlete.vo2_max} ml/kg/min"]
        ]
        
        if self.is_full_plan:
            training_data.insert(2, ['Semanas até a Prova:', f"{self.athlete.semanas_ate_prova} semanas"])
        
        training_table = Table(training_data, colWidths=[120, 150])
        training_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 0), (1, -1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colors['text_light']),
            ('TEXTCOLOR', (1, 0), (1, -1), self.colors['text_dark']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, self.colors['border'])
        ]))
        
        elements.append(training_table)
        
        return elements
    
    def _create_periodization_section(self) -> List:
        """Cria seção de periodização (apenas para planos completos)."""
        elements = []
        
        if not self.is_full_plan:
            return elements
        
        # Título
        section_title = Paragraph(
            "📊 PERIODIZAÇÃO DO TREINAMENTO",
            self.styles['CustomSection']
        )
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Calcular periodização
        periodization = PeriodizationPlanner(self.athlete.semanas_ate_prova, self.athlete.esporte)
        distribuicao = periodization.calcular_distribuicao_fases()
        
        # Cabeçalho da tabela
        table_data = [['Fase', 'Semanas', 'Foco', 'Volume', 'Descrição']]
        
        # Adicionar fases
        for bloco in distribuicao:
            fase_config = periodization.fase_config[bloco['fase']]
            semanas_range = f"{bloco['semana_inicio']}-{bloco['semana_fim']}"
            num_semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
            
            table_data.append([
                fase_config['nome'],
                f"{semanas_range}\n({num_semanas} sem.)",
                fase_config['intensidade'].replace('_', ' ').title(),
                f"{int(fase_config['volume'] * 100)}%",
                fase_config['descricao']
            ])
        
        # Criar tabela
        period_table = Table(table_data, colWidths=[80, 70, 80, 50, 250])
        period_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Dados
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 1), (3, -1), 'CENTER'),
            ('ALIGN', (4, 1), (4, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['secondary']])
        ]))
        
        elements.append(period_table)
        
        return elements
    
    def _create_training_plan_section(self) -> List:
        """Cria seção do plano de treinamento."""
        elements = []
        
        # Título
        title_text = "📅 PLANO COMPLETO DE TREINAMENTO" if self.is_full_plan else "📅 PLANO SEMANAL DE TREINAMENTO"
        section_title = Paragraph(title_text, self.styles['CustomSection'])
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Agrupar treinos por semana (se plano completo)
        if self.is_full_plan and 'semana' in self.training_plan[0]:
            # Agrupar por semana
            semanas_dict = {}
            for treino in self.training_plan:
                semana = treino.get('semana', 1)
                if semana not in semanas_dict:
                    semanas_dict[semana] = []
                semanas_dict[semana].append(treino)
            
            # Criar tabela para cada semana
            for semana in sorted(semanas_dict.keys()):
                treinos_semana = semanas_dict[semana]
                
                # Subtítulo da semana
                fase = treinos_semana[0].get('fase', 'Base')
                tipo_semana = treinos_semana[0].get('tipo_semana', 'Normal')
                
                week_title = Paragraph(
                    f"<b>Semana {semana}</b> - {fase} ({tipo_semana})",
                    self.styles['CustomSubtitle']
                )
                elements.append(week_title)
                elements.append(Spacer(1, 10))
                
                # Tabela de treinos
                elements.append(self._create_training_table(treinos_semana))
                elements.append(Spacer(1, 20))
        else:
            # Plano de uma semana
            elements.append(self._create_training_table(self.training_plan))
        
        return elements
    
    def _create_training_table(self, treinos: List[Dict]) -> Table:
        """Cria tabela de treinos."""
        # Cabeçalho
        table_data = [['Dia', 'Modalidade', 'Duração', 'Tipo', 'Zona', 'FC', 'Descrição']]
        
        # Adicionar treinos
        for treino in treinos:
            dia_semana = treino.get('dia', 'N/A')
            modalidade = treino.get('modalidade', 'N/A')
            duracao = treino.get('duracao', 'N/A')
            tipo = treino.get('tipo', 'N/A')
            zona = treino.get('zona', 'N/A')
            intensidade = self.zones.get_intensity_value(zona) if zona != 'N/A' else 'N/A'
            descricao = treino.get('descricao', 'N/A')
            
            table_data.append([
                dia_semana,
                modalidade,
                duracao,
                tipo,
                zona,
                intensidade,
                descricao
            ])
        
        # Criar tabela com larguras ajustadas
        training_table = Table(table_data, colWidths=[60, 70, 50, 70, 60, 60, 160])
        training_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['accent']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Dados
            ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
            ('ALIGN', (0, 1), (5, -1), 'CENTER'),
            ('ALIGN', (6, 1), (6, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['secondary']])
        ]))
        
        return training_table
    
    def _create_zones_section(self) -> List:
        """Cria seção de zonas de treinamento."""
        elements = []
        
        # Título
        section_title = Paragraph(
            "💓 ZONAS DE TREINAMENTO",
            self.styles['CustomSection']
        )
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Descrição
        description = Paragraph(
            "As zonas de treinamento são baseadas na frequência cardíaca e determinam a intensidade de cada treino:",
            self.styles['CustomBody']
        )
        elements.append(description)
        elements.append(Spacer(1, 15))
        
        # Tabela de zonas
        table_data = [['Zona', 'Descrição', 'Intensidade (FC)']]
        
        for zona_nome, zona_data in self.zones.get_zones().items():
            table_data.append([
                zona_nome,
                zona_data['desc'],
                self.zones.get_intensity_value(zona_nome)
            ])
        
        zones_table = Table(table_data, colWidths=[100, 300, 130])
        zones_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            
            # Dados
            ('FONT', (0, 1), (0, -1), 'Helvetica-Bold', 9),
            ('FONT', (1, 1), (-1, -1), 'Helvetica', 9),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['border']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['secondary']])
        ]))
        
        elements.append(zones_table)
        
        return elements
    
    def _create_recommendations_section(self) -> List:
        """Cria seção de recomendações de saúde."""
        elements = []
        
        # Gerar recomendações
        generator = TrainingPlanGenerator(self.athlete)
        recomendacoes = generator.health_analysis.get('recomendacoes', [])
        
        # Adicionar recomendações de ciclo menstrual se aplicável
        if generator.menstrual_analysis and generator.menstrual_analysis.get('recomendacoes'):
            recomendacoes.extend(['', ''])
            recomendacoes.extend(generator.menstrual_analysis['recomendacoes'])
        
        if not recomendacoes:
            return elements
        
        # Título
        section_title = Paragraph(
            "⚕️ RECOMENDAÇÕES DE SAÚDE",
            self.styles['CustomSection']
        )
        elements.append(section_title)
        elements.append(Spacer(1, 15))
        
        # Adicionar cada recomendação
        for rec in recomendacoes:
            if rec.strip():  # Pular linhas vazias
                bullet = Paragraph(f"• {rec}", self.styles['CustomBody'])
                elements.append(bullet)
                elements.append(Spacer(1, 5))
        
        return elements


# Função de conveniência para exportação rápida
def export_training_plan_to_pdf(athlete: Athlete, training_plan: List[Dict], 
                                is_full_plan: bool = False, filename: str = None) -> str:
    """
    Função de conveniência para exportar plano de treinamento para PDF.
    
    Args:
        athlete: Objeto Athlete com dados completos
        training_plan: Lista de dicionários com treinos
        is_full_plan: Se True, inclui periodização completa
        filename: Nome do arquivo (opcional)
    
    Returns:
        Caminho completo do arquivo gerado
    """
    exporter = PDFExporter(athlete, training_plan, is_full_plan)
    return exporter.export_to_pdf(filename)
