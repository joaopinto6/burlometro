# 🛡️ Burlómetro - Detector de Burlas

Um detector inteligente de mensagens suspeitas que utiliza IA e OCR para identificar tentativas de burla/scam.

Aplicação web moderna com backend em **Python Flask** e frontend responsivo.

## ✨ Funcionalidades

- 📝 **Análise de Texto**: Cole o texto da mensagem suspeita
- 📷 **OCR de Imagens**: Carregue screenshots de mensagens para extração automática de texto
- 🤖 **IA Avançada**: Utiliza modelos de linguagem para análise inteligente
- 📱 **Design Responsivo**: Interface moderna inspirada no iPhone Messages
- 🔒 **Análise Segura**: Processamento local e API segura
- 🌐 **SEO Otimizado**: Meta tags e structured data para melhor indexação

## 🚀 Como Usar

### Configuração do Servidor Flask

1. **Clone o repositório ou descarregue os ficheiros**

2. **Instale o Python 3.7+** se ainda não tiver

3. **Instale as dependências Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a API (Opcional)**:
   - Crie um ficheiro `.env` com:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```
   - Obtenha uma chave gratuita em: https://openrouter.ai/

5. **Inicie o servidor Flask**:
   ```bash
   python server.py
   ```

6. **Abra o browser** em `http://localhost:3000`

### Desenvolvimento

Para desenvolvimento com auto-reload:
```bash
# Ative o modo debug no server.py (já está ativado por padrão)
python server.py
```

## 🔧 Como Funciona

### Análise de Texto
1. Digite ou cole a mensagem suspeita
2. Clique em "Analisar Mensagem"
3. O sistema analisa indicadores de burla usando IA ou regras locais
4. Receba um relatório detalhado com nível de risco

### Análise de Imagem
1. Clique no separador "Imagem"
2. Carregue uma screenshot da mensagem
3. O OCR (Tesseract.js) extrai automaticamente o texto
4. A análise procede automaticamente

## 🧠 Indicadores de Burla

O sistema deteta:
- ⚡ Urgência excessiva ("último dia", "imediatamente")
- 💳 Pedidos de dados bancários/pessoais
- 🔗 Links suspeitos
- 🏛️ Imitação de entidades oficiais (bancos, CTT, EDP, etc.)
- 🎁 Ofertas irrealistas e prémios falsos
- ❗ Pressão para ação imediata
- 🎯 Padrões típicos de phishing
- 📱 Erros ortográficos propositais

## 🎨 Interface

- **Design Minimalista**: Inspirado na interface do iPhone Messages
- **Cores Intuitivas**: 
  - 🟢 Verde para mensagens seguras
  - 🟡 Amarelo para atenção
  - 🔴 Vermelho para burlas detectadas
- **Responsivo**: Funciona perfeitamente em mobile e desktop
- **Acessível**: Suporte para screen readers e navegação por teclado

## 🔧 Tecnologias Utilizadas

### Backend
- **Python Flask**: Servidor web principal
- **Flask-CORS**: Suporte para CORS
- **python-dotenv**: Gestão de variáveis de ambiente
- **requests**: Cliente HTTP para APIs externas

### Frontend
- **HTML5, CSS3, JavaScript**: Interface moderna e responsiva
- **Tesseract.js**: OCR no browser para extração de texto
- **CSS Grid/Flexbox**: Layout responsivo
- **Progressive Web App**: Suporte para instalação

### IA e Análise
- **OpenRouter API**: DeepSeek Chat para análise avançada
- **Análise Fallback**: Regras baseadas em padrões portugueses
- **Regex**: Deteção de URLs, números suspeitos, etc.

## 📊 Níveis de Risco

1. **✅ Seguro (safe)**: Mensagem parece legítima
2. **⚠️ Atenção (warning)**: Contém elementos suspeitos 
3. **🚨 Burla (scam)**: Alta probabilidade de ser fraudulenta

Cada análise inclui:
- Nível de confiança (0-100%)
- Explicação detalhada
- Lista de indicadores encontrados

## 🔒 Privacidade e Segurança

- ✅ Processamento no seu servidor Flask
- ✅ Não armazena mensagens
- ✅ API keys protegidas com variáveis de ambiente
- ✅ CORS configurado para domínios específicos
- ✅ Análise local como fallback sem internet
- ✅ OCR processado localmente no browser

## 📁 Estrutura do Projeto

```
burlometro/
├── server.py              # Servidor Flask principal
├── index.html             # Interface web
├── requirements.txt       # Dependências Python
├── robots.txt             # SEO - Instruções para crawlers
├── sitemap.xml            # SEO - Mapa do site
├── favicon_io/            # Ícones da aplicação
│   ├── favicon.ico
│   ├── android-chrome-*.png
│   └── site.webmanifest
├── LICENSE                # Licença MIT
└── README.md              # Este ficheiro
```

## 🌐 SEO e Performance

- ✅ Meta tags otimizadas para Portugal
- ✅ Open Graph e Twitter Cards
- ✅ Structured data (JSON-LD)
- ✅ Sitemap.xml e robots.txt
- ✅ Favicons para todas as plataformas
- ✅ Progressive Web App capabilities

## 📝 Configuração de Produção

### Variáveis de Ambiente (.env)
```bash
OPENROUTER_API_KEY=sk-or-your-api-key-here
```

### Deploy
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em produção
python server.py
```

## 🤝 Contribuir

Contribuições são bem-vindas! Este projeto ajuda a proteger utilizadores portugueses contra burlas online.

### Como contribuir:
1. Fork este repositório
2. Crie uma branch para a sua funcionalidade
3. Teste as suas alterações
4. Submeta um Pull Request

## ⚠️ Aviso Legal

Esta ferramenta é apenas para fins educativos e informativos. Sempre confirme a legitimidade de mensagens através de canais oficiais das entidades mencionadas.

## 📞 Suporte

- 🐛 **Bugs**: Abra uma issue no GitHub
- 💡 **Sugestões**: Contribua com ideias
- 📧 **Contacto**: Para questões de segurança

---

**Mantenha-se seguro online! 🛡️**

*Projeto desenvolvido para proteger utilizadores portugueses contra burlas digitais*
