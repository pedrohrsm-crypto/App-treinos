"""
Exemplo de uso do Sistema de Treinamento
Execute este arquivo para testar com dados pré-definidos
"""

from training_planner import Athlete, TrainingPlanGenerator, ExcelExporter, HealthIssue


def exemplo_triathlon():
    """Exemplo: Atleta de Triathlon"""
    print("=" * 70)
    print("EXEMPLO 1: TRIATLETA - MEIO IRONMAN")
    print("=" * 70)
    
    atleta = Athlete(
        nome="João Silva",
        idade=35,
        peso=75.0,
        altura=178.0,
        esporte="Triathlon",
        dias_semana=6,
        distancia_prova="Meio Ironman",
        limiar_lactato=168.0,
        vo2_max=52.0
    )
    
    generator = TrainingPlanGenerator(atleta)
    plano = generator.get_weekly_training()
    
    print(f"\nPlano gerado para {atleta.nome}")
    print(f"IMC: {atleta.imc} | Treinos na semana: {len(plano)}\n")
    
    for treino in plano:
        print(f"📅 {treino['dia']} - {treino['modalidade']} ({treino['duracao']})")
    
    # Exportar
    exporter = ExcelExporter(atleta, plano)
    filename = exporter.export_to_excel("Exemplo_Triathlon.xlsx")
    print(f"\n✅ Exportado: {filename}\n")


def exemplo_corrida():
    """Exemplo: Corredor de Maratona com problema no joelho"""
    print("=" * 70)
    print("EXEMPLO 2: CORREDOR - MARATONA (COM LESÃO NO JOELHO)")
    print("=" * 70)
    
    # Problema de saúde: lesão no joelho
    problema_joelho = HealthIssue(
        tipo='ortopédico',
        descricao='Condromalácia patelar',
        membro_afetado='joelho_direito',
        gravidade='moderado'
    )
    
    atleta = Athlete(
        nome="Maria Santos",
        idade=28,
        peso=58.0,
        altura=165.0,
        esporte="Corrida",
        dias_semana=5,
        distancia_prova="Maratona",
        limiar_lactato=172.0,
        vo2_max=48.0,
        problemas_saude=[problema_joelho]
    )
    
    generator = TrainingPlanGenerator(atleta)
    plano = generator.get_weekly_training()
    
    print(f"\nPlano gerado para {atleta.nome}")
    print(f"IMC: {atleta.imc} | Treinos na semana: {len(plano)}")
    print(f"⚠️ ATENÇÃO: Treinos ajustados por lesão no joelho\n")
    
    for treino in plano:
        print(f"📅 {treino['dia']} - {treino['tipo']} ({treino['duracao']})")
        if '⚕️' in treino['descricao']:
            print(f"   ⚠️ TREINO AJUSTADO")
    
    # Exportar
    exporter = ExcelExporter(atleta, plano)
    filename = exporter.export_to_excel("Exemplo_Corrida_Joelho.xlsx")
    print(f"\n✅ Exportado: {filename}\n")


def exemplo_natacao():
    """Exemplo: Nadador com problema no ombro"""
    print("=" * 70)
    print("EXEMPLO 3: NADADOR - 3000m (COM LESÃO NO OMBRO)")
    print("=" * 70)
    
    # Problema de saúde: lesão no ombro
    problema_ombro = HealthIssue(
        tipo='ortopédico',
        descricao='Tendinite no manguito rotador',
        membro_afetado='ombro_esquerdo',
        gravidade='leve'
    )
    
    atleta = Athlete(
        nome="Pedro Costa",
        idade=22,
        peso=72.0,
        altura=182.0,
        esporte="Natação",
        dias_semana=5,
        distancia_prova="3000m",
        limiar_lactato=165.0,
        vo2_max=55.0,
        problemas_saude=[problema_ombro]
    )
    
    generator = TrainingPlanGenerator(atleta)
    plano = generator.get_weekly_training()
    
    print(f"\nPlano gerado para {atleta.nome}")
    print(f"IMC: {atleta.imc} | Treinos na semana: {len(plano)}")
    print(f"⚠️ ATENÇÃO: Treinos ajustados por lesão no ombro\n")
    
    for treino in plano:
        print(f"📅 {treino['dia']} - {treino['tipo']} ({treino['duracao']})")
        if '⚕️' in treino['descricao']:
            print(f"   📝 {treino['descricao'][:80]}...")
    
    # Exportar
    exporter = ExcelExporter(atleta, plano)
    filename = exporter.export_to_excel("Exemplo_Natacao_Ombro.xlsx")
    print(f"\n✅ Exportado: {filename}\n")


def exemplo_ciclismo():
    """Exemplo: Ciclista com problema lombar"""
    print("=" * 70)
    print("EXEMPLO 4: CICLISTA - 160K (COM DOR LOMBAR)")
    print("=" * 70)
    
    # Problema de saúde: dor lombar
    problema_lombar = HealthIssue(
        tipo='ortopédico',
        descricao='Hérnia de disco L4-L5',
        membro_afetado='lombar',
        gravidade='moderado'
    )
    
    atleta = Athlete(
        nome="Carlos Oliveira",
        idade=40,
        peso=80.0,
        altura=175.0,
        esporte="Ciclismo",
        dias_semana=4,
        distancia_prova="160K",
        limiar_lactato=160.0,
        vo2_max=45.0,
        problemas_saude=[problema_lombar]
    )
    
    generator = TrainingPlanGenerator(atleta)
    plano = generator.get_weekly_training()
    
    print(f"\nPlano gerado para {atleta.nome}")
    print(f"IMC: {atleta.imc} | Treinos na semana: {len(plano)}")
    print(f"⚠️ ATENÇÃO: Treinos ajustados por problema lombar\n")
    
    for treino in plano:
        print(f"📅 {treino['dia']} - {treino['tipo']} ({treino['duracao']})")
    
    # Exportar
    exporter = ExcelExporter(atleta, plano)
    filename = exporter.export_to_excel("Exemplo_Ciclismo_Lombar.xlsx")
    print(f"\n✅ Exportado: {filename}\n")


def exemplo_diabetes():
    """Exemplo: Triatleta com diabetes"""
    print("=" * 70)
    print("EXEMPLO 5: TRIATLETA COM DIABETES TIPO 1")
    print("=" * 70)
    
    # Problema de saúde: diabetes
    problema_diabetes = HealthIssue(
        tipo='diabetes',
        descricao='Diabetes tipo 1',
        gravidade='moderado'
    )
    
    atleta = Athlete(
        nome="Ana Paula",
        idade=32,
        peso=62.0,
        altura=168.0,
        esporte="Triathlon",
        dias_semana=5,
        distancia_prova="Olímpico",
        limiar_lactato=170.0,
        vo2_max=50.0,
        problemas_saude=[problema_diabetes]
    )
    
    generator = TrainingPlanGenerator(atleta)
    plano = generator.get_weekly_training()
    
    print(f"\nPlano gerado para {atleta.nome}")
    print(f"IMC: {atleta.imc} | Treinos na semana: {len(plano)}\n")
    
    # Mostrar recomendações
    if generator.health_analysis['recomendacoes']:
        print("🤖 RECOMENDAÇÕES DE IA:")
        for rec in generator.health_analysis['recomendacoes']:
            print(rec)
        print()
    
    # Exportar
    exporter = ExcelExporter(atleta, plano)
    filename = exporter.export_to_excel("Exemplo_Triathlon_Diabetes.xlsx")
    print(f"\n✅ Exportado: {filename}\n")


if __name__ == "__main__":
    print("\n🏃 EXEMPLOS DE USO DO SISTEMA DE TREINAMENTO\n")
    
    print("Escolha um exemplo:")
    print("1 - Triathlon (Meio Ironman) - Sem restrições")
    print("2 - Corrida (Maratona) - Com lesão no joelho")
    print("3 - Natação (3000m) - Com lesão no ombro")
    print("4 - Ciclismo (160K) - Com problema lombar")
    print("5 - Triathlon (Olímpico) - Com diabetes")
    print("6 - Executar todos os exemplos")
    
    escolha = input("\nOpção (1-6): ").strip()
    
    print()
    
    if escolha == "1":
        exemplo_triathlon()
    elif escolha == "2":
        exemplo_corrida()
    elif escolha == "3":
        exemplo_natacao()
    elif escolha == "4":
        exemplo_ciclismo()
    elif escolha == "5":
        exemplo_diabetes()
    elif escolha == "6":
        exemplo_triathlon()
        exemplo_corrida()
        exemplo_natacao()
        exemplo_ciclismo()
        exemplo_diabetes()
    else:
        print("Opção inválida!")
    
    print("=" * 70)
    print("✅ Exemplos concluídos! Verifique os arquivos .xlsx gerados.")
    print("=" * 70)
