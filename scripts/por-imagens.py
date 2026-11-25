#!/usr/bin/env python3
"""Põe a imagem ilustrativa no topo de cada cartêo do guia (PT/EN/ES). Idempotente.

Mapa: seçêo do guia -> ids das imagens, na ordem dos cartões da 1ª grade da seçêo.
Só põe a imagem que existe em guia/assets/img/<id>.jpg.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MAPA = {
    "passos": ["p1-casa", "p2-online", "p3-digital", "p4-saude"],
    "cozinhar": ["c1-72h", "c2-truques", "c3-gas", "c4-lenha", "c5-apto", "c6-nunca"],
    "comunicar": ["m1-celular", "m2-radio", "m3-walkie", "m4-radioamador", "m5-tanque", "m6-rotas"],
}
CSS = ".cimg{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:10px;margin:0 0 14px;border:1px solid var(--line)}"
PAGINAS = {"guia/index.html": "assets/img/", "guia/en/index.html": "../assets/img/", "guia/es/index.html": "../assets/img/"}


def aplica(html: str, prefixo: str) -> tuple[str, int]:
    if ".cimg{" not in html:
        html = html.replace("</style>", "  " + CSS + "\n</style>", 1)
    n = 0
    for sec, ids in MAPA.items():
        m = re.search(rf'<section id="{sec}">.*?</div></section>', html, re.S)
        if not m:
            raise SystemExit(f"seçêo {sec} nêo achada")
        bloco = m.group(0)
        g = re.search(r'<div class="grid g2"[^>]*>', bloco)
        ini = g.end()
        cards = [c.start() for c in re.finditer(r'<div class="card">', bloco[ini:])][: len(ids)]
        novo = bloco
        for pos, idimg in sorted(zip(cards, ids), reverse=True):
            if not (RAIZ / "guia/assets/img" / f"{idimg}.jpg").is_file():
                continue
            a = ini + pos + len('<div class="card">')
            if novo[a:a + 15] == '<img class="cim':
                continue
            tag = f'<img class="cimg" src="{prefixo}{idimg}.jpg" alt="" loading="lazy" width="960" height="540">'
            novo = novo[:a] + tag + novo[a:]
            n += 1
        html = html.replace(bloco, novo, 1)
    return html, n


def main() -> int:
    for rel, pref in PAGINAS.items():
        p = RAIZ / rel
        html, n = aplica(p.read_text(encoding="utf-8"), pref)
        p.write_text(html, encoding="utf-8")
        print(f"{rel}: +{n} imagens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
