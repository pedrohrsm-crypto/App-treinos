"""
Exemplo de uso do Sistema de Periodização Completa
Demonstra o planejamento de 40 semanas para uma maratona
"""

from training_planner import Athlete, TrainingPlanGenerator, ExcelExporter


def exemplo_maratona_40_semanas():
    """Exemplo: Corredor preparando para maratona em 40 semanas"""
    print("=" * 80)
    print("EXEMPLO: PREPARAÇÃO PARA MARATONA - 40 SEMANAS")
    print("=" * 80)
    
    atleta = Athlete(
        nome="Carlos Alberto",
        idade=35,
        peso=75.0,
        altura=178.0,
        esporte="Corrida",
        dias_semana=5,
        distancia_prova="Maratona",
        limiar_lactato=168.0,
        vo2_max=52.0,
        genero="Masculino",
        semanas_ate_prova=40
    )
    
    print(f"\n📊 Atleta: {atleta.nome}")
    print(f"   Objetivo: {atleta.distancia_prova}")
    print(f"   Prazo: {atleta.semanas_ate_prova} semanas")
    print(f"   IMC: {atleta.imc}\n")
    
    # Gerar plano completo
    generator = TrainingPlanGenerator(atleta)
    
    # Mostrar periodização
    print("=" * 80)
    print("PERIODIZAÇÃO COMPLETA:")
    print("=" * 80)
    
    distribuicao = generator.periodization.calcular_distribuicao_fases()
    
    for bloco in distribuicao:
        fase_config = generator.periodization.fase_config[bloco['fase']]
        semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
        
        print(f"\n🏃 {fase_config['nome'].upper()}")
        print(f"   Semanas: {bloco['semana_inicio']} a {bloco['semana_fim']} ({semanas} semanas)")
        print(f"   Descrição: {fase_config['descricao']}")
        print(f"   Intensidade: {fase_config['intensidade'].replace('_', ' ').title()}")
        print(f"   Volume base: {int(fase_config['volume'] * 100)}%")
        print(f"   Zonas principais: {', '.join(fase_config['zonas_principais'])}")
    
    print("\n" + "=" * 80)
    
    # Mostrar exemplos de semanas específicas
    semanas_exemplo = [1, 8, 16, 24, 32, 39, 40]
    
    print("\n📅 EXEMPLOS DE SEMANAS ESPECÍFICAS:")
    print("=" * 80)
    
    for num_semana in semanas_exemplo:
        info = generator.periodization.get_info_semana(num_semana)
        print(f"\nSemana {num_semana}:")
        print(f"  Fase: {info['nome_fase']}")
        print(f"  Tipo: {info['tipo_semana']}")
        print(f"  Volume: {int(info['volume_multiplicador'] * 100)}%")
        
        if num_semana == 40:
            print(f"  🏁 SEMANA DA PROVA!")
    
    print("\n" + "=" * 80)
    
    # Mostrar detalhes da semana 1 e semana 40
    print("\n🔍 DETALHAMENTO - SEMANA 1 (Base Aeróbica):")
    print("-" * 80)
    treinos_s1 = generator.get_weekly_training(1)
    for treino in treinos_s1:
        print(f"  {treino['dia']:10} | {treino['tipo']:20} | {treino['duracao']:8} | {treino['zona']}")
    
    print("\n🔍 DETALHAMENTO - SEMANA 40 (Polimento - Dia da Prova):")
    print("-" * 80)
    treinos_s40 = generator.get_weekly_training(40)
    for treino in treinos_s40:
        print(f"  {treino['dia']:10} | {treino['tipo']:20} | {treino['duracao']:8} | {treino['zona']}")
    
    print("\n" + "=" * 80)
    
    # Exportar plano completo
    print("\n⏳ Gerando planilha Excel com plano completo de 40 semanas...")
    plano_completo = generator.get_full_training_plan()
    
    print(f"   Total de treinos gerados: {len(plano_completo)}")
    
    exporter = ExcelExporter(atleta, plano_completo, is_full_plan=True)
    filename = exporter.export_to_excel("Maratona_40_Semanas_Completo.xlsx")
    
    print(f"\n✅ Planilha exportada: {filename}")
    print(f"   Abas incluídas:")
    print(f"      • Informações do Atleta")
    print(f"      • Periodização (5 fases)")
    print(f"      • Plano Completo (todos os {len(plano_completo)} treinos)")
    print(f"      • Zonas de Treinamento")
    
    print("\n" + "=" * 80)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 80)


def exemplo_10k_curto():
    """Exemplo: Corredor preparando para 10K em 8 semanas"""
    print("\n\n" + "=" * 80)
    print("EXEMPLO: PREPARAÇÃO PARA 10K - 8 SEMANAS")
    print("=" * 80)
    
    atleta = Athlete(
        nome="Maria Silva",
        idade=28,
        peso=58.0,
        altura=165.0,
        esporte="Corrida",
        dias_semana=4,
        distancia_prova="10K",
        limiar_lactato=175.0,
        vo2_max=48.0,
        genero="Feminino",
        semanas_ate_prova=8
    )
    
    print(f"\n📊 Atleta: {atleta.nome}")
    print(f"   Objetivo: {atleta.distancia_prova}")
    print(f"   Prazo: {atleta.semanas_ate_prova} semanas\n")
    
    generator = TrainingPlanGenerator(atleta)
    
    print("PERIODIZAÇÃO:")
    print("-" * 80)
    distribuicao = generator.periodization.calcular_distribuicao_fases()
    
    for bloco in distribuicao:
        fase_config = generator.periodization.fase_config[bloco['fase']]
        semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
        print(f"  Semanas {bloco['semana_inicio']}-{bloco['semana_fim']} ({semanas}): {fase_config['nome']}")
    
    print("\n" + "-" * 80)
    
    # Exportar
    plano_completo = generator.get_full_training_plan()
    exporter = ExcelExporter(atleta, plano_completo, is_full_plan=True)
    filename = exporter.export_to_excel("10K_8_Semanas_Completo.xlsx")
    
    print(f"\n✅ Planilha exportada: {filename}")
    print(f"   Total de treinos: {len(plano_completo)}")


def exemplo_ironman_20_semanas():
    """Exemplo: Triatleta preparando para Ironman em 20 semanas"""
    print("\n\n" + "=" * 80)
    print("EXEMPLO: PREPARAÇÃO PARA IRONMAN - 20 SEMANAS")
    print("=" * 80)
    
    atleta = Athlete(
        nome="João Santos",
        idade=32,
        peso=72.0,
        altura=180.0,
        esporte="Triathlon",
        dias_semana=6,
        distancia_prova="Ironman",
        limiar_lactato=165.0,
        vo2_max=55.0,
        genero="Masculino",
        semanas_ate_prova=20
    )
    
    print(f"\n📊 Atleta: {atleta.nome}")
    print(f"   Objetivo: {atleta.distancia_prova}")
    print(f"   Prazo: {atleta.semanas_ate_prova} semanas\n")
    
    generator = TrainingPlanGenerator(atleta)
    
    print("PERIODIZAÇÃO:")
    print("-" * 80)
    distribuicao = generator.periodization.calcular_distribuicao_fases()
    
    for bloco in distribuicao:
        fase_config = generator.periodization.fase_config[bloco['fase']]
        semanas = bloco['semana_fim'] - bloco['semana_inicio'] + 1
        print(f"  Semanas {bloco['semana_inicio']}-{bloco['semana_fim']} ({semanas}): {fase_config['nome']}")
    
    # Mostrar semana 10 (Fase de Velocidade)
    print("\n🔍 EXEMPLO - SEMANA 10:")
    print("-" * 80)
    treinos_s10 = generator.get_weekly_training(10)
    for treino in treinos_s10:
        print(f"  {treino['dia']:10} | {treino['modalidade']:10} | {treino['tipo']:15} | {treino['duracao']}")
    
    print("\n" + "-" * 80)
    
    # Exportar
    plano_completo = generator.get_full_training_plan()
    exporter = ExcelExporter(atleta, plano_completo, is_full_plan=True)
    filename = exporter.export_to_excel("Ironman_20_Semanas_Completo.xlsx")
    
    print(f"\n✅ Planilha exportada: {filename}")
    print(f"   Total de treinos: {len(plano_completo)}")


if __name__ == "__main__":
    print("\n🏃 EXEMPLOS DE PERIODIZAÇÃO COMPLETA\n")
    
    print("Escolha um exemplo:")
    print("1 - Maratona (40 semanas) - Exemplo completo detalhado")
    print("2 - 10K (8 semanas) - Plano curto")
    print("3 - Ironman (20 semanas) - Triathlon longo")
    print("4 - Executar todos os exemplos")
    
    escolha = input("\nOpção (1-4): ").strip()
    
    print()
    
    if escolha == "1":
        exemplo_maratona_40_semanas()
    elif escolha == "2":
        exemplo_10k_curto()
    elif escolha == "3":
        exemplo_ironman_20_semanas()
    elif escolha == "4":
        exemplo_maratona_40_semanas()
        exemplo_10k_curto()
        exemplo_ironman_20_semanas()
    else:
        print("Opção inválida!")
    
    print("\n" + "=" * 80)
    print("✅ Exemplos concluídos! Verifique os arquivos .xlsx gerados.")
    print("=" * 80)
