# Podcast de IA

Podcast diário sobre inteligência artificial, em pt-BR, com dois apresentadores
(Ana e Bia) e produção quase totalmente automatizada: um agente na nuvem busca
papers, escreve o roteiro e mantém a fila; o GitHub Actions gera o áudio e
publica uma release pra cada episódio.

## Ouvir os episódios

Cada episódio vira uma [Release](../../releases) no GitHub, com o `.mp3`
anexado como asset.

- **Pelo celular:** app do GitHub → aba **Releases** → escolhe o episódio → baixa o asset.
- **Pelo navegador:** [`releases`](../../releases) ou direto pela pasta [`audio/`](audio).

## Como o pipeline funciona

```
todo dia, 4h (horário de Brasília)
  │
  ▼
Rotina agendada na nuvem (Claude Code Routine)
  1. roda scripts/buscar_papers.py, cruza com estado/fila.md e estado/trilha.md
  2. apresenta candidatos e PERGUNTA se gera episódio hoje — espera resposta
     (a conversa fica disponível em claude.ai/code, dá pra responder do celular)
  3. escreve roteiros/epNNN-slug.md
  4. atualiza estado/fila.md e estado/trilha.md
  5. git commit + push do roteiro e do estado (não do áudio)
  │
  ▼
GitHub Actions (.github/workflows/gerar-audio.yml)
  disparado automaticamente pelo push em roteiros/**.md
  1. gera o .mp3 com edge-tts
  2. commita e dá push do áudio
  3. cria (ou atualiza) uma Release com o .mp3 anexado
```

O áudio **não** é gerado dentro da rotina na nuvem: o ambiente sandboxed dela
bloqueia o WebSocket que o `edge-tts` precisa. Por isso essa etapa foi movida
pro GitHub Actions, cujos runners não têm essa restrição.

## Estrutura

```
podcast-ia/
├── CLAUDE.md                 # instruções persistentes do produtor (regras de conteúdo)
├── PODCAST-IA-SETUP.md       # spec original de implementação
├── .github/workflows/
│   └── gerar-audio.yml       # gera áudio + cria release a cada roteiro novo
├── config/
│   ├── fontes.yaml           # fontes de papers e critérios de filtro
│   └── vozes.yaml            # vozes dos apresentadores (edge-tts / Gemini TTS)
├── estado/
│   ├── fila.md               # backlog de papers (pendente/feito/descartado)
│   └── trilha.md             # progresso da trilha base (fundamentos)
├── roteiros/
│   └── epNNN-slug.md
├── audio/
│   └── epNNN-slug.mp3
└── scripts/
    ├── buscar_papers.py      # coleta candidatos (labs + Hugging Face Daily Papers)
    ├── gerar_audio.py        # roteiro → áudio via edge-tts
    └── requirements.txt
```

## Duas trilhas de conteúdo

- **Trilha base** (`estado/trilha.md`): sequência fixa e progressiva, do zero ao
  estado da arte. Cada episódio assume só o que veio antes — nenhum termo novo
  sem definição.
- **Trilha diária**: papers recentes dos labs (Anthropic, Google DeepMind,
  OpenAI, DeepSeek) e do Hugging Face Daily Papers, só liberados depois que a
  trilha base cobrir os pré-requisitos necessários.

## Rodando localmente

Dependências Python ficam numa venv (o Python do sistema é
*externally-managed*):

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
```

Buscar candidatos a episódio:

```bash
.venv/bin/python scripts/buscar_papers.py --dias 10
```

Gerar áudio de um roteiro:

```bash
.venv/bin/python scripts/gerar_audio.py roteiros/epNNN-slug.md
```

Precisa de `ffmpeg` no PATH.

## Configuração da rotina na nuvem

A automação diária roda como uma [Claude Code Routine](https://claude.ai/code/routines),
não como GitHub Actions — ela precisa de uma sessão completa do Claude Code
(ler estado, decidir, escrever roteiro, esperar resposta), o que um workflow
de CI sozinho não faz. Detalhes de ambiente:

- **Ambiente de nuvem:** usa um ambiente customizado (não o "Default"), com
  acesso de rede liberado (`Custom`) para os domínios dos labs e do Hugging
  Face — o ambiente padrão só libera registries de pacotes.
- **Acesso ao GitHub:** feito via `/web-setup` (sincroniza um token do `gh`
  CLI autenticado localmente com a conta Claude). A conexão via GitHub App
  apresentou um bug conhecido (fica presa em autorização OAuth simples, sem
  permissão de push) — `/web-setup` contorna isso.

## Limitações conhecidas

- **DeepSeek AI (GitHub)** às vezes falha por rate limit da API não-autenticada
  do GitHub (60 requisições/hora por IP). Não é fatal — o script trata cada
  fonte de forma independente e segue com as outras.
- Upvote do Hugging Face mede popularidade, não relevância conceitual — a
  curadoria pesa adequação à trilha acima da posição no ranking (ver
  `CLAUDE.md`).
- Se uma fonte voltar vazia por vários dias seguidos, é sinal de que o
  scraping quebrou, não de que o lab parou de publicar.
