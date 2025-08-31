#!/usr/bin/env python3
"""
Script de demonstração da API do sistema de classificação de emails
"""

import requests
import json
import time

def test_api_endpoint():
    """Testa o endpoint da API"""
    
    print("🌐 Testando API do Sistema de Emails")
    print("=" * 50)
    
    # URL da API
    api_url = "http://localhost:8000/api/email/process/"
    
    # Emails de teste
    test_emails = [
        {
            "sender": "gerente@empresa.com",
            "subject": "Reunião de Projeto - Sistema de Vendas",
            "content": "Olá! Precisamos agendar uma reunião para discutir o desenvolvimento do novo sistema de vendas. O projeto está atrasado e precisamos definir as prioridades para a próxima sprint. Podemos marcar para amanhã às 14h?"
        },
        {
            "sender": "cliente@cliente.com",
            "subject": "Solicitação de Alterações - Contrato",
            "content": "Bom dia! Gostaria de solicitar algumas alterações no contrato que assinamos. Preciso adicionar cláusulas de confidencialidade e ajustar os prazos de entrega. Quando podemos conversar sobre isso?"
        },
        {
            "sender": "amigo@email.com",
            "subject": "Corrente de Email - Boa Sorte",
            "content": "Olha só! Esta corrente de email já passou por 50 pessoas e trouxe sorte para todas elas! Se você não reencaminhar para 10 amigos em 24 horas, algo ruim vai acontecer. Reencaminhe agora e tenha um dia abençoado!"
        },
        {
            "sender": "spam@promocao.com",
            "subject": "Promoção Imperdível - 90% de Desconto",
            "content": "ATENÇÃO! Promoção por tempo limitado! Produtos com até 90% de desconto! Não perca esta oportunidade única! Clique aqui agora para aproveitar!"
        }
    ]
    
    print("📧 Enviando emails para classificação via API...")
    print()
    
    for i, email in enumerate(test_emails, 1):
        print(f"📨 Teste {i}: {email['subject']}")
        print(f"   Remetente: {email['sender']}")
        
        try:
            # Enviar requisição POST
            response = requests.post(
                api_url,
                json=email,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Status: {response.status_code}")
                print(f"   🏷️  Categoria: {result['category']}")
                print(f"   📊 Confiança: {result['confidence_score']:.1%}")
                print(f"   💬 Resposta: {result['suggested_response'][:80]}...")
                print(f"   🆔 ID: {result['id']}")
                
            else:
                print(f"   ❌ Erro: {response.status_code}")
                print(f"   📝 Resposta: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Erro: Não foi possível conectar ao servidor")
            print("   💡 Certifique-se de que o Django está rodando: python manage.py runserver")
            break
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        print()
        time.sleep(1)  # Pausa entre requisições
    
    print("🎯 Teste da API concluído!")
    print("\nPara testar via interface web:")
    print("1. Acesse: http://localhost:8000/email/")
    print("2. Use os exemplos pré-carregados")
    print("3. Veja os resultados em tempo real!")

def test_web_interface():
    """Testa a interface web"""
    
    print("\n🌐 Testando Interface Web")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/email/")
        if response.status_code == 200:
            print("✅ Interface web acessível em: http://localhost:8000/email/")
        else:
            print(f"❌ Interface web retornou status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Servidor Django não está rodando")
        print("💡 Execute: python manage.py runserver")

if __name__ == "__main__":
    print("🚀 Iniciando demonstração da API...")
    
    # Aguardar um pouco para o servidor inicializar
    print("⏳ Aguardando servidor Django inicializar...")
    time.sleep(3)
    
    # Testar API
    test_api_endpoint()
    
    # Testar interface web
    test_web_interface()
    
    print("\n🎉 Demonstração concluída!")
    print("\n📚 Recursos disponíveis:")
    print("• API: POST /api/email/process/")
    print("• Interface: http://localhost:8000/email/")
    print("• Lista: http://localhost:8000/email/list/")
    print("• Estatísticas: http://localhost:8000/email/analytics/")
