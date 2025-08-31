import re
import numpy as np
from typing import Tuple, Dict, Any
from transformers import pipeline

class EmailProcessor:
    def __init__(self):
        self.classifier = None
        
        # Initialize the classifier
        self._initialize_classifier()
    
    def _initialize_classifier(self):
        """Initialize the Hugging Face classifier for email classification"""
        try:
            # Use a multilingual model for Portuguese and English
            model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
            self.classifier = pipeline(
                "sentiment-analysis",
                model=model_name,
                tokenizer=model_name
            )
            print("✅ Modelo Hugging Face carregado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo Hugging Face: {e}")
            print("⚠️  Sistema funcionará com classificação básica")
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess the email text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def classify_email(self, subject: str, content: str) -> Tuple[str, float]:
        """Classify email as productive or unproductive"""
        # Combine subject and content
        full_text = f"{subject} {content}"
        processed_text = self.preprocess_text(full_text)
        
        if not processed_text:
            return "improdutivo", 0.5
        
        try:
            if self.classifier:
                # Use Hugging Face classifier
                result = self.classifier(processed_text[:512])[0]  # Limit to 512 tokens
                
                # Map sentiment to productivity
                if result['label'] in ['1 star', '2 stars']:
                    category = 'improdutivo'
                    confidence = 1.0 - result['score']
                else:
                    category = 'produtivo'
                    confidence = result['score']
                
                return category, confidence
            
        except Exception as e:
            print(f"Erro na classificação: {e}")
        
        # Fallback classification based on keywords
        return self._keyword_based_classification(processed_text)
    
    def _keyword_based_classification(self, text: str) -> Tuple[str, float]:
        """Fallback classification using keyword analysis"""
        productive_keywords = [
            'reunião', 'meeting', 'projeto', 'project', 'cliente', 'client',
            'trabalho', 'work', 'relatório', 'report', 'deadline', 'entrega',
            'solicitação', 'request', 'contrato', 'contract', 'avaliação',
            'performance', 'sprint', 'agenda', 'urgente', 'importante'
        ]
        
        unproductive_keywords = [
            'corrente', 'chain', 'reencaminhar', 'forward', 'spam', 'promoção',
            'desconto', 'discount', 'piada', 'joke', 'fofoca', 'gossip',
            'marketing', 'newsletter', 'propaganda', 'advertisement'
        ]
        
        productive_count = sum(1 for word in productive_keywords if word in text)
        unproductive_count = sum(1 for word in unproductive_keywords if word in text)
        
        if productive_count > unproductive_count:
            confidence = min(0.8, 0.5 + (productive_count * 0.1))
            return 'produtivo', confidence
        elif unproductive_count > productive_count:
            confidence = min(0.8, 0.5 + (unproductive_count * 0.1))
            return 'improdutivo', confidence
        else:
            return 'improdutivo', 0.5
    
    def generate_response(self, category: str, subject: str, content: str) -> str:
        """Generate automatic response based on email category"""
        if category == 'produtivo':
            return self._generate_productive_response(subject, content)
        else:
            return self._generate_unproductive_response(subject, content)
    
    def _generate_productive_response(self, subject: str, content: str) -> str:
        """Generate response for productive emails"""
        responses = [
            "Obrigado pelo email. Vou analisar e retornar em breve.",
            "Recebi sua mensagem. Estou trabalhando nisso e te mantenho informado.",
            "Perfeito! Vou dar a atenção necessária a este assunto.",
            "Excelente iniciativa. Vamos agendar uma reunião para discutir os detalhes.",
            "Muito bem! Estou processando as informações e retorno em seguida."
        ]
        
        # Simple keyword-based response selection
        if any(word in content.lower() for word in ['reunião', 'meeting', 'agenda']):
            return "Vou verificar minha agenda e confirmar a disponibilidade para a reunião."
        elif any(word in content.lower() for word in ['projeto', 'project', 'trabalho']):
            return "Perfeito! Vou revisar o projeto e te envio um status atualizado."
        elif any(word in content.lower() for word in ['cliente', 'client', 'atendimento']):
            return "Entendido! Vou priorizar este atendimento ao cliente."
        else:
            return np.random.choice(responses)
    
    def _generate_unproductive_response(self, subject: str, content: str) -> str:
        """Generate response for unproductive emails"""
        responses = [
            "Obrigado, mas não posso participar de correntes de email.",
            "Agradeço o envio, mas não estou interessado neste tipo de conteúdo.",
            "Vou remover meu email desta lista de distribuição.",
            "Por favor, não me inclua em futuras correntes de email.",
            "Obrigado, mas não posso ajudar com este tipo de solicitação."
        ]
        
        if any(word in content.lower() for word in ['spam', 'promoção', 'desconto']):
            return "Não estou interessado em promoções. Por favor, remova meu email da lista."
        elif any(word in content.lower() for word in ['corrente', 'reencaminhar', 'forward']):
            return "Não participo de correntes de email. Por favor, não me inclua em futuras mensagens."
        else:
            return np.random.choice(responses)
    
    def process_email(self, subject: str, content: str, sender: str) -> Dict[str, Any]:
        """Process email and return classification results"""
        # Classify email
        category, confidence = self.classify_email(subject, content)
        
        # Generate response
        suggested_response = self.generate_response(category, subject, content)
        
        return {
            'category': category,
            'confidence_score': confidence,
            'suggested_response': suggested_response,
            'is_productive': category == 'produtivo'
        }
