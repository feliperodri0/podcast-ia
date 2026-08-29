"""Busca candidatos a episódio nos labs prioritários + Hugging Face Daily Papers.

Não decide o que vira episódio — só coleta e imprime. A curadoria semântica
(adequação à trilha, descarte por falta de ideia conceitual, etc.) é feita
por quem lê o relatório (o Claude Code, seguindo CLAUDE.md), cruzando com
estado/trilha.md e estado/fila.md.

Falha de uma fonte é sempre não-fatal: loga e segue com as outras
(ver seção 10 do PODCAST-IA-SETUP.md — scraping de blog quebra sem aviso).
"""
import argparse
import difflib
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import requests
import yaml
from bs4 import BeautifulSoup

RAIZ = Path(__file__).resolve().parent.parent
CONFIG_PATH = RAIZ / "config" / "fontes.yaml"
TIMEOUT = 15
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; podcast-ia-bot/1.0)"}

@dataclass
class Candidato:
    fonte: str
    titulo: str
    url: str
    data: date | None
    resumo: str = ""
    tipo: str = "post"  # post | paper | note | repo
    extra: str = ""  # ex.: "132 upvotes"


def carregar_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def _get(url: str) -> requests.Response:
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r


# --- Anthropic Research (HTML; sem RSS disponível) -------------------------

def fetch_anthropic(janela_dias: int) -> list[Candidato]:
    html = _get("https://www.anthropic.com/research").text
    soup = BeautifulSoup(html, "html.parser")
    limite = date.today() - timedelta(days=janela_dias)
    candidatos = []
    vistos = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("/research/") or href.startswith("/research/team/"):
            continue
        if href in vistos:
            continue
        titulo_tag = a.find(["h1", "h2", "h3", "h4"])
        if not titulo_tag:
            # a lista "Publications" (tabela completa) usa <span class="...title...">
            # em vez de heading — sem esse fallback, ela é pulada em silêncio.
            titulo_tag = a.find(lambda tag: tag.name in ("span", "div", "p")
                                 and tag.get("class")
                                 and any("title" in c.lower() for c in tag.get("class")))
        if not titulo_tag:
            continue
        titulo = titulo_tag.get_text(strip=True)
        time_tag = a.find("time")
        data_pub = None
        if time_tag and time_tag.get_text(strip=True):
            try:
                data_pub = datetime.strptime(time_tag.get_text(strip=True), "%b %d, %Y").date()
            except ValueError:
                pass
        if data_pub and data_pub < limite:
            continue
        resumo_tag = a.find("p")
        resumo = resumo_tag.get_text(strip=True) if resumo_tag else ""
        vistos.add(href)
        candidatos.append(Candidato(
            fonte="Anthropic Research",
            titulo=titulo,
            url=f"https://www.anthropic.com{href}",
            data=data_pub,
            resumo=resumo,
        ))
    return candidatos


# --- Transformer Circuits (HTML estável, data-date explícito) --------------

def fetch_transformer_circuits(janela_dias: int) -> list[Candidato]:
    html = _get("https://transformer-circuits.pub/").text
    soup = BeautifulSoup(html, "html.parser")
    limite = date.today() - timedelta(days=janela_dias)
    candidatos = []

    for a in soup.select("a[data-date]"):
        data_str = a.get("data-date", "")
        try:
            data_pub = datetime.strptime(data_str, "%Y-%m-%d").date()
        except ValueError:
            data_pub = None
        if data_pub and data_pub < limite:
            continue
        titulo_tag = a.find("h3")
        if not titulo_tag:
            continue
        desc_tag = a.find("div", class_="description")
        href = a["href"]
        if href.startswith("http"):
            url = href
        else:
            url = f"https://transformer-circuits.pub/{href}"
        candidatos.append(Candidato(
            fonte="Transformer Circuits",
            titulo=titulo_tag.get_text(strip=True),
            url=url,
            data=data_pub,
            resumo=desc_tag.get_text(strip=True) if desc_tag else "",
            tipo="paper" if a.get("class") and "paper" in a.get("class") else "note",
        ))
    return candidatos


# --- Google DeepMind ---------------------------------------------------
# A própria página /research/publications/ é uma SPA renderizada via JS, mas o
# sitemap.xml geral do site lista cada publicação individual com lastmod, e
# essas páginas de publicação (diferente da listagem) SÃO estáticas. Puxamos
# as URLs do sitemap dentro da janela e visitamos cada uma pra extrair título,
# data e resumo. Quando a publicação linka o paper original (arXiv etc.), usa
# esse link como URL principal.

def fetch_deepmind(janela_dias: int) -> list[Candidato]:
    xml_bytes = _get("https://deepmind.google/sitemap.xml").content
    root = ET.fromstring(xml_bytes)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    limite = date.today() - timedelta(days=janela_dias)

    urls_na_janela = []
    for url_tag in root.findall("sm:url", ns):
        loc = url_tag.findtext("sm:loc", namespaces=ns) or ""
        if "/research/publications/" not in loc:
            continue
        lastmod = url_tag.findtext("sm:lastmod", namespaces=ns)
        try:
            data_pub = datetime.strptime(lastmod[:10], "%Y-%m-%d").date()
        except (TypeError, ValueError):
            continue
        if data_pub < limite:
            continue
        urls_na_janela.append((data_pub, loc))

    candidatos = []
    for data_pub, loc in urls_na_janela:
        try:
            pagina = BeautifulSoup(_get(loc).text, "html.parser")
        except requests.RequestException:
            continue
        titulo_tag = pagina.find("h1")
        if not titulo_tag:
            continue
        link_paper = pagina.find("a", attrs={"data-event-content-name": "View publication"})
        abstract_div = pagina.find("div", class_="publication-abstract")
        resumo_tag = abstract_div.find("p") if abstract_div else None
        candidatos.append(Candidato(
            fonte="Google DeepMind Research",
            titulo=titulo_tag.get_text(strip=True),
            url=link_paper["href"] if link_paper and link_paper.get("href") else loc,
            data=data_pub,
            resumo=resumo_tag.get_text(strip=True) if resumo_tag else "",
            tipo="paper",
        ))
    return candidatos


# --- OpenAI --------------------------------------------------------------
# /news/research/ é SPA e o RSS de /news/ não inclui a categoria "Research"
# (ela vive em /index/..., não em /news/...). O site expõe um sitemap dedicado
# só pra pesquisa, em /sitemap.xml/research/ — usamos o lastmod como proxy de
# data de publicação (não é exato, mas é o único sinal estático disponível).

def fetch_openai(janela_dias: int) -> list[Candidato]:
    xml_bytes = _get("https://openai.com/sitemap.xml/research/").content
    root = ET.fromstring(xml_bytes)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    limite = date.today() - timedelta(days=janela_dias)
    candidatos = []

    for url_tag in root.findall("sm:url", ns):
        loc = url_tag.findtext("sm:loc", namespaces=ns) or ""
        if "/index/" not in loc:
            continue
        lastmod = url_tag.findtext("sm:lastmod", namespaces=ns)
        data_pub = None
        if lastmod:
            try:
                data_pub = datetime.fromisoformat(lastmod.replace("Z", "+00:00")).date()
            except ValueError:
                pass
        if data_pub and data_pub < limite:
            continue
        slug = loc.rstrip("/").rsplit("/", 1)[-1]
        titulo = slug.replace("-", " ").capitalize()
        candidatos.append(Candidato(
            fonte="OpenAI",
            titulo=titulo,
            url=loc,
            data=data_pub,
            resumo="(título derivado da URL — página é renderizada via JS, sem título estático; confirme no link)",
        ))
    return candidatos


# --- DeepSeek AI (GitHub) --------------------------------------------------
# Não são "papers" no sentido estrito — são repositórios atualizados.
# Sinalizamos tipo="repo" pra quem for curar saber que se aplica o critério
# de descarte "apelo é a demo/pesos abertos, sem ideia nova por trás".

def fetch_deepseek(janela_dias: int) -> list[Candidato]:
    dados = _get("https://api.github.com/orgs/deepseek-ai/repos?sort=updated&per_page=20").json()
    limite = date.today() - timedelta(days=janela_dias)
    candidatos = []

    for repo in dados:
        pushed_at = repo.get("pushed_at")
        data_pub = None
        if pushed_at:
            data_pub = datetime.fromisoformat(pushed_at.replace("Z", "+00:00")).date()
        if data_pub and data_pub < limite:
            continue
        candidatos.append(Candidato(
            fonte="DeepSeek AI (GitHub)",
            titulo=repo["name"],
            url=repo["html_url"],
            data=data_pub,
            resumo=repo.get("description") or "",
            tipo="repo",
        ))
    return candidatos


# --- Hugging Face Daily Papers --------------------------------------------

def fetch_hf_daily(data_alvo: date, puxar_top: int) -> list[Candidato]:
    dados = _get(f"https://huggingface.co/api/daily_papers?date={data_alvo.isoformat()}").json()
    itens = []
    for entry in dados:
        p = entry["paper"]
        itens.append(Candidato(
            fonte="Hugging Face Daily Papers",
            titulo=p["title"],
            url=f"https://huggingface.co/papers/{p['id']}",
            data=data_alvo,
            resumo=p.get("summary", "")[:400],
            tipo="paper",
            extra=f"{p.get('upvotes', 0)} upvotes",
        ))
    itens.sort(key=lambda c: int(c.extra.split()[0]), reverse=True)
    return itens[:puxar_top]


# --- Deduplicação -----------------------------------------------------

def normalizar(titulo: str) -> str:
    return "".join(ch.lower() for ch in titulo if ch.isalnum() or ch.isspace()).strip()


def deduplicar(candidatos: list[Candidato]) -> list[Candidato]:
    """Mesmo trabalho no blog do lab e no HF → mantém só o blog (regra do fontes.yaml)."""
    labs = [c for c in candidatos if c.fonte != "Hugging Face Daily Papers"]
    hf = [c for c in candidatos if c.fonte == "Hugging Face Daily Papers"]
    labs_normalizados = [normalizar(c.titulo) for c in labs]

    hf_unicos = []
    for c in hf:
        titulo_norm = normalizar(c.titulo)
        duplicata = any(
            difflib.SequenceMatcher(None, titulo_norm, ln).ratio() > 0.6
            for ln in labs_normalizados
        )
        if not duplicata:
            hf_unicos.append(c)
    return labs + hf_unicos


# --- Execução --------------------------------------------------------

FONTES_LABS = {
    "Anthropic Research": fetch_anthropic,
    "Transformer Circuits": fetch_transformer_circuits,
    "Google DeepMind Research": fetch_deepmind,
    "OpenAI": fetch_openai,
    "DeepSeek AI (GitHub)": fetch_deepseek,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dias", type=int, default=10, help="janela em dias pros blogs dos labs (padrão: 10)")
    ap.add_argument("--hf-data", type=str, default=None, help="data alvo do HF Daily Papers, formato AAAA-MM-DD (padrão: ontem)")
    args = ap.parse_args()

    config = carregar_config()
    hf_data = datetime.strptime(args.hf_data, "%Y-%m-%d").date() if args.hf_data else date.today() - timedelta(days=1)
    puxar_top = config["prioridade_2_curadoria"]["puxar_top"]

    todos: list[Candidato] = []
    falhas: list[str] = []
    vazios: list[str] = []

    for nome, fn in FONTES_LABS.items():
        try:
            resultado = fn(args.dias)
            todos.extend(resultado)
            if not resultado:
                vazios.append(nome)
        except Exception as e:
            falhas.append(f"{nome}: {e}")
            print(f"[AVISO] falha ao buscar {nome}: {e}", file=sys.stderr)

    try:
        todos.extend(fetch_hf_daily(hf_data, puxar_top))
    except Exception as e:
        falhas.append(f"Hugging Face Daily Papers: {e}")
        print(f"[AVISO] falha ao buscar Hugging Face Daily Papers: {e}", file=sys.stderr)

    candidatos = deduplicar(todos)
    candidatos.sort(key=lambda c: c.data or date.min, reverse=True)

    print(f"# Candidatos encontrados — {date.today().isoformat()}\n")
    print(f"Janela dos labs: últimos {args.dias} dias. HF Daily Papers: {hf_data.isoformat()}.\n")

    por_fonte: dict[str, list[Candidato]] = {}
    for c in candidatos:
        por_fonte.setdefault(c.fonte, []).append(c)

    for fonte, itens in por_fonte.items():
        print(f"## {fonte} ({len(itens)})")
        for c in itens:
            data_str = c.data.isoformat() if c.data else "sem data"
            extra = f" | {c.extra}" if c.extra else ""
            print(f"- [{c.tipo}] {data_str}{extra} | {c.titulo}")
            print(f"  {c.url}")
            if c.resumo:
                print(f"  {c.resumo[:200]}{'...' if len(c.resumo) > 200 else ''}")
        print()

    if vazios:
        print(f"[ATENÇÃO] fontes sem nenhum resultado na janela: {', '.join(vazios)}.")
        print("Se isso persistir por vários dias seguidos, o scraping provavelmente quebrou "
              "(ver seção 10 do PODCAST-IA-SETUP.md) — não confundir com 'não publicaram nada'.\n")
    if falhas:
        print(f"[ATENÇÃO] fontes com erro de busca: {len(falhas)}. Ver avisos acima (stderr).\n")

    print(f"Total: {len(candidatos)} candidatos, de {len(por_fonte)} fontes.")
    print(f"Lembrete de config: max_candidatos_por_dia = {config['max_candidatos_por_dia']} "
          f"— aplicar isso na curadoria (adequação à trilha), não como corte cego aqui.")


if __name__ == "__main__":
    main()
