# Pipeline: Podcast de IA automatizado

Spec de implementação. Abra esta pasta com o Claude Code e peça:
**"leia o PODCAST-IA-SETUP.md e implemente o projeto"**.

---

## 0. O que este projeto faz

Um pipeline que, todo dia:

1. Busca papers novos nos labs prioritários (Anthropic, Google/DeepMind, OpenAI, DeepSeek) e no Hugging Face Daily Papers;
2. Filtra por relevância e pergunta ao usuário se quer episódio hoje;
3. Se sim, gera um roteiro didático em pt-BR;
4. Sintetiza o roteiro em `.mp3` via TTS;
5. Mantém uma fila persistente — o que foi recusado hoje continua disponível amanhã.

Há duas trilhas de conteúdo rodando em paralelo:

- **Trilha base (fundamentos):** sequência fixa e progressiva, do zero ao estado da arte.
- **Trilha diária (novidades):** papers recentes, só liberados depois que a base cobriu os pré-requisitos.

---

## 1. Estrutura de pastas

```
podcast-ia/
├── PODCAST-IA-SETUP.md      # este arquivo
├── CLAUDE.md                 # instruções persistentes p/ o Claude Code
├── .env                      # chaves de API (NUNCA commitar)
├── config/
│   ├── fontes.yaml           # feeds e critérios de filtro
│   └── vozes.yaml            # config dos apresentadores
├── estado/
│   ├── fila.md               # backlog de papers (pendente/feito/descartado)
│   └── trilha.md             # progresso da trilha base
├── roteiros/
│   └── ep001-o-que-e-ia.md
├── audio/
│   └── ep001-o-que-e-ia.mp3
└── scripts/
    ├── buscar_papers.py
    ├── gerar_audio.py
    └── requirements.txt
```

---

## 2. `config/fontes.yaml`

Hierarquia: labs primeiro (já são curados), arXiv só como rede de segurança.

```yaml
prioridade_1_labs:
  - nome: Anthropic Research
    url: https://www.anthropic.com/research
    tipo: scrape
  - nome: Transformer Circuits
    url: https://transformer-circuits.pub/
    tipo: scrape
  - nome: Google DeepMind Research
    url: https://deepmind.google/research/publications/
    tipo: scrape
  - nome: OpenAI
    url: https://openai.com/news/research/
    tipo: scrape
  - nome: DeepSeek AI (GitHub)
    url: https://api.github.com/orgs/deepseek-ai/repos?sort=updated
    tipo: api

prioridade_2_curadoria:
  nome: Hugging Face Daily Papers
  url: https://huggingface.co/api/daily_papers   # confirme o formato ao implementar
  tipo: api
  janela: ontem        # NÃO use o dia corrente — upvotes ainda estão subindo
  puxar_top: 10        # puxe 10 e filtre por adequação à trilha; top-2 cego é ruim
  ordenar_por: upvotes

criterios_descarte:
  - papers puramente de benchmark sem contribuição conceitual
  - papers que exigem pré-requisito ainda não coberto na trilha base
  - duplicatas (mesmo trabalho no blog do lab e no HF → manter só o blog)
  - papers cujo apelo é a demo/pesos abertos, sem ideia nova por trás

max_candidatos_por_dia: 3
```

---

## 3. `estado/fila.md`

Formato que o Claude Code lê e reescreve a cada execução. Markdown puro de propósito —
você consegue editar na mão.

```markdown
# Fila de papers

## Pendentes
- [ ] 2026-08-24 | Anthropic | Título do paper | url | pré-req: RAG | motivo: recusado 24/08
- [ ] 2026-08-25 | DeepSeek | Título do paper | url | pré-req: MoE | motivo: recusado 25/08

## Feitos
- [x] 2026-08-20 | Google | Título | url | → audio/ep014-titulo.mp3

## Descartados
- 2026-08-22 | HF Daily | Título | url | motivo: benchmark sem contribuição conceitual
```

**Regra crítica:** "não hoje" move para `Pendentes` com a data. Nunca some.
Só vai para `Descartados` se o usuário disser explicitamente "descarta".

---

## 4. `estado/trilha.md` — a progressão base

```markdown
# Trilha base — progressão

- [x] 01. O que é IA? (IA simbólica vs. estatística, por que "aprender")
- [ ] 02. O que é Machine Learning? (dados, features, treino vs. inferência)
- [ ] 03. Aprendizado supervisionado, não-supervisionado e por reforço
- [ ] 04. Redes neurais: o neurônio, camadas, backpropagation
- [ ] 05. Deep Learning e por que 2012 mudou tudo
- [ ] 06. Embeddings: como texto vira número
- [ ] 07. Atenção e o Transformer
- [ ] 08. O que é um LLM? Pré-treino, tokens, escala
- [ ] 09. Fine-tuning, RLHF e alinhamento
- [ ] 10. RAG: por que o modelo precisa consultar coisas
- [ ] 11. Agentes: tool use, planejamento, loops
- [ ] 12. Mixture of Experts e eficiência
- [ ] 13. Raciocínio: chain-of-thought e modelos de reasoning
- [ ] 14. Interpretabilidade: o que acontece dentro do modelo
- [ ] 15. Avaliação e limites: alucinação, benchmarks, red teaming
- [ ] 16. Estado da arte — ponte para a trilha diária
```

Cada episódio assume **só** o que veio antes. Nenhum termo novo sem definição.

---

## 5. Formato do roteiro

`roteiros/epNNN-slug.md`. Falas explícitas, porque o TTS lê literalmente.

```markdown
---
episodio: 003
titulo: Aprendizado supervisionado, não-supervisionado e por reforço
duracao_alvo_min: 12
prereq: [01, 02]
fontes:
  - url: ...
---

[ANA] Oi, gente. No episódio passado a gente fechou com uma ideia solta...

[LEO] Deixa eu tentar resumir pra ver se peguei. Você tá dizendo que...

[ANA] Exato. E aqui entra a primeira das três famílias...
```

Regras de roteiro:
- Frases curtas. Voz falada, não escrita.
- Toda sigla é expandida na primeira aparição.
- Números e fórmulas viram linguagem: "cerca de setenta por cento", não "~70%".
- Blocos de no máximo ~2.500 caracteres entre marcadores `[ANA]`/`[LEO]` para o chunking do TTS.
- Cada episódio abre recapitulando o anterior em 30 segundos.

---

## 6. `scripts/gerar_audio.py`

Duas implementações. Comece pela gratuita.

### Opção A — edge-tts (grátis, sem chave de API)

```python
"""Gera áudio do roteiro usando edge-tts. Custo zero, roda local."""
import asyncio, re, sys, subprocess
from pathlib import Path
import edge_tts

VOZES = {
    "ANA": "pt-BR-FranciscaNeural",
    "LEO": "pt-BR-AntonioNeural",
}

def parse_roteiro(path: Path) -> list[tuple[str, str]]:
    texto = path.read_text(encoding="utf-8")
    if texto.startswith("---"):
        texto = texto.split("---", 2)[2]  # descarta o frontmatter
    partes = re.split(r"\[(ANA|LEO)\]", texto)
    falas = []
    for i in range(1, len(partes), 2):
        speaker = partes[i]
        fala = partes[i + 1].strip()
        if fala:
            falas.append((speaker, fala))
    return falas

async def sintetizar(falas, tmpdir: Path) -> list[Path]:
    arquivos = []
    for idx, (speaker, texto) in enumerate(falas):
        out = tmpdir / f"{idx:04d}.mp3"
        comm = edge_tts.Communicate(texto, VOZES[speaker], rate="+5%")
        await comm.save(str(out))
        arquivos.append(out)
        print(f"  [{idx+1}/{len(falas)}] {speaker}: {texto[:50]}...")
    return arquivos

def concatenar(arquivos: list[Path], destino: Path):
    lista = destino.parent / "_concat.txt"
    lista.write_text("\n".join(f"file '{a.resolve()}'" for a in arquivos))
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lista), "-c", "copy", str(destino)],
        check=True, capture_output=True,
    )
    lista.unlink()

def main():
    roteiro = Path(sys.argv[1])
    destino = Path("audio") / f"{roteiro.stem}.mp3"
    destino.parent.mkdir(exist_ok=True)
    tmpdir = Path(".tmp_audio"); tmpdir.mkdir(exist_ok=True)

    falas = parse_roteiro(roteiro)
    print(f"{len(falas)} falas encontradas.")
    arquivos = asyncio.run(sintetizar(falas, tmpdir))
    concatenar(arquivos, destino)
    for a in arquivos: a.unlink()
    tmpdir.rmdir()
    print(f"Pronto: {destino}")

if __name__ == "__main__":
    main()
```

Dependências: `pip install edge-tts` e `ffmpeg` no PATH.

### Opção B — Gemini TTS multi-speaker (pago, duas vozes conversando)

Troque só a função de síntese. Pontos de atenção documentados pelo Google:
o modo multi-speaker aceita **exatamente 2 vozes**; a qualidade **degrada acima de
poucos minutos**, então o chunking é obrigatório; e o modelo às vezes retorna
tokens de texto no lugar de áudio, gerando **erro 500** — precisa de retry.

```python
"""Gera áudio via Gemini TTS multi-speaker. Requer GEMINI_API_KEY."""
import os, time, wave
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-preview-tts"  # confira o nome atual na doc
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def agrupar_em_blocos(falas, max_chars=2000):
    """Junta falas consecutivas até o limite — evita drift de qualidade."""
    blocos, atual, tam = [], [], 0
    for speaker, texto in falas:
        if tam + len(texto) > max_chars and atual:
            blocos.append(atual); atual, tam = [], 0
        atual.append((speaker, texto)); tam += len(texto)
    if atual: blocos.append(atual)
    return blocos

def sintetizar_bloco(bloco, tentativas=3):
    prompt = "Leia este trecho de podcast em português brasileiro, tom curioso e didático:\n\n"
    prompt += "\n".join(f"{s}: {t}" for s, t in bloco)

    cfg = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="ANA",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="LEO",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
                        ),
                    ),
                ]
            )
        ),
    )
    for n in range(tentativas):
        try:
            r = client.models.generate_content(model=MODEL, contents=prompt, config=cfg)
            return r.candidates[0].content.parts[0].inline_data.data
        except Exception as e:
            print(f"  retry {n+1}/{tentativas}: {e}")
            time.sleep(2 ** n)
    raise RuntimeError("falhou após todas as tentativas")

def salvar_wav(pcm: bytes, path: str):
    with wave.open(path, "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
        f.writeframes(pcm)
```

Concatene os `.wav` com o mesmo `ffmpeg concat` da Opção A.

---

## 7. `CLAUDE.md` — instruções persistentes

Crie na raiz. O Claude Code lê automaticamente em toda sessão.

```markdown
# Projeto: Podcast de IA

## Papel
Você é o produtor deste podcast. Escreve roteiros didáticos em pt-BR e mantém a fila.

## Regras invioláveis
1. Nunca introduza um conceito que não tenha sido coberto em episódio anterior
   ou definido dentro do próprio episódio. Consulte estado/trilha.md antes de escrever.
2. Público-alvo: pessoa inteligente e sem formação em IA. Zero matemática exposta.
3. "Não hoje" NUNCA descarta um paper — move para Pendentes em estado/fila.md.
4. Priorize papers dos blogs dos labs (Anthropic, Google/DeepMind, OpenAI, DeepSeek)
   sobre o Hugging Face. Anthropic e OpenAI raramente aparecem no HF — se uma semana
   inteira vier só de HF, avise: significa que o scraping dos blogs quebrou.
5. Upvote do HF mede popularidade, não relevância conceitual. Ao escolher entre os 10
   candidatos, pese adequação à trilha acima da posição no ranking.
6. Todo roteiro cita as fontes no frontmatter. Sem fonte, sem episódio.
7. Se um paper de 2026 depende de um conceito que a trilha base ainda não cobriu,
   avise e sugira o episódio de fundamento antes.

## Comandos que eu vou usar
- "buscar papers" → roda scripts/buscar_papers.py, mostra candidatos + pendentes da fila
- "episódio N" → escreve roteiros/epNNN-slug.md a partir de estado/trilha.md
- "episódio sobre <paper>" → escreve roteiro a partir de um item da fila
- "gerar áudio epNNN" → roda scripts/gerar_audio.py
- "status" → mostra progresso da trilha e tamanho da fila
```

---

## 8. Agendamento diário

Duas rotas, escolha uma:

**Rota A — tarefa agendada do Claude Code Desktop.** Roda na sua máquina, com acesso
aos arquivos do projeto. Só executa com o app aberto e o PC ligado. Na sidebar:
Routines → New routine → Local. Prompt:

> Todo dia às 8h, na pasta `podcast-ia`: rode `scripts/buscar_papers.py`, leia
> `estado/fila.md`, e me apresente até 3 candidatos juntando os achados de hoje com
> os pendentes acumulados. Para cada um: título, lab, 2 linhas do que muda, e qual
> episódio da trilha base é pré-requisito. Termine perguntando se quero episódio hoje.
> Não gere nada antes da minha resposta.

**Rota B — cron + Claude Code headless.** Independe de app aberto:

```bash
0 8 * * * cd ~/podcast-ia && claude -p "rode a rotina diária conforme CLAUDE.md" >> log.txt
```

A confirmação diária aqui vira assíncrona: você lê o log e responde quando quiser.

---

## 9. Ordem de implementação

1. Estrutura de pastas + `CLAUDE.md` + `config/fontes.yaml`
2. `estado/trilha.md` e `estado/fila.md` vazios
3. `scripts/gerar_audio.py` (Opção A) — teste com um roteiro de 3 falas
4. Roteiro do episódio 01 completo → gere o áudio → **ouça e calibre tom/duração**
5. Só então `scripts/buscar_papers.py`
6. Só então o agendamento

Não pule o passo 4. Calibrar o roteiro depois de 15 episódios gerados é retrabalho.

---

## 10. Onde isso provavelmente vai doer

- **Scraping dos blogs dos labs quebra.** Eles mudam o HTML sem aviso. Trate falha de
  uma fonte como não-fatal: logue e siga com as outras.
- **Viés dos upvotes do HF.** O ranking favorece lançamentos de pesos abertos e demos
  rodáveis. Trabalho conceitual de interpretabilidade quase nunca sobe. Se a fila começar
  a parecer só "modelo novo lançado", é esse viés agindo — compense puxando manualmente
  do Transformer Circuits.
- **Dependência excessiva do HF.** Com o arXiv fora, os blogs dos labs viraram a única
  fonte de Anthropic e OpenAI. Se o scraping deles quebrar silenciosamente, você perde
  metade da cobertura sem perceber. Monitore: fonte que não retorna nada há 7 dias
  provavelmente está quebrada, não parada.
- **Drift de tom entre episódios.** Mitigue mandando o Claude Code ler os 2 roteiros
  anteriores antes de escrever um novo.
- **Duração.** 12 minutos de áudio ≈ 1.800 palavras faladas. Roteiro muito mais curto
  que isso vira episódio de 4 minutos.
