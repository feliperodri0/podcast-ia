"""Gera áudio do roteiro usando edge-tts. Custo zero, roda local."""
import asyncio, re, sys, subprocess
from pathlib import Path
import edge_tts

VOZES = {
    "ANA": "pt-BR-FranciscaNeural",
    "BIA": "pt-BR-ThalitaMultilingualNeural",
}

def parse_roteiro(path: Path) -> list[tuple[str, str]]:
    texto = path.read_text(encoding="utf-8")
    if texto.startswith("---"):
        texto = texto.split("---", 2)[2]  # descarta o frontmatter
    partes = re.split(r"\[(ANA|BIA)\]", texto)
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
