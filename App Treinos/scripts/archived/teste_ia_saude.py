"""
Teste do Sistema de IA para Adequações de Saúde
Demonstra as capacidades de análise e ajuste automático
"""

from training_planner import HealthIssue, HealthAdvisor, Athlete, TrainingPlanGenerator


def testar_analise_ia():
    """Testa a análise de IA para diferentes problemas de saúde"""
    
    advisor = HealthAdvisor()
    
    print("=" * 80)
    print("TESTE DO SISTEMA DE IA - HEALTH ADVISOR")
    print("=" * 80)
    
    # Teste 1: Problema no joelho
    print("\n1️⃣ ANÁLISE: Lesão no Joelho")
    print("-" * 80)
    problema_joelho = HealthIssue(
        tipo='ortopédico',
        descricao='Condromalácia patelar',
        membro_afetado='joelho_direito',
        gravidade='moderado'
    )
    
    analise = advisor.analyze_health_issues([problema_joelho], 'Corrida')
    print("\n🤖 RECOMENDAÇÕES DA IA:")
    for rec in analise['recomendacoes']:
        print(rec)
    
    # Teste 2: Problema no ombro
    print("\n\n2️⃣ ANÁLISE: Lesão no Ombro")
    print("-" * 80)
    problema_ombro = HealthIssue(
        tipo='ortopédico',
        descricao='Tendinite no manguito rotador',
        membro_afetado='ombro_esquerdo',
        gravidade='leve'
    )
    
    analise = advisor.analyze_health_issues([problema_ombro], 'Natação')
    print("\n🤖 RECOMENDAÇÕES DA IA:")
    for rec in analise['recomendacoes']:
        print(rec)
    
    # Teste 3: Diabetes
    print("\n\n3️⃣ ANÁLISE: Diabetes")
    print("-" * 80)
    problema_diabetes = HealthIssue(
        tipo='diabetes',
        descricao='Diabetes tipo 1',
        gravidade='moderado'
    )
    
    analise = advisor.analyze_health_issues([problema_diabetes], 'Triathlon')
    print("\n🤖 RECOMENDAÇÕES DA IA:")
    for rec in analise['recomendacoes']:
        print(rec)
    
    # Teste 4: Múltiplos problemas
    print("\n\n4️⃣ ANÁLISE: Múltiplas Condições")
    print("-" * 80)
    problema_lombar = HealthIssue(
        tipo='ortopédico',
        descricao='Hérnia de disco',
        membro_afetado='lombar',
        gravidade='grave'
    )
    
    analise = advisor.analyze_health_issues(
        [problema_joelho, problema_lombar], 
        'Ciclismo'
    )
    print("\n🤖 RECOMENDAÇÕES DA IA (Múltiplas Condições):")
    for rec in analise['recomendacoes']:
        print(rec)


def testar_ajuste_treinos():
    """Testa o ajuste automático de treinos"""
    
    print("\n\n" + "=" * 80)
    print("TESTE DE AJUSTE AUTOMÁTICO DE TREINOS")
    print("=" * 80)
    
    # Criar atleta com lesão no joelho
    problema = HealthIssue(
        tipo='ortopédico',
        descricao='Condromalácia patelar',
        membro_afetado='joelho_direito',
        gravidade='moderado'
    )
    
    atleta = Athlete(
        nome="Teste Silva",
        idade=30,
        peso=70.0,
        altura=175.0,
        esporte="Corrida",
        dias_semana=4,
        distancia_prova="Meia Maratona",
        limiar_lactato=165.0,
        vo2_max=50.0,
        genero="Masculino",
        problemas_saude=[problema]
    )
    
    # Gerar treinos
    generator = TrainingPlanGenerator(atleta)
    treinos = generator.get_weekly_training()
    
    print(f"\n📊 Atleta: {atleta.nome}")
    print(f"   IMC: {atleta.imc} | Problema: {problema.descricao}")
    print(f"\n📋 Treinos Ajustados:")
    print("-" * 80)
    
    for i, treino in enumerate(treinos, 1):
        print(f"\n{i}. {treino['dia']} - {treino['modalidade']}")
        print(f"   Tipo: {treino['tipo']} | Duração: {treino['duracao']}")
        print(f"   Zona: {treino['zona']}")
        
        if '⚕️' in treino['descricao']:
            print(f"   ⚠️ TREINO AJUSTADO POR IA")
            print(f"   📝 {treino['descricao']}")
        else:
            print(f"   📝 {treino['descricao'][:70]}...")


def testar_comparacao():
    """Compara treinos com e sem restrições"""
    
    print("\n\n" + "=" * 80)
    print("COMPARAÇÃO: COM vs SEM RESTRIÇÕES DE SAÚDE")
    print("=" * 80)
    
    # Atleta SEM restrições
    atleta_saudavel = Athlete(
        nome="Atleta Saudável",
        idade=30,
        peso=70.0,
        altura=175.0,
        esporte="Corrida",
        dias_semana=4,
        distancia_prova="10K",
        limiar_lactato=165.0,
        vo2_max=50.0,
        genero="Masculino",
        problemas_saude=[]
    )
    
    # Atleta COM lesão
    problema = HealthIssue(
        tipo='ortopédico',
        descricao='Tendinite patelar',
        membro_afetado='joelho_direito',
        gravidade='moderado'
    )
    
    atleta_lesionado = Athlete(
        nome="Atleta com Lesão",
        idade=30,
        peso=70.0,
        altura=175.0,
        esporte="Corrida",
        dias_semana=4,
        distancia_prova="10K",
        limiar_lactato=165.0,
        vo2_max=50.0,
        genero="Masculino",
        problemas_saude=[problema]
    )
    
    # Gerar treinos
    gen_saudavel = TrainingPlanGenerator(atleta_saudavel)
    gen_lesionado = TrainingPlanGenerator(atleta_lesionado)
    
    treinos_saudavel = gen_saudavel.get_weekly_training()
    treinos_lesionado = gen_lesionado.get_weekly_training()
    
    print("\n📊 COMPARAÇÃO DE VOLUME:")
    print("-" * 80)
    
    volume_saudavel = sum([int(t['duracao'].split()[0]) for t in treinos_saudavel])
    volume_lesionado = sum([int(t['duracao'].split()[0]) for t in treinos_lesionado])
    reducao = ((volume_saudavel - volume_lesionado) / volume_saudavel) * 100
    
    print(f"✅ Atleta Saudável: {volume_saudavel} minutos/semana")
    print(f"⚠️  Atleta Lesionado: {volume_lesionado} minutos/semana")
    print(f"📉 Redução aplicada: {reducao:.1f}%")
    
    print("\n📋 COMPARAÇÃO LADO A LADO:")
    print("-" * 80)
    
    for i in range(min(len(treinos_saudavel), len(treinos_lesionado))):
        t_sau = treinos_saudavel[i]
        t_les = treinos_lesionado[i]
        
        print(f"\n{t_sau['dia']}:")
        print(f"  Normal:  {t_sau['duracao']:>8} | {t_sau['tipo']}")
        print(f"  Ajustado: {t_les['duracao']:>8} | {t_les['tipo']}")
        if '⚕️' in t_les['descricao']:
            print(f"  ⚠️ Modificado por IA")


def testar_ciclo_menstrual():
    """Testa os ajustes para diferentes fases do ciclo menstrual"""
    
    print("\n\n" + "=" * 80)
    print("TESTE DE AJUSTES POR CICLO MENSTRUAL")
    print("=" * 80)
    
    fases = ['menstrual', 'folicular', 'ovulatoria', 'lutea']
    
    for fase in fases:
        print(f"\n{'='*80}")
        print(f"🌸 TESTANDO FASE: {fase.upper()}")
        print("="*80)
        
        atleta = Athlete(
            nome=f"Atleta - Fase {fase.capitalize()}",
            idade=28,
            peso=58.0,
            altura=165.0,
            esporte="Corrida",
            dias_semana=4,
            distancia_prova="10K",
            limiar_lactato=172.0,
            vo2_max=48.0,
            genero="Feminino",
            fase_menstrual=fase
        )
        
        generator = TrainingPlanGenerator(atleta)
        
        # Mostrar recomendações
        if generator.menstrual_analysis:
            print("\n🤖 RECOMENDAÇÕES DA IA:")
            for rec in generator.menstrual_analysis.get('recomendacoes', []):
                print(rec)
        
        # Mostrar um treino ajustado
        plano = generator.get_weekly_training()
        if plano:
            treino = plano[0]
            print(f"\n📋 Exemplo de treino ajustado:")
            print(f"   Dia: {treino['dia']}")
            print(f"   Tipo: {treino['tipo']}")
            print(f"   Duração: {treino['duracao']}")
            print(f"   Zona: {treino['zona']}")
            if '🌸' in treino['descricao']:
                print(f"   ⚠️ Ajustado para fase {fase}")


if __name__ == "__main__":
    print("\n🏃 SISTEMA DE TESTE - IA PARA ADEQUAÇÕES DE SAÚDE\n")
    
    # Executar todos os testes
    testar_analise_ia()
    testar_ajuste_treinos()
    testar_comparacao()
    testar_ciclo_menstrual()
    
    print("\n\n" + "=" * 80)
    print("✅ TESTES CONCLUÍDOS!")
    print("=" * 80)
    print("\nO sistema demonstrou:")
    print("  ✓ Análise inteligente de problemas de saúde")
    print("  ✓ Recomendações personalizadas por IA")
    print("  ✓ Ajuste automático de treinos")
    print("  ✓ Redução proporcional de volume")
    print("  ✓ Marcação visual de treinos modificados")
    print("  ✓ Adaptação para ciclo menstrual (4 fases)")
    print("\n" + "=" * 80)
