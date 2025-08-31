#!/usr/bin/env python3
"""
Script de teste para o sistema de classificação de emails
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_django.settings')
django.setup()

from hello.nlp_processor import EmailProcessor

def test_email_classification():
    """Testa a classificação de diferentes tipos de emails"""
    
    print("🧠 Testando Sistema de Classificação de Emails")
    print("=" * 50)
    
    # Inicializar o processador
    processor = EmailProcessor()
    
    # Emails de teste
    test_emails = [
        {
            "sender": "gerente@empresa.com",
            "subject": "Reunião de Projeto - Sistema de Vendas",
            "content": "Olá! Precisamos agendar uma reunião para discutir o desenvolvimento do novo sistema de vendas. O projeto está atrasado e precisamos definir as prioridades para a próxima sprint. Podemos marcar para amanhã às 14h?",
            "expected": "produtivo"
        },
        {
            "sender": "cliente@cliente.com",
            "subject": "Solicitação de Alterações - Contrato",
            "content": "Bom dia! Gostaria de solicitar algumas alterações no contrato que assinamos. Preciso adicionar cláusulas de confidencialidade e ajustar os prazos de entrega. Quando podemos conversar sobre isso?",
            "expected": "produtivo"
        },
        {
            "sender": "amigo@email.com",
            "subject": "Corrente de Email - Boa Sorte",
            "content": "Olha só! Esta corrente de email já passou por 50 pessoas e trouxe sorte para todas elas! Se você não reencaminhar para 10 amigos em 24 horas, algo ruim vai acontecer. Reencaminhe agora e tenha um dia abençoado!",
            "expected": "improdutivo"
        },
        {
            "sender": "spam@promocao.com",
            "subject": "Promoção Imperdível - 90% de Desconto",
            "content": "ATENÇÃO! Promoção por tempo limitado! Produtos com até 90% de desconto! Não perca esta oportunidade única! Clique aqui agora para aproveitar!",
            "expected": "improdutivo"
        },
        {
            "sender": "rh@empresa.com",
            "subject": "Avaliação de Performance - 2024",
            "content": "Prezado colaborador, sua avaliação de performance anual está agendada para a próxima semana. Por favor, prepare um relatório das suas principais conquistas e objetivos para o próximo ano.",
            "expected": "produtivo"
        }
    ]
    
    results = []
    
    for i, email in enumerate(test_emails, 1):
        print(f"\n📧 Teste {i}: {email['subject']}")
        print(f"   Remetente: {email['sender']}")
        print(f"   Esperado: {email['expected']}")
        
        try:
            # Processar email
            result = processor.process_email(
                email['subject'],
                email['content'],
                email['sender']
            )
            
            # Verificar resultado
            predicted = result['category']
            confidence = result['confidence_score']
            response = result['suggested_response']
            
            print(f"   Resultado: {predicted}")
            print(f"   Confiança: {confidence:.1%}")
            print(f"   Resposta: {response[:100]}...")
            
            # Verificar se a classificação está correta
            is_correct = predicted == email['expected']
            status = "✅ CORRETO" if is_correct else "❌ INCORRETO"
            print(f"   Status: {status}")
            
            results.append({
                'test': i,
                'expected': email['expected'],
                'predicted': predicted,
                'confidence': confidence,
                'correct': is_correct
            })
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            results.append({
                'test': i,
                'expected': email['expected'],
                'predicted': 'ERRO',
                'confidence': 0,
                'correct': False
            })
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    total_tests = len(results)
    correct_predictions = sum(1 for r in results if r['correct'])
    accuracy = (correct_predictions / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Total de testes: {total_tests}")
    print(f"Previsões corretas: {correct_predictions}")
    print(f"Precisão: {accuracy:.1f}%")
    
    if accuracy >= 80:
        print("🎉 Excelente! Sistema funcionando muito bem!")
    elif accuracy >= 60:
        print("👍 Bom! Sistema funcionando bem!")
    else:
        print("⚠️  Sistema precisa de ajustes!")
    
    # Detalhes dos testes
    print("\n📋 DETALHES DOS TESTES:")
    for result in results:
        status = "✅" if result['correct'] else "❌"
        print(f"{status} Teste {result['test']}: Esperado {result['expected']}, Predito {result['predicted']}")

def test_nlp_features():
    """Testa as funcionalidades de NLP"""
    
    print("\n🔍 Testando Funcionalidades de NLP")
    print("=" * 40)
    
    processor = EmailProcessor()
    
    # Teste de pré-processamento
    test_text = "Olá! Precisamos agendar uma REUNIÃO para discutir o PROJETO. O sistema está FUNCIONANDO bem!"
    
    print(f"Texto original: {test_text}")
    processed = processor.preprocess_text(test_text)
    print(f"Texto processado: {processed}")
    
    # Teste de geração de respostas
    print("\n📝 Testando Geração de Respostas:")
    
    productive_response = processor.generate_response("produtivo", "Reunião", "Vamos agendar uma reunião")
    print(f"Resposta para email produtivo: {productive_response}")
    
    unproductive_response = processor.generate_response("improdutivo", "Spam", "Promoção imperdível")
    print(f"Resposta para email improdutivo: {unproductive_response}")

if __name__ == "__main__":
    print("🚀 Iniciando testes do sistema de emails...")
    
    try:
        test_email_classification()
        test_nlp_features()
        
        print("\n🎯 Testes concluídos com sucesso!")
        print("\nPara usar o sistema web:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://localhost:8000/email/")
        print("3. Teste com diferentes tipos de emails!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        print("Verifique se o Django está configurado corretamente.")
        sys.exit(1)
