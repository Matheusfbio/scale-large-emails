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
                
                # Map sentiment to productivity - CORRIGIDO
                # Emails com sentimento negativo (1-2 estrelas) são produtivos (trabalho)
                # Emails com sentimento positivo (4-5 estrelas) são improdutivos (spam/correntes)
                if result['label'] in ['1 star', '2 stars']:
                    category = 'produtivo'
                    # Ajustar confiança baseada na força do sentimento
                    base_confidence = result['score']
                    confidence = self._calculate_enhanced_confidence(
                        base_confidence, processed_text, 'produtivo'
                    )
                elif result['label'] in ['4 stars', '5 stars']:
                    category = 'improdutivo'
                    # Ajustar confiança baseada na força do sentimento
                    base_confidence = result['score']
                    confidence = self._calculate_enhanced_confidence(
                        base_confidence, processed_text, 'improdutivo'
                    )
                else:
                    # Para 3 estrelas (neutro), usar classificação por palavras-chave
                    return self._keyword_based_classification(processed_text)
                
                return category, confidence
            
        except Exception as e:
            print(f"Erro na classificação: {e}")
        
        # Fallback classification based on keywords
        return self._keyword_based_classification(processed_text)
    
    def _calculate_enhanced_confidence(self, base_confidence: float, text: str, category: str) -> float:
        """Calculate enhanced confidence score based on multiple factors"""
        # Fator base do modelo de sentimento (0.0 a 1.0)
        sentiment_factor = base_confidence
        
        # Fator de palavras-chave (0.0 a 1.0)
        keyword_factor = self._calculate_keyword_factor(text, category)
        
        # Fator de estrutura do email (0.0 a 1.0)
        structure_factor = self._calculate_structure_factor(text, category)
        
        # Fator de contexto (0.0 a 1.0)
        context_factor = self._calculate_context_factor(text, category)
        
        # Calcular confiança final ponderada
        weights = {
            'sentiment': 0.4,      # 40% - modelo de sentimento
            'keywords': 0.3,       # 30% - palavras-chave
            'structure': 0.2,      # 20% - estrutura
            'context': 0.1         # 10% - contexto
        }
        
        final_confidence = (
            sentiment_factor * weights['sentiment'] +
            keyword_factor * weights['keywords'] +
            structure_factor * weights['structure'] +
            context_factor * weights['context']
        )
        
        # NOVO: Aplicar boost final para emails produtivos com características muito claras
        if category == 'produtivo':
            final_confidence = self._apply_productive_boost(final_confidence, text)
        
        # Garantir que a confiança esteja entre 0.0 e 1.0
        return max(0.0, min(1.0, final_confidence))
    
    def _apply_productive_boost(self, base_confidence: float, text: str) -> float:
        """Apply final boost for very clear productive emails"""
        boost = 0.0
        
        # Boost para emails com múltiplas características de trabalho
        work_indicators = 0
        
        # Características principais
        if any(word in text for word in ['reunião', 'meeting']):
            work_indicators += 1
        if any(word in text for word in ['planejamento', 'planning']):
            work_indicators += 1
        if any(word in text for word in ['objetivos', 'goals', 'metas']):
            work_indicators += 1
        if any(word in text for word in ['equipe', 'team']):
            work_indicators += 1
        if any(word in text for word in ['responsabilidades', 'responsibilities']):
            work_indicators += 1
        if any(word in text for word in ['cronograma', 'schedule']):
            work_indicators += 1
        if any(word in text for word in ['orçamento', 'budget']):
            work_indicators += 1
        if any(word in text for word in ['gerente', 'manager']):
            work_indicators += 1
        
        # Aplicar boost baseado no número de indicadores
        if work_indicators >= 6:
            boost += 0.25  # Boost máximo para emails muito claros
        elif work_indicators >= 5:
            boost += 0.20
        elif work_indicators >= 4:
            boost += 0.15
        elif work_indicators >= 3:
            boost += 0.10
        elif work_indicators >= 2:
            boost += 0.05
        
        # Boost adicional para combinações específicas
        if all(word in text for word in ['reunião', 'planejamento', 'objetivos']):
            boost += 0.10  # Combinação muito forte
        
        if all(word in text for word in ['equipe', 'responsabilidades', 'cronograma']):
            boost += 0.10  # Combinação muito forte
        
        # Boost para estrutura profissional
        if any(word in text for word in ['prezados', 'atenciosamente', 'cordiais']):
            boost += 0.05  # Linguagem formal
        
        if any(word in text for word in ['Q1 2024', 'Q4 2023', '23/01/2024', '14h']):
            boost += 0.05  # Detalhes específicos
        
        return base_confidence + boost
    
    def _calculate_keyword_factor(self, text: str, category: str) -> float:
        """Calculate confidence based on keyword presence and frequency"""
        if category == 'produtivo':
            productive_keywords = [
                'reunião', 'meeting', 'projeto', 'project', 'cliente', 'client',
                'trabalho', 'work', 'relatório', 'report', 'deadline', 'entrega',
                'solicitação', 'request', 'contrato', 'contract', 'avaliação',
                'performance', 'sprint', 'agenda', 'urgente', 'importante',
                'planejamento', 'planning', 'metas', 'goals', 'objetivos',
                'objectives', 'orçamento', 'budget', 'responsabilidades',
                'responsibilities', 'cronograma', 'schedule', 'empresa',
                'company', 'equipe', 'team', 'gerente', 'manager'
            ]
            keywords = productive_keywords
        else:
            unproductive_keywords = [
                'corrente', 'chain', 'reencaminhar', 'forward', 'spam', 'promoção',
                'desconto', 'discount', 'piada', 'joke', 'fofoca', 'gossip',
                'marketing', 'newsletter', 'propaganda', 'advertisement',
                'sorte', 'luck', 'abençoado', 'blessed', 'reencaminhe',
                'forward now', 'boa sorte', 'good luck', 'prosperidade',
                'prosperity', 'amor verdadeiro', 'true love', 'sucesso',
                'success', 'dinheiro inesperado', 'unexpected money'
            ]
            keywords = unproductive_keywords
        
        # Contar palavras-chave encontradas
        found_keywords = sum(1 for word in keywords if word in text)
        
        # NOVO: Calcular frequência das palavras-chave
        word_frequency = 0
        for word in keywords:
            word_frequency += text.count(word)
        
        # NOVO: Verificar posição das palavras-chave (assunto tem mais peso)
        position_bonus = 0
        lines = text.split('\n')
        if lines:
            first_line = lines[0].lower()
            for word in keywords:
                if word in first_line:
                    position_bonus += 0.1  # Bônus para palavras no início
        
        # NOVO: Verificar combinações de palavras-chave
        combination_bonus = 0
        if category == 'produtivo':
            # Combinações que indicam trabalho profissional
            if all(word in text for word in ['reunião', 'planejamento']):
                combination_bonus += 0.15
            if all(word in text for word in ['projeto', 'objetivos', 'metas']):
                combination_bonus += 0.15
            if all(word in text for word in ['equipe', 'responsabilidades', 'cronograma']):
                combination_bonus += 0.15
        else:
            # Combinações que indicam spam
            if all(word in text for word in ['corrente', 'reencaminhar', 'sorte']):
                combination_bonus += 0.15
            if all(word in text for word in ['boa sorte', 'prosperidade', 'abençoado']):
                combination_bonus += 0.15
            if all(word in text for word in ['✨', '💰', '❤️']):
                combination_bonus += 0.15
        
        # Calcular fator baseado na presença de palavras-chave
        base_score = 0.3  # Base mínima
        
        if found_keywords == 0:
            base_score = 0.2  # Muito baixa confiança se não encontrar palavras-chave
        elif found_keywords == 1:
            base_score = 0.4
        elif found_keywords == 2:
            base_score = 0.6
        elif found_keywords == 3:
            base_score = 0.75
        elif found_keywords >= 4:
            base_score = 0.9  # Alta confiança se encontrar muitas palavras-chave
        
        # Aplicar bônus de frequência
        frequency_bonus = min(0.1, word_frequency * 0.02)
        
        # Calcular score final
        final_score = base_score + frequency_bonus + position_bonus + combination_bonus
        
        return min(0.95, max(0.1, final_score))
    
    def _calculate_structure_factor(self, text: str, category: str) -> float:
        """Calculate confidence based on email structure"""
        lines = text.split('\n')
        word_count = len(text.split())
        
        if category == 'produtivo':
            # Emails produtivos tendem a ter estrutura mais formal
            structure_indicators = 0
            
            # Verificar presença de elementos estruturais
            if any(':' in line for line in lines):  # Tópicos com dois pontos
                structure_indicators += 1
            if word_count > 50:  # Emails de trabalho são mais longos
                structure_indicators += 1
            if any(line.strip().startswith('-') for line in lines):  # Listas
                structure_indicators += 1
            if any(word in text for word in ['objetivos', 'metas', 'cronograma']):
                structure_indicators += 1
            
            return min(0.9, 0.4 + (structure_indicators * 0.15))
        
        else:
            # Emails improdutivos tendem a ter estrutura mais informal
            structure_indicators = 0
            
            if any('✨' in line or '💰' in line or '❤️' in line for line in lines):  # Emojis
                structure_indicators += 1
            if any(word in text for word in ['reencaminhe', 'forward now', 'agora']):
                structure_indicators += 1
            if any(word in text for word in ['sorte', 'abençoado', 'prosperidade']):
                structure_indicators += 1
            if word_count < 30:  # Correntes são geralmente curtas
                structure_indicators += 1
            
            return min(0.9, 0.4 + (structure_indicators * 0.15))
    
    def _calculate_context_factor(self, text: str, category: str) -> float:
        """Calculate confidence based on contextual clues"""
        context_score = 0.5  # Base neutra
        
        if category == 'produtivo':
            # Verificar contexto de trabalho
            work_context_indicators = [
                'empresa', 'company', 'equipe', 'team', 'gerente', 'manager',
                'cliente', 'client', 'projeto', 'project', 'trabalho', 'work'
            ]
            
            context_matches = sum(1 for word in work_context_indicators if word in text)
            if context_matches >= 2:
                context_score = 0.8
            elif context_matches == 1:
                context_score = 0.6
            else:
                context_score = 0.4
                
        else:
            # Verificar contexto de spam/corrente
            spam_context_indicators = [
                'corrente', 'chain', 'reencaminhar', 'forward', 'spam',
                'sorte', 'luck', 'abençoado', 'blessed', 'prosperidade'
            ]
            
            context_matches = sum(1 for word in spam_context_indicators if word in text)
            if context_matches >= 2:
                context_score = 0.8
            elif context_matches == 1:
                context_score = 0.6
            else:
                context_score = 0.4
        
        return context_score
    
    def _keyword_based_classification(self, text: str) -> Tuple[str, float]:
        """Fallback classification using keyword analysis"""
        productive_keywords = [
            'reunião', 'meeting', 'projeto', 'project', 'cliente', 'client',
            'trabalho', 'work', 'relatório', 'report', 'deadline', 'entrega',
            'solicitação', 'request', 'contrato', 'contract', 'avaliação',
            'performance', 'sprint', 'agenda', 'urgente', 'importante',
            'planejamento', 'planning', 'metas', 'goals', 'objetivos',
            'objectives', 'orçamento', 'budget', 'responsabilidades',
            'responsibilities', 'cronograma', 'schedule', 'empresa',
            'company', 'equipe', 'team', 'gerente', 'manager'
        ]
        
        unproductive_keywords = [
            'corrente', 'chain', 'reencaminhar', 'forward', 'spam', 'promoção',
            'desconto', 'discount', 'piada', 'joke', 'fofoca', 'gossip',
            'marketing', 'newsletter', 'propaganda', 'advertisement',
            'sorte', 'luck', 'abençoado', 'blessed', 'reencaminhe',
            'forward now', 'boa sorte', 'good luck', 'prosperidade',
            'prosperity', 'amor verdadeiro', 'true love', 'sucesso',
            'success', 'dinheiro inesperado', 'unexpected money'
        ]
        
        productive_count = sum(1 for word in productive_keywords if word in text)
        unproductive_count = sum(1 for word in unproductive_keywords if word in text)
        
        # Determinar categoria baseada na contagem
        if productive_count > unproductive_count:
            category = 'produtivo'
            # Usar sistema de confiança aprimorado
            confidence = self._calculate_enhanced_confidence(
                0.7, text, 'produtivo'  # Base de 0.7 para classificação por palavras-chave
            )
        elif unproductive_count > productive_count:
            category = 'improdutivo'
            # Usar sistema de confiança aprimorado
            confidence = self._calculate_enhanced_confidence(
                0.7, text, 'improdutivo'  # Base de 0.7 para classificação por palavras-chave
            )
        else:
            # Se empate, usar análise mais detalhada
            if any(word in text for word in ['reunião', 'projeto', 'trabalho', 'cliente']):
                category = 'produtivo'
                confidence = self._calculate_enhanced_confidence(0.6, text, 'produtivo')
            elif any(word in text for word in ['corrente', 'reencaminhar', 'sorte', 'abençoado']):
                category = 'improdutivo'
                confidence = self._calculate_enhanced_confidence(0.6, text, 'improdutivo')
            else:
                category = 'improdutivo'
                confidence = 0.5  # Confiança baixa para casos ambíguos
        
        return category, confidence
    
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
