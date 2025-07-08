import os
import re
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Define BOTH www and non-www origins for robustness
# Your custom domain on Netlify might be accessible via both
netlify_app_url_apex = "https://burlometro.pt"  # Apex/root domain
netlify_app_url_www = "https://www.burlometro.pt" # 'www' subdomain

CORS(app, resources={
    r"/api/*": {
        "origins": [netlify_app_url_apex, netlify_app_url_www, "http://localhost:*", "http://127.0.0.1:*"]
    }
})

# ... rest of your server.py ...
#CORS(app)

PORT = int(os.getenv('PORT', 3000))

def perform_simple_analysis(text):
    """Perform rule-based scam analysis as fallback"""
    text_lower = text.lower()
    
    scam_indicators = [
        'urgente', 'imediatamente', 'último dia', 'oferta limitada',
        'clique aqui', 'verifique agora', 'confirme os dados',
        'conta bloqueada', 'suspensa', 'dados bancários',
        'transferência', 'prémio', 'ganhou', 'sorteio',
        'phishing', 'bitcoin', 'criptomoeda', 'nib', 'iban',
        'multibanco', 'cartão de crédito', 'password',
        'código de segurança', 'pin', 'dados pessoais',
        'validar conta', 'atualizar dados', 'expirou',
        'desconto especial', 'oferta exclusiva', 'apenas hoje',
        'clique no link', 'download', 'instale agora',
        'vírus detectado', 'computador infetado'
    ]

    official_entities = [
        'banco', 'caixa geral', 'millennium', 'santander',
        'ctt', 'correios', 'emel', 'edp', 'nos', 'meo',
        'vodafone', 'segurança social', 'finanças', 'at',
        'tribunal', 'polícia', 'gnr', 'psp'
    ]

    found_indicators = [indicator for indicator in scam_indicators if indicator in text_lower]
    mentions_official_entity = any(entity in text_lower for entity in official_entities)
    
    suspicious_urls = re.findall(r'https?://[^\s]+', text)
    has_long_numbers = bool(re.search(r'\d{6,}', text))
    has_multiple_exclamations = text.count('!') > 2
    has_capital_words = len(re.findall(r'[A-Z]{3,}', text)) > 1
    
    risk_score = 0
    
    # Calculate risk score
    risk_score += len(found_indicators) * 15
    if suspicious_urls:
        risk_score += 25
    if has_long_numbers:
        risk_score += 20
    if mentions_official_entity and found_indicators:
        risk_score += 30
    if has_multiple_exclamations:
        risk_score += 10
    if has_capital_words:
        risk_score += 15

    # Determine risk level
    risk_level = 'safe'
    is_scam = False

    if risk_score >= 70:
        risk_level = 'scam'
        is_scam = True
    elif risk_score >= 35:
        risk_level = 'warning'

    confidence = min(max(risk_score + 10, 20), 95)

    return {
        'is_scam': is_scam,
        'confidence': confidence,
        'risk_level': risk_level,
        'explanation': get_risk_explanation(risk_level, found_indicators, mentions_official_entity),
        'indicators': found_indicators
    }

def get_risk_explanation(risk_level, indicators, mentions_official):
    """Generate explanation based on risk level"""
    if risk_level == 'safe':
        return 'A mensagem parece ser legítima. Não foram encontrados indicadores significativos de burla.'
    elif risk_level == 'warning':
        warning_text = f"A mensagem contém alguns elementos suspeitos{': ' + ', '.join(indicators[:3]) if indicators else ''}. "
        return warning_text + 'Tenha cuidado e verifique sempre a fonte antes de fornecer qualquer informação.'
    elif risk_level == 'scam':
        scam_text = '🚨 ATENÇÃO: Esta mensagem tem várias características típicas de burla'
        if indicators:
            scam_text += f", incluindo: {', '.join(indicators[:4])}"
        if mentions_official:
            scam_text += '. A mensagem parece imitar uma entidade oficial'
        scam_text += '. NÃO forneça informações pessoais, não clique em links e não faça transferências.'
        return scam_text
    else:
        return 'Análise inconclusiva.'

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for scam analysis"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'error': 'Mensagem é obrigatória'}), 400

        # Check if OpenRouter API key is available
        openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        if not openrouter_api_key:
            print('OpenRouter API key not found, using fallback analysis')
            analysis = perform_simple_analysis(message)
            return jsonify(analysis)

        # Call OpenRouter API
        headers = {
            'Authorization': f'Bearer {openrouter_api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://burlometro.pt/',
            'X-Title': 'Burlómetro'
        }

        payload = {
            'model': 'deepseek/deepseek-chat-v3-0324:free',
            'messages': [
                {
                    'role': 'system',
                    'content': '''Você é um especialista em deteção de burlas e mensagens fraudulentas em português. Analise a mensagem fornecida e determine se é uma tentativa de burla/scam. 

Considere indicadores como:
- Urgência excessiva
- Pedidos de informação pessoal/financeira
- Links suspeitos
- Erros ortográficos propositais
- Ofertas irrealistas
- Pressão para ação imediata
- Imitação de entidades oficiais (bancos, correios, etc.)
- Prémios ou sorteios falsos
- Ameaças de suspensão de conta

IMPORTANTE: Responda APENAS com JSON puro, sem markdown, sem ```json, sem formatação adicional. Apenas o objeto JSON:

{
  "is_scam": boolean,
  "confidence": number (0-100),
  "risk_level": "safe" | "warning" | "scam",
  "explanation": "explicação detalhada em português",
  "indicators": ["lista", "de", "indicadores", "encontrados"]
}'''
                },
                {
                    'role': 'user',
                    'content': f'Analise esta mensagem: "{message}"'
                }
            ],
            'temperature': 0.3,
            'max_tokens': 500
        }

        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )

        if not response.ok:
            raise Exception(f'OpenRouter API error: {response.status_code}')

        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content']
        print('Raw AI response:', ai_response)
        
        try:
            # Clean the response by removing markdown code blocks if present
            cleaned_response = ai_response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = re.sub(r'^```json\n?', '', cleaned_response)
                cleaned_response = re.sub(r'\n?```$', '', cleaned_response)
            elif cleaned_response.startswith('```'):
                cleaned_response = re.sub(r'^```\n?', '', cleaned_response)
                cleaned_response = re.sub(r'\n?```$', '', cleaned_response)
            
            print('Cleaned response:', cleaned_response)
            analysis = json.loads(cleaned_response)
            return jsonify(analysis)
        except json.JSONDecodeError as parse_error:
            print('Error parsing AI response:', parse_error)
            print('Cleaned response was:', cleaned_response)
            fallback_analysis = perform_simple_analysis(message)
            return jsonify(fallback_analysis)

    except Exception as error:
        print('Error in analysis:', error)
        
        # Fallback to simple rule-based analysis
        analysis = perform_simple_analysis(data.get('message', ''))
        return jsonify(analysis)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK', 
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f'🛡️  Burlómetro server running on http://localhost:{PORT}')
    app.run(host='0.0.0.0', port=PORT, debug=False)
