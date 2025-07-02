const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('.')); // Serve static files from current directory

// API endpoint for scam analysis
app.post('/api/analyze', async (req, res) => {
  try {
    const { message } = req.body;

    if (!message || message.trim().length === 0) {
      return res.status(400).json({ error: 'Mensagem é obrigatória' });
    }

    // Check if OpenRouter API key is available
    if (!process.env.OPENROUTER_API_KEY) {
      console.log('OpenRouter API key not found, using fallback analysis');
      const analysis = performSimpleAnalysis(message);
      return res.json(analysis);
    }

    // Call OpenRouter API
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:3000',
        'X-Title': 'Burlómetro'
      },
      body: JSON.stringify({
        model: 'deepseek/deepseek-chat-v3-0324:free',
        messages: [
          {
            role: 'system',
            content: `Você é um especialista em deteção de burlas e mensagens fraudulentas em português. Analise a mensagem fornecida e determine se é uma tentativa de burla/scam. 

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

IMPORTANTE: Responda APENAS com JSON puro, sem markdown, sem \`\`\`json, sem formatação adicional. Apenas o objeto JSON:

{
  "is_scam": boolean,
  "confidence": number (0-100),
  "risk_level": "safe" | "warning" | "scam",
  "explanation": "explicação detalhada em português",
  "indicators": ["lista", "de", "indicadores", "encontrados"]
}`
          },
          {
            role: 'user',
            content: `Analise esta mensagem: "${message}"`
          }
        ],
        temperature: 0.3,
        max_tokens: 500
      })
    });

    if (!response.ok) {
      throw new Error(`OpenRouter API error: ${response.status}`);
    }

    const data = await response.json();
    const aiResponse = data.choices[0].message.content;
    console.log('Raw AI response:', aiResponse);
    
    try {
      // Clean the response by removing markdown code blocks if present
      let cleanedResponse = aiResponse.trim();
      if (cleanedResponse.startsWith('```json')) {
        cleanedResponse = cleanedResponse.replace(/```json\n?/, '').replace(/\n?```$/, '');
      } else if (cleanedResponse.startsWith('```')) {
        cleanedResponse = cleanedResponse.replace(/```\n?/, '').replace(/\n?```$/, '');
      }
      
      console.log('Cleaned response:', cleanedResponse);
      const analysis = JSON.parse(cleanedResponse);
      res.json(analysis);
    } catch (parseError) {
      console.error('Error parsing AI response:', parseError);
      console.error('Cleaned response was:', cleanedResponse);
      const fallbackAnalysis = performSimpleAnalysis(message);
      res.json(fallbackAnalysis);
    }

  } catch (error) {
    console.error('Error in analysis:', error);
    
    // Fallback to simple rule-based analysis
    const analysis = performSimpleAnalysis(req.body.message);
    res.json(analysis);
  }
});

function performSimpleAnalysis(text) {
  const textLower = text.toLowerCase();
  
  const scamIndicators = [
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
  ];

  const officialEntities = [
    'banco', 'caixa geral', 'millennium', 'santander',
    'ctt', 'correios', 'emel', 'edp', 'nos', 'meo',
    'vodafone', 'segurança social', 'finanças', 'at',
    'tribunal', 'polícia', 'gnr', 'psp'
  ];

  const foundIndicators = scamIndicators.filter(indicator => 
    textLower.includes(indicator)
  );

  const mentionsOfficialEntity = officialEntities.some(entity =>
    textLower.includes(entity)
  );

  const suspiciousUrls = text.match(/https?:\/\/[^\s]+/g) || [];
  const hasLongNumbers = /\d{6,}/.test(text); // Long numbers (like account numbers)
  const hasMultipleExclamations = (text.match(/!/g) || []).length > 2;
  const hasCapitalWords = (text.match(/[A-Z]{3,}/g) || []).length > 1;
  
  let riskScore = 0;
  
  // Calculate risk score
  riskScore += foundIndicators.length * 15;
  if (suspiciousUrls.length > 0) riskScore += 25;
  if (hasLongNumbers) riskScore += 20;
  if (mentionsOfficialEntity && foundIndicators.length > 0) riskScore += 30;
  if (hasMultipleExclamations) riskScore += 10;
  if (hasCapitalWords) riskScore += 15;

  // Determine risk level
  let riskLevel = 'safe';
  let isScam = false;

  if (riskScore >= 70) {
    riskLevel = 'scam';
    isScam = true;
  } else if (riskScore >= 35) {
    riskLevel = 'warning';
  }

  const confidence = Math.min(Math.max(riskScore + 10, 20), 95);

  return {
    is_scam: isScam,
    confidence: confidence,
    risk_level: riskLevel,
    explanation: getRiskExplanation(riskLevel, foundIndicators, mentionsOfficialEntity),
    indicators: foundIndicators
  };
}

function getRiskExplanation(riskLevel, indicators, mentionsOfficial) {
  switch (riskLevel) {
    case 'safe':
      return 'A mensagem parece ser legítima. Não foram encontrados indicadores significativos de burla.';
    case 'warning':
      const warningText = `A mensagem contém alguns elementos suspeitos${indicators.length > 0 ? `: ${indicators.slice(0, 3).join(', ')}` : ''}. `;
      return warningText + 'Tenha cuidado e verifique sempre a fonte antes de fornecer qualquer informação.';
    case 'scam':
      let scamText = '🚨 ATENÇÃO: Esta mensagem tem várias características típicas de burla';
      if (indicators.length > 0) {
        scamText += `, incluindo: ${indicators.slice(0, 4).join(', ')}`;
      }
      if (mentionsOfficial) {
        scamText += '. A mensagem parece imitar uma entidade oficial';
      }
      scamText += '. NÃO forneça informações pessoais, não clique em links e não faça transferências.';
      return scamText;
    default:
      return 'Análise inconclusiva.';
  }
}

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Serve the main page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.listen(PORT, () => {
  console.log(`🛡️  Burlómetro server running on http://localhost:${PORT}`);
  console.log(`💡 Add your OpenRouter API key to .env file as OPENROUTER_API_KEY=your_key_here`);
});
