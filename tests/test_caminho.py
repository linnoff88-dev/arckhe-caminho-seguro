import datetime as dt
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
import caminho  # noqa: E402


def test_agua_defesa_civil_2l_por_pessoa_dia():
    q = caminho.quantidades(1, 3)
    assert q["agua_l"] == 6  # Defesa Civil: 6 L em 3 dias por pessoa


def test_quantidades_familia_14_dias():
    q = caminho.quantidades(4, 14)
    assert q["agua_l"] == 112
    assert q["garrafoes_5l"] == 23          # arredonda para cima
    assert q["kcal"] == 112000
    assert q["kg_seco"] == 32.0


@pytest.mark.parametrize("p,d", [(0, 3), (2, 0), (-1, 3)])
def test_quantidades_invalidas(p, d):
    with pytest.raises(ValueError):
        caminho.quantidades(p, d)


def test_parse_riscos_limpa_e_valida():
    assert caminho.parse_riscos(" Enchente, apagao;enchente ") == ["enchente", "apagao"]
    assert caminho.parse_riscos("") == []
    with pytest.raises(ValueError):
        caminho.parse_riscos("meteoro")


def test_plano_tem_72h_14d_e_revisao_em_6_meses():
    txt = caminho.montar_plano("Silva", 2, hoje=dt.date(2026, 11, 13))
    assert "# Plano do caminho seguro — Silva" in txt
    assert "| 12 L" in txt and "| 56 L" in txt
    assert "Revisar em 14/05/2027" in txt
    for t, _ in caminho.PASSOS:
        assert t in txt
    assert "199" in txt and "193" in txt and "192" in txt


def test_plano_itens_condicionais():
    sem = caminho.montar_plano("", 1)
    assert "Fralda" not in sem and "Ração" not in sem and "Óculos" not in sem
    com = caminho.montar_plano("", 3, criancas=1, idosos=1, pets=2, remedios=True)
    assert "Fralda" in com and "Óculos" in com and "Ração" in com and "uso contínuo para 14 dias" in com


def test_plano_checklists_dos_riscos():
    txt = caminho.montar_plano("", 2, riscos=["enchente", "digital"])
    assert caminho.RISCOS["enchente"] in txt and caminho.RISCOS["digital"] in txt
    assert caminho.RISCOS["vendaval"] not in txt
    assert "40199" in txt and "APLICATIVO" in txt


def test_numero_brasileiro_na_tabela():
    txt = caminho.montar_plano("", 4)
    assert "~24.000 kcal de comida pronta, sem cozinhar" in txt and "≈ 32,0 kg de alimento seco" in txt
    linha = next(l for l in txt.splitlines() if l.startswith("| Comida"))
    assert "6,9 kg" not in linha          # 72 h não vira quilo de comida seca: é comida pronta
    assert "pronta. sem" not in txt        # vírgula do texto não pode virar ponto


def test_72h_sem_cozinhar_e_14d_com_fogo():
    txt = caminho.montar_plano("", 2)
    assert "## Comer e cozinhar sem luz" in txt and "72 horas: ninguém cozinha" in txt
    assert "geladeira" in txt and "48 h" in txt
    # sem moradia/fogão, o plano mostra todas as opções
    for f in caminho.FOGOES.values():
        assert f"### {f}" in txt
    for m in caminho.MORADIAS.values():
        assert f"### {m}" in txt
    assert "monóxido de carbono" in txt and "193" in txt


def test_apartamento_inducao_so_o_que_serve():
    txt = caminho.montar_plano("", 2, moradia="apto", fogao="indução")
    assert "### Fogão elétrico ou cooktop de indução" in txt and "### Apartamento" in txt
    assert "### Fogão a lenha" not in txt and "### Casa com quintal" not in txt
    assert "Nada de lenha, carvão, churrasqueira" in txt and "proibido em muitos prédios" in txt
    linha = next(l for l in txt.splitlines() if l.startswith("| Comida"))
    assert "precisa de fogo" not in linha and "comida pronta (o fogão elétrico" in linha


def test_apartamento_sem_fogao_nao_oferece_lenha():
    txt = caminho.montar_plano("", 2, moradia="apartamento")
    assert "### Fogão a lenha" not in txt and "### Fogão de gás encanado" in txt


def test_sitio_lenha():
    txt = caminho.montar_plano("", 3, moradia="sitio", fogao="lenha")
    assert "### Fogão a lenha" in txt and "chaminé" in txt and "queimada" in txt
    assert "### Apartamento" not in txt


def test_moradia_ou_fogao_invalidos():
    with pytest.raises(ValueError):
        caminho.montar_plano("", 1, moradia="barco")
    with pytest.raises(ValueError):
        caminho.montar_plano("", 1, fogao="microondas")
    with pytest.raises(ValueError):
        caminho.montar_plano("", 1, moradia="apartamento", fogao="lenha")


def test_cli_moradia_fogao(tmp_path):
    saida = tmp_path / "a.md"
    r = subprocess.run([sys.executable, str(RAIZ / "caminho.py"), "--pessoas", "2", "--moradia", "apartamento",
                        "--fogao", "inducao", "--saida", str(saida)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "### Apartamento" in saida.read_text(encoding="utf-8")


def test_manuais_e_cozinhar_existem_e_sao_citados():
    assert (RAIZ / "MANUAIS.md").is_file()
    coz = (RAIZ / "passos/1b-cozinhar-sem-luz.md").read_text(encoding="utf-8")
    for termo in ("72 horas", "Apartamento", "lenha", "monóxido", "fósforo"):
        assert termo in coz, termo
    assert "1b-cozinhar-sem-luz.md" in (RAIZ / "passos/1-casa-72h.md").read_text(encoding="utf-8")
    for g in ("guia/index.html", "guia/en/index.html", "guia/es/index.html"):
        html = (RAIZ / g).read_text(encoding="utf-8")
        assert 'id="cozinhar"' in html and 'id="manuais"' in html, g


def test_todo_risco_tem_checklist_e_passos_existem():
    assert set(caminho.RISCOS) == set(caminho.CHECK_RISCO)
    for _, arq in caminho.PASSOS:
        assert (RAIZ / arq).is_file(), arq


def test_link_certificado_e_inema_club():
    txt = caminho.montar_plano("", 1)
    assert "nivel-ia/guia/#certificado" in txt and "https://inema.club" in txt


def test_cli_grava_arquivo(tmp_path):
    saida = tmp_path / "p.md"
    r = subprocess.run([sys.executable, str(RAIZ / "caminho.py"), "--pessoas", "3", "--riscos", "calor",
                        "--saida", str(saida)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("ok:") and "18 L" in r.stdout
    assert caminho.RISCOS["calor"] in saida.read_text(encoding="utf-8")


def test_cli_risco_errado_sai_2(tmp_path):
    r = subprocess.run([sys.executable, str(RAIZ / "caminho.py"), "--pessoas", "1", "--riscos", "zumbi",
                        "--saida", str(tmp_path / "x.md")], capture_output=True, text=True)
    assert r.returncode == 2 and "risco desconhecido" in r.stderr


def test_cli_listar_riscos():
    r = subprocess.run([sys.executable, str(RAIZ / "caminho.py"), "--listar-riscos"], capture_output=True, text=True)
    assert r.returncode == 0 and all(k in r.stdout for k in caminho.RISCOS)


def test_sem_internet_no_codigo():
    src = (RAIZ / "caminho.py").read_text(encoding="utf-8")
    for proibido in ("import urllib", "import requests", "import socket", "http.client"):
        assert proibido not in src


def test_biblioteca_offline_3_opcoes_separadas():
    off = RAIZ / "offline"
    for nome in ("README.md", "1-so-celular.md", "2-pc-simples.md", "3-pc-forte-nomad.md"):
        assert (off / nome).is_file(), nome
    idx = (off / "README.md").read_text(encoding="utf-8")
    for nome in ("1-so-celular.md", "2-pc-simples.md", "3-pc-forte-nomad.md"):
        assert nome in idx
    for g in ("guia/index.html", "guia/en/index.html", "guia/es/index.html"):
        html = (RAIZ / g).read_text(encoding="utf-8")
        assert 'id="biblioteca"' in html and "project-nomad/guia/" in html


def test_comunicar_e_deslocar_no_plano():
    txt = caminho.montar_plano("", 2)
    assert "## Comunicar quando o sistema cai" in txt and "## Deslocamento" in txt
    assert "AM/FM" in txt and "COER" in txt and "polícia" in txt
    assert "metade" in txt and "Inmetro" in txt
    for arq in ("passos/2b-comunicar-sem-rede.md", "passos/2c-deslocamento.md"):
        assert (RAIZ / arq).is_file()
    for g in ("guia/index.html", "guia/en/index.html", "guia/es/index.html"):
        assert 'id="comunicar"' in (RAIZ / g).read_text(encoding="utf-8"), g


def test_imagens_dos_cartoes_existem_nos_3_idiomas():
    import re
    for g in ("guia/index.html", "guia/en/index.html", "guia/es/index.html"):
        p = RAIZ / g
        srcs = re.findall(r'<img class="cimg" src="([^"]+)"', p.read_text(encoding="utf-8"))
        assert len(srcs) == 16, (g, len(srcs))
        for s in srcs:
            assert (p.parent / s).resolve().is_file(), (g, s)
