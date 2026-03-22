"""
Teste Rápido de Exportação - Validar Caminhos Atualizados
==========================================================

Testa se os caminhos de exportação foram atualizados corretamente.
"""

from pathlib import Path
import sys

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from training_planner import Athlete, TrainingPlanGenerator, ExcelExporter


def testar_caminhos():
    """Testa os caminhos de exportação."""
    
    print("\n" + "="*80)
    print(" TESTE DE CAMINHOS - EXPORTAÇÃO DE PLANILHAS")
    print("="*80 + "\n")
    
    # Verificar diretório de exportação
    export_dir = Path(__file__).parent.parent / 'data' / 'exports'
    print(f"📁 Diretório de exportação configurado:")
    print(f"   {export_dir}")
    print(f"\n📍 Caminho absoluto:")
    print(f"   {export_dir.absolute()}\n")
    
    # Verificar se o diretório existe ou pode ser criado
    try:
        export_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Diretório criado/verificado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}\n")
        return False
    
    # Criar atleta de teste
    print("🏃 Criando atleta de teste...\n")
    
    atleta_teste = Athlete(
        nome="Teste Sistema",
        idade=30,
        peso=70.0,
        altura=175,
        genero="Masculino",
        esporte="Corrida",
        distancia_prova="10km",
        limiar_lactato=170,
        vo2_max=55.0,
        dias_semana=4,
        semanas_ate_prova=4
    )
    
    # Gerar plano
    print("📋 Gerando plano de treinamento...\n")
    
    gerador = TrainingPlanGenerator(atleta_teste)
    plano_semanal = gerador.get_weekly_training(numero_semana=1)
    
    # Testar exportação
    print("💾 Testando exportação...\n")
    
    try:
        exporter = ExcelExporter(atleta_teste, plano_semanal, is_full_plan=False)
        filename = "TESTE_VALIDACAO_CAMINHOS.xlsx"
        filepath = exporter.export_to_excel(filename)
        
        print(f"✅ Exportação bem-sucedida!")
        print(f"\n📄 Arquivo criado:")
        print(f"   {filepath}")
        
        # Verificar se o arquivo existe
        if Path(filepath).exists():
            tamanho = Path(filepath).stat().st_size
            print(f"\n📊 Tamanho do arquivo: {tamanho:,} bytes")
            print(f"✅ Arquivo existe e foi criado corretamente!")
        else:
            print(f"\n❌ ERRO: Arquivo não foi encontrado no caminho esperado!")
            return False
        
        print("\n" + "="*80)
        print(" ✅ TESTE DE CAMINHOS CONCLUÍDO COM SUCESSO!")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO durante exportação: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_caminhos()
    sys.exit(0 if sucesso else 1)
