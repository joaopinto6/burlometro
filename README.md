# 🛡️ Burlómetro - Detector de Burlas

Um detector inteligente de mensagens suspeitas que utiliza IA e OCR para identificar tentativas de burla/scam.

## ✨ Funcionalidades

- 📝 **Análise de Texto**: Cole o texto da mensagem suspeita
- 📷 **OCR de Imagens**: Carregue screenshots de mensagens para extração automática de texto
- 🤖 **IA Avançada**: Utiliza modelos de linguagem para análise inteligente
- 📱 **Design Responsivo**: Interface moderna inspirada no iPhone Messages
- 🔒 **Análise Segura**: Processamento local e API segura

## 🚀 Como Usar

### Instalação

1. **Clone o repositório ou descarregue os ficheiros**

2. **Instale as dependências**:
   ```bash
   npm install
   ```

3. **Configure a API (Opcional)**:
   - Copie `.env.example` para `.env`
   - Adicione a sua chave da OpenRouter API:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     ```
   - Obtenha uma chave gratuita em: https://openrouter.ai/

4. **Inicie o servidor**:
   ```bash
   npm start
   ```

5. **Abra o browser** em `http://localhost:3000`

### Desenvolvimento

Para desenvolvimento com auto-reload:
```bash
npm run dev
```

## 🔧 Como Funciona

### Análise de Texto
1. Digite ou cole a mensagem suspeita
2. Clique em "Analisar Mensagem"
3. O sistema analisa indicadores de burla
4. Receba um relatório detalhado com nível de risco

### Análise de Imagem
1. Clique no separador "Imagem"
2. Carregue uma screenshot da mensagem
3. O OCR extrai automaticamente o texto
4. A análise procede como no modo texto

## 🧠 Indicadores de Burla

O sistema deteta:
- ⚡ Urgência excessiva
- 💳 Pedidos de dados bancários/pessoais
- 🔗 Links suspeitos
- 🏛️ Imitação de entidades oficiais
- 🎁 Ofertas irrealistas
- ❗ Pressão para ação imediata
- 🎯 Erros ortográficos propositais

## 🎨 Interface

- **Design Minimalista**: Inspirado na interface do iPhone Messages
- **Cores Intuitivas**: 
  - 🟢 Verde para mensagens seguras
  - 🟡 Amarelo para atenção
  - 🔴 Vermelho para burlas detectadas
- **Responsivo**: Funciona perfeitamente em mobile e desktop

## 🔧 Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Node.js, Express
- **OCR**: Tesseract.js
- **IA**: OpenRouter API (DeepSeek Chat)
- **Análise Fallback**: Regras baseadas em padrões

## 📊 Níveis de Risco

1. **✅ Seguro**: Mensagem parece legítima
2. **⚠️ Atenção**: Contém elementos suspeitos
3. **🚨 Burla**: Alta probabilidade de ser fraudulenta

## 🔒 Privacidade e Segurança

- ✅ Processamento no seu servidor
- ✅ Não armazena mensagens
- ✅ API keys protegidas no backend
- ✅ Análise local como fallback

## 📝 Notas

- **Sem API Key**: O sistema funciona com análise baseada em regras locais
- **Com API Key**: Análise avançada com IA para maior precisão
- **OCR**: Funciona melhor com imagens claras e texto legível

## 🤝 Contribuir

Contribuições são bem-vindas! Este projeto ajuda a proteger utilizadores contra burlas.

## ⚠️ Aviso Legal

Esta ferramenta é apenas para fins educativos e informativos. Sempre confirme a legitimidade de mensagens através de canais oficiais.

---

**Mantenha-se seguro online! 🛡️**
