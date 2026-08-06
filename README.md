# Meu Bot IA

Bot de Discord com personalidade própria, usando a API da OpenAI (com function
calling) para responder mensagens, saber a data/hora atual e pesquisar na web
via Tavily.

## Estrutura

```
meu_bot_ia/
├── main.py                  # ponto de entrada
├── config.py                 # variáveis de ambiente
├── core/
│   ├── personality.py         # personalidade / system prompt
│   ├── ai_client.py           # chamadas à OpenAI + loop de function calling
│   ├── tools_manager.py        # registro central das ferramentas
│   └── memory.py                # histórico de conversa por canal
├── tools/
│   ├── datetime_tool.py         # data/hora atual
│   └── search_tool.py            # pesquisa via Tavily
├── discord_bot/
│   ├── events.py                  # on_ready, on_message (menções)
│   └── commands.py                 # comandos como !reset
└── utils/
    └── logger.py                   # logging padronizado
```

## Como rodar

1. Crie um ambiente virtual (opcional mas recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e preencha com suas chaves:
   ```
   DISCORD_TOKEN=...
   OPENAI_API_KEY=...
   TAVILY_API_KEY=...
   ```

4. Edite `core/personality.py` com a personalidade que você quer.

5. No Portal de Desenvolvedores do Discord, ative os **Privileged Gateway
   Intents** "MESSAGE CONTENT" e "SERVER MEMBERS" pro seu bot — sem isso ele
   não consegue ler o conteúdo das mensagens.

6. Rode:
   ```
   python main.py
   ```

## Como usar

- Mencione o bot (`@NomeDoBot sua pergunta`) em qualquer canal que ele tenha
  acesso, e ele responde usando a IA.
- `!reset` limpa o histórico de conversa daquele canal.

## Próximos passos (fase de voz)

Quando você for adicionar a parte de call (STT/TTS), a ideia é criar
`discord_bot/voice.py` reaproveitando a mesma função `gerar_resposta()` de
`core/ai_client.py` — ela já recebe texto e devolve texto, então o fluxo de
voz vai ser: áudio → STT → texto → `gerar_resposta()` → texto → TTS → áudio.
Isso mantém o "cérebro" da IA igual, só troca a entrada/saída.

Pra adicionar uma nova ferramenta (function calling) no futuro, o padrão é
sempre o mesmo:
1. Criar um arquivo em `tools/`, com um `TOOL_SCHEMA` e uma função.
2. Registrar os dois em `core/tools_manager.py` (`TOOLS_SCHEMA` e `TOOLS_MAP`).

Nenhum outro arquivo precisa mudar.
