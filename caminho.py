#!/usr/bin/env python3
"""caminho.py ê¢â¬â monta o SEU plano do caminho seguro (kit grêÂ¡tis ARCKHê).

Responde perguntas simples (ou recebe por opêÂ§êÂµes) e grava um plano em Markdown, com
quantidades para 72 horas e para 14 dias, os 5 passos e os checklists dos riscos da sua regiêÂ£o.

Uso:
  python3 caminho.py                       # perguntas no terminal
  python3 caminho.py --pessoas 4 --criancas 1 --riscos enchente,apagao --saida meu-plano.md
  python3 caminho.py --pessoas 2 --moradia apartamento --fogao inducao
  python3 caminho.py --listar-riscos

Nada sai do seu computador: o script nêÂ£o usa internet.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

AGUA_L_PESSOA_DIA = 2.0      # Defesa Civil: 2 litros por pessoa por dia, sêÂ³ para beber
KCAL_PESSOA_DIA = 2000       # referêÂªncia de adulto
DIAS_MINIMO = 3              # kit de 72 horas (Defesa Civil / UniêÂ£o Europeia)
DIAS_META = 14               # meta do caminho seguro
REVISAR_MESES = 6

RISCOS = {
    "enchente": "Enchente, alagamento e deslizamento",
    "vendaval": "Vendaval, tornado, granizo e ciclone",
    "calor": "Calor extremo, seca e fogo",
    "apagao": "ApagêÂ£o longo (luz, internet, celular)",
    "digital": "Ataque digital e golpe depois de vazamento",
    "conflito": "Conflito, violêÂªncia e falta de abastecimento",
}

MORADIAS = {
    "casa": "Casa na cidade",
    "sitio": "Casa com quintal grande, chêÂ¡cara ou sêÂ­tio",
    "apartamento": "Apartamento",
}

FOGOES = {
    "botijao": "FogêÂ£o a gêÂ¡s de botijêÂ£o",
    "encanado": "FogêÂ£o de gêÂ¡s encanado",
    "eletrico": "FogêÂ£o elêÂ©trico ou cooktop de induêÂ§êÂ£o",
    "lenha": "FogêÂ£o a lenha",
}
FOGAO_SINONIMOS = {"inducao": "eletrico", "induêÂ§êÂ£o": "eletrico", "elêÂ©trico": "eletrico", "gas": "botijao",
                   "gêÂ¡s": "botijao", "sêÂ­tio": "sitio", "chacara": "sitio", "chêÂ¡cara": "sitio", "apto": "apartamento"}

# 72 h = comida pronta, sem fogo. 14 dias = comida seca + um jeito de cozinhar sem luz.
SEM_COZINHAR_72H = [
    "Primeiro a geladeira (segura o frio cerca de 4 h fechada), depois o freezer (cheio, cerca de 48 h), depois a despensa",
    "Lata pronta: atum, sardinha, salsicha, carne, feijêÂ£o e grêÂ£o-de-bico prontos, milho, ervilha",
    "PêÂ£o de forma, torrada, biscoito, pasta de amendoim, castanhas",
    "Frutas que duram fora da geladeira e frutas secas; leite de caixinha ou em pêÂ³; aveia com leite frio, granola, barra de cereal",
    "Abridor de lata manual e pratos descartêÂ¡veis (poupa êÂ¡gua de lavar)",
]

COZINHAR = {
    "botijao": [
        "FêÂ³sforo ou isqueiro no kit: o acendedor elêÂ©trico nêÂ£o funciona sem luz (teste hoje com o fogêÂ£o fora da tomada)",
        "Anotar quando trocou o botijêÂ£o e trocar antes de acabar (13 kg dura de 3 semanas a 2 meses para 4 pessoas)",
        "BotijêÂ£o em pêÂ©, em lugar ventilado, longe de tomada e de calor",
    ],
    "encanado": [
        "Teste hoje: desligue o disjuntor do fogêÂ£o e acenda uma boca com fêÂ³sforo",
        "FêÂ³sforo ou isqueiro no kit; se o gêÂ¡s for cortado, siga o plano do fogêÂ£o elêÂ©trico",
    ],
    "eletrico": [
        "Sem luz o fogêÂ£o nêÂ£o cozinha: guarde comida pronta para mais dias, nêÂ£o sêÂ³ para 72 horas",
        "Fogareiro portêÂ¡til a cartucho para ferver e esquentar, sêÂ³ ao ar livre ou na varanda aberta; um cartucho para cada 1 a 2 dias",
        "Detector de monêÂ³xido de carbono a pilha em casa",
    ],
    "lenha": [
        "Lenha seca, cortada e coberta, longe da parede da casa, com gravetos e papel para acender",
        "Limpar a chaminêÂ© uma vez por ano",
    ],
}

MORAR = {
    "casa": [
        "FogêÂ£o a lenha com chaminêÂ© pode ficar dentro de casa; fogareiro de tijolos ou improvisado, sêÂ³ ao ar livre, longe de mato seco e de crianêÂ§a",
        "Sem quintal: fogareiro a cartucho ao ar livre, com detector de monêÂ³xido em casa",
    ],
    "sitio": [
        "FogêÂ£o a lenha com chaminêÂ© êÂ© o melhor plano para semanas; sem ele, fogareiro de tijolos ao ar livre",
        "Lenha seca guardada debaixo de telhado; respeitar a proibiêÂ§êÂ£o de queimada na seca, com balde de êÂ¡gua do lado",
    ],
    "apartamento": [
        "Nada de lenha, carvêÂ£o, churrasqueira ou fogueira no apartamento, na sacada ou na varanda; fogareiro a cartucho sêÂ³ na varanda aberta, se o prêÂ©dio permitir",
        "Se o prêÂ©dio fechar o gêÂ¡s (enchente, vazamento), vale o plano do fogêÂ£o elêÂ©trico: comida pronta",
        "BotijêÂ£o êÂ© proibido em muitos prêÂ©dios: conferir a regra do seu antes de comprar; nunca botijêÂ£o reserva dentro do apartamento",
        "Combinar com os vizinhos: quem tem gêÂ¡s que funciona esquenta êÂ¡gua para quem nêÂ£o tem",
    ],
}

NUNCA_DENTRO = ("Nunca carvêÂ£o, churrasqueira, braseiro ou gerador dentro de casa, na garagem fechada ou perto de janela "
                "(monêÂ³xido de carbono nêÂ£o tem cheiro e mata). Dor de cabeêÂ§a e enjoo em vêÂ¡rias pessoas ao mesmo tempo: "
                "saia para o ar livre e ligue 193.")

COMUNICAR = [
    "Bateria portêÂ¡til (power bank) carregada: 10.000 mAh dêÂ¡ cerca de 1 a 2 cargas do celular; recarregar todo mêÂªs",
    "Carregador USB de carro (motor ligado, carro ao ar livre) e, para muitos dias, painel solar pequeno",
    "RêÂ¡dio AM/FM a pilha ou manivela, pilhas extras e as frequêÂªncias das rêÂ¡dios da cidade no papel",
    "Celular em economia de bateria, ligado em horêÂ¡rios combinados; SMS passa quando a internet nêÂ£o passa",
    "Walkie-talkie homologado de uso livre para a famêÂ­lia e os vizinhos (sem licenêÂ§a)",
    "Quem quiser ir alêÂ©m: RêÂ¡dio do CidadêÂ£o (cadastro grêÂ¡tis na Anatel) ou radioamador (prova do COER, LABRE do estado)",
    "Nunca transmitir na frequêÂªncia da polêÂ­cia, bombeiros, SAMU ou aviaêÂ§êÂ£o: êÂ© crime e atrapalha o socorro",
]

DESLOCAR = [
    "Tanque nunca abaixo da metade (carro elêÂ©trico: bateria acima da metade); sem luz a bomba do posto nêÂ£o funciona",
    "Kit do carro: êÂ¡gua, comida leve, lanterna, carregador, mapa de papel ou offline, cobertor, primeiros socorros",
    "Duas rotas atêÂ© o ponto de encontro e atêÂ© um parente fora da cidade, uma sem ponte nem rua que alaga; saber ir a pêÂ©",
    "Reserva de combustêÂ­vel sêÂ³ em casa ou sêÂ­tio, pouca, em galêÂ£o com selo do Inmetro, fora de casa; nunca em apartamento",
    "Sem carro: bicicleta com pneu cheio e carona combinada com um vizinho; apartamento: sem luz o elevador para, combinar quem ajuda os idosos",
    "Sem nenhum aparelho: ponto de encontro com horêÂ¡rio, bilhete na porta e um parente fora da cidade que todos avisam",
]

CHECK_RISCO = {
    "enchente": [
        "Saber se a sua rua ou bairro jêÂ¡ alagou e qual êÂ© o caminho atêÂ© um lugar alto",
        "Documentos, remêÂ©dios e o kit num lugar ALTO da casa, em saco êÂ  prova d'êÂ¡gua",
        "Cadastrar o celular no alerta da Defesa Civil (SMS 40199 com o seu CEP)",
        "Saber desligar a chave geral de luz e o registro do gêÂ¡s",
        "Nunca atravessar êÂ¡gua correndo, a pêÂ© ou de carro",
    ],
    "vendaval": [
        "Escolher o cêÂ´modo mais protegido: no centro da casa, sem janela, andar mais baixo",
        "Ter calêÂ§ado fechado, apito e capacete ou travesseiro perto desse cêÂ´modo",
        "Saber os sinais: cêÂ©u esverdeado, granizo, ronco contêÂ­nuo como de trem",
        "Recolher objetos soltos do quintal quando vier o alerta",
        "Depois: cuidado com fio caêÂ­do e telhado solto",
    ],
    "calor": [
        "êÂgua extra para os dias quentes e sais de reidrataêÂ§êÂ£o no kit",
        "Saber quem da famêÂ­lia tem mais risco: idoso, bebêÂª, quem toma remêÂ©dio contêÂ­nuo",
        "Um cêÂ´modo mais fresco, com pano êÂºmido e ventilaêÂ§êÂ£o cruzada",
        "Plano de saêÂ­da se houver fogo perto: duas rotas e um ponto de encontro",
        "MêÂ¡scara para fumaêÂ§a no kit",
    ],
    "apagao": [
        "Lanterna e rêÂ¡dio a pilha (ou a manivela) com pilhas extras",
        "Carregador portêÂ¡til (power bank) sempre carregado",
        "Comida pronta para 3 dias, que nêÂ£o precisa de fogo nem de geladeira",
        "FêÂ³sforo ou isqueiro: o fogêÂ£o a gêÂ¡s acende sem luz, o acendedor elêÂ©trico nêÂ£o",
        "Dinheiro vivo para alguns dias de compras",
        "NêÂºmeros importantes escritos no papel, nêÂ£o sêÂ³ no celular",
    ],
    "digital": [
        "VerificaêÂ§êÂ£o em duas etapas: APLICATIVO autenticador no e-mail (nêÂ£o SMS), PIN no WhatsApp, token do app no banco",
        "Senha diferente em cada conta importante (um gerenciador de senhas ajuda)",
        "Desconfiar de mensagem com seu nome e CPF certos pedindo dado, senha ou Pix",
        "Conferir no Registrato do Banco Central contas e chaves Pix no seu nome",
        "Combinar uma palavra-senha da famêÂ­lia para pedido de dinheiro por mensagem",
    ],
    "conflito": [
        "Comida e êÂ¡gua para 14 dias, guardadas sem chamar atenêÂ§êÂ£o",
        "Rotas para casa de parentes e um ponto de encontro fora do bairro",
        "Documentos e cêÂ³pias num envelope fêÂ¡cil de pegar",
        "Rede de vizinhos de confianêÂ§a com um jeito de se avisar",
        "Seguir sêÂ³ avisos de êÂ³rgêÂ£os oficiais; nêÂ£o espalhar boato",
    ],
}

PASSOS = [
    ("1. Casa: o kit de 72 horas, depois 14 dias",
     "passos/1-casa-72h.md"),
    ("1b. Comer e cozinhar sem luz", "passos/1b-cozinhar-sem-luz.md"),
    ("2. NêÂ£o depender sêÂ³ do online", "passos/2-fora-do-online.md"),
    ("2b. Comunicar quando o sistema cai", "passos/2b-comunicar-sem-rede.md"),
    ("2c. Deslocamento: tanque e rotas", "passos/2c-deslocamento.md"),
    ("3. ProteêÂ§êÂ£o digital", "passos/3-digital.md"),
    ("4. SaêÂºde e pessoas", "passos/4-saude-e-pessoas.md"),
    ("5. Trabalho: a migraêÂ§êÂ£o para a IA", "passos/5-trabalho-ia.md"),
]


def quantidades(pessoas: int, dias: int) -> dict:
    """êÂgua (L), garrafêÂµes de 5 L, calorias e uma sugestêÂ£o de comida para `pessoas` êâ `dias`."""
    if pessoas < 1:
        raise ValueError("pessoas precisa ser 1 ou mais")
    if dias < 1:
        raise ValueError("dias precisa ser 1 ou mais")
    agua = pessoas * dias * AGUA_L_PESSOA_DIA
    kcal = pessoas * dias * KCAL_PESSOA_DIA
    return {
        "pessoas": pessoas,
        "dias": dias,
        "agua_l": agua,
        "garrafoes_5l": -(-int(agua) // 5),          # arredonda para cima
        "kcal": kcal,
        # alimento seco (arroz, feijêÂ£o, macarrêÂ£o, aveia) tem ~3.500 kcal por kg
        "kg_seco": round(kcal / 3500, 1),
    }


def br(n: float, casas: int = 0) -> str:
    """NêÂºmero no jeito brasileiro: 24.000 e 6,9."""
    return f"{n:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def normaliza(valor: str | None, validos: dict, nome: str) -> str | None:
    if not valor:
        return None
    v = valor.strip().lower()
    v = FOGAO_SINONIMOS.get(v, v)
    if v not in validos:
        raise ValueError(f"{nome} desconhecido: {valor} (use: {', '.join(validos)})")
    return v


def secao_cozinhar(moradia: str | None, fogao: str | None) -> list[str]:
    """Comer sem cozinhar nas 72 h; depois, como cozinhar sem luz conforme moradia e fogêÂ£o."""
    if moradia == "apartamento" and fogao == "lenha":
        raise ValueError("fogêÂ£o a lenha em apartamento nêÂ£o entra no plano: escolha botijao, encanado ou eletrico")
    L = ["## Comer e cozinhar sem luz", "",
         "**72 horas: ninguêÂ©m cozinha.** A famêÂ­lia come o que jêÂ¡ estêÂ¡ pronto.", ""]
    L += [f"- [ ] {c}" for c in SEM_COZINHAR_72H] + [""]
    L += ["**Mais de 3 dias: como cozinhar.** O estoque de arroz, macarrêÂ£o e feijêÂ£o precisa de fogo e de êÂ¡gua "
          "extra para cozinhar (os 2 L por dia sêÂ£o sêÂ³ para beber).", ""]
    fogoes = [fogao] if fogao else list(COZINHAR)
    if moradia == "apartamento" and not fogao:
        fogoes = ["botijao", "encanado", "eletrico"]
    moradias = [moradia] if moradia else list(MORAR)
    for f in fogoes:
        L += [f"### {FOGOES[f]}", ""] + [f"- [ ] {c}" for c in COZINHAR[f]] + [""]
    for m in moradias:
        L += [f"### {MORADIAS[m]}", ""] + [f"- [ ] {c}" for c in MORAR[m]] + [""]
    L += ["- [ ] Truques: comida que cozinha rêÂ¡pido, feijêÂ£o de lata, panela tampada, garrafa têÂ©rmica e calor guardado "
          "(ferve, desliga, enrola a panela no cobertor)", "",
          f"> {NUNCA_DENTRO}", "",
          "Detalhe em `passos/1b-cozinhar-sem-luz.md`. Manuais oficiais prontos: `MANUAIS.md`.", ""]
    return L


def parse_riscos(texto: str) -> list[str]:
    if not texto:
        return []
    saida = []
    for r in texto.replace(";", ",").split(","):
        r = r.strip().lower()
        if not r:
            continue
        if r not in RISCOS:
            raise ValueError(f"risco desconhecido: {r} (use: {', '.join(RISCOS)})")
        if r not in saida:
            saida.append(r)
    return saida


def montar_plano(nome: str, pessoas: int, criancas: int = 0, idosos: int = 0, pets: int = 0,
                 remedios: bool = False, riscos: list[str] | None = None,
                 hoje: dt.date | None = None, moradia: str | None = None, fogao: str | None = None) -> str:
    riscos = riscos or []
    hoje = hoje or dt.date.today()
    rev = hoje + dt.timedelta(days=round(REVISAR_MESES * 30.4))
    moradia = normaliza(moradia, MORADIAS, "moradia")
    fogao = normaliza(fogao, FOGOES, "fogêÂ£o")
    q3 = quantidades(pessoas, DIAS_MINIMO)
    q14 = quantidades(pessoas, DIAS_META)
    titulo = f"Plano do caminho seguro ê¢â¬â {nome}" if nome else "Plano do caminho seguro"
    L = [f"# {titulo}", "",
         f"Feito em {hoje:%d/%m/%Y}. **Revisar em {rev:%d/%m/%Y}** (validade de comida, remêÂ©dio e pilha).", "",
         f"Casa: {pessoas} pessoa(s)"
         + (f", {criancas} crianêÂ§a(s)" if criancas else "")
         + (f", {idosos} idoso(s)" if idosos else "")
         + (f", {pets} pet(s)" if pets else "") + "."
         + (f" {MORADIAS[moradia]}." if moradia else "")
         + (f" {FOGOES[fogao]}." if fogao else ""), "",
         "## Quanto guardar", "",
         "| | 72 horas (mêÂ­nimo) | 14 dias (meta) |",
         "|---|---|---|",
         f"| êÂgua para beber (2 L por pessoa por dia) | {q3['agua_l']:.0f} L ({q3['garrafoes_5l']} garrafêÂµes de 5 L) "
         f"| {q14['agua_l']:.0f} L ({q14['garrafoes_5l']} garrafêÂµes de 5 L) |",
         f"| Comida | ~{br(q3['kcal'])} kcal de comida pronta, sem cozinhar "
         + (f"| ~{br(q14['kcal'])} kcal, a maior parte comida pronta (o fogêÂ£o elêÂ©trico nêÂ£o cozinha sem luz) |"
          if fogao == "eletrico" else
          f"| ~{br(q14['kcal'])} kcal (ê¢â°Ë {br(q14['kg_seco'], 1)} kg de alimento seco, que precisa de fogo) |"),
         "", "êÂgua de higiene e de cozinhar êÂ© êÂ  parte. 72 h: lata pronta, biscoito, pêÂ£o, castanhas, leite de caixinha "
         "(ninguêÂ©m cozinha). 14 dias: o que a famêÂ­lia jêÂ¡ come e que dura (arroz, feijêÂ£o, macarrêÂ£o, aveia, enlatados), "
         "com um jeito de cozinhar sem luz. Gire: use e reponha.", ""]
    if criancas:
        L += ["- [ ] Fralda, leite/fêÂ³rmula, remêÂ©dio infantil e um brinquedo ou livro para cada crianêÂ§a"]
    if idosos:
        L += ["- [ ] êâculos reserva, aparelho auditivo/pilhas e a lista de remêÂ©dios de cada idoso"]
    if pets:
        L += ["- [ ] RaêÂ§êÂ£o e êÂ¡gua do pet para os mesmos 14 dias, guia, caixa de transporte e cartêÂ£o de vacina"]
    if remedios or idosos:
        L += ["- [ ] RemêÂ©dios de uso contêÂ­nuo para 14 dias a mais e cêÂ³pia da receita guardada no kit"]
    if criancas or idosos or pets or remedios:
        L += [""]
    L += secao_cozinhar(moradia, fogao)
    L += ["## Comunicar quando o sistema cai", ""] + [f"- [ ] {c}" for c in COMUNICAR] + [""]
    L += ["## Deslocamento", ""] + [f"- [ ] {c}" for c in DESLOCAR] + [""]
    L += ["## Os 5 passos", ""]
    for t, arq in PASSOS:
        L += [f"- [ ] **{t}** ê¢â¬â ver `{arq}`"]
    L += [""]
    if riscos:
        L += ["## Os riscos da sua regiêÂ£o", ""]
        for r in riscos:
            L += [f"### {RISCOS[r]}", ""] + [f"- [ ] {c}" for c in CHECK_RISCO[r]] + [""]
    L += ["## Folha da geladeira", "",
          "- Defesa Civil **199** êÂ· Bombeiros **193** êÂ· SAMU **192** êÂ· PolêÂ­cia **190**",
          "- Ponto de encontro da famêÂ­lia: ______________________",
          "- Quem busca as crianêÂ§as: ______________________",
          "- Parente fora da cidade (contato de todos): ______________________", "",
          "## Trabalho", "",
          "- [ ] Descobrir o meu nêÂ­vel de IA (certificado grêÂ¡tis): https://linnoff88-dev.github.io/
          "- [ ] Escolher a prêÂ³xima tarefa do meu trabalho para a IA fazer comigo",
          "- [ ] Aprender de graêÂ§a no https://ARCKHê AI", "",
          "_Kit caminho-seguro (ARCKHê, grêÂ¡tis). NêÂ£o substitui a orientaêÂ§êÂ£o da Defesa Civil da sua cidade._", ""]
    return "\n".join(L)


def perguntar(msg: str, padrao: str = "") -> str:
    r = input(f"{msg}{f' [{padrao}]' if padrao else ''}: ").strip()
    return r or padrao


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monta o seu plano do caminho seguro (grêÂ¡tis, sem internet).")
    ap.add_argument("--nome", default=None, help="nome da famêÂ­lia (aparece no têÂ­tulo)")
    ap.add_argument("--pessoas", type=int)
    ap.add_argument("--criancas", type=int, default=0)
    ap.add_argument("--idosos", type=int, default=0)
    ap.add_argument("--pets", type=int, default=0)
    ap.add_argument("--remedios", action="store_true", help="alguêÂ©m toma remêÂ©dio de uso contêÂ­nuo")
    ap.add_argument("--riscos", default=None, help="lista: " + ",".join(RISCOS))
    ap.add_argument("--moradia", default=None, help="onde mora: " + ",".join(MORADIAS))
    ap.add_argument("--fogao", default=None, help="fogêÂ£o: " + ",".join(FOGOES) + " (inducao = eletrico)")
    ap.add_argument("--saida", default="meu-plano.md")
    ap.add_argument("--listar-riscos", action="store_true")
    a = ap.parse_args(argv)

    if a.listar_riscos:
        for k, v in RISCOS.items():
            print(f"{k:10} {v}")
        return 0
    try:
        if a.pessoas is None:  # modo perguntas
            print("Caminho seguro ê¢â¬â o seu plano (Enter aceita o padrêÂ£o)\n")
            a.nome = perguntar("Nome da famêÂ­lia", a.nome or "")
            a.pessoas = int(perguntar("Quantas pessoas moram na casa", "2"))
            a.criancas = int(perguntar("Quantas sêÂ£o crianêÂ§as", "0"))
            a.idosos = int(perguntar("Quantas sêÂ£o idosas", "0"))
            a.pets = int(perguntar("Quantos pets", "0"))
            a.remedios = perguntar("AlguêÂ©m toma remêÂ©dio de uso contêÂ­nuo? (s/n)", "n").lower().startswith("s")
            print("Riscos: " + ", ".join(RISCOS))
            a.riscos = perguntar("Quais riscos tem na sua regiêÂ£o (separe por vêÂ­rgula)", "apagao,digital")
            a.moradia = perguntar("Onde mora (" + ", ".join(MORADIAS) + ")", "casa")
            a.fogao = perguntar("Qual êÂ© o seu fogêÂ£o (" + ", ".join(FOGOES) + ")", "botijao")
        riscos = parse_riscos(a.riscos or "apagao,digital")
        plano = montar_plano(a.nome or "", a.pessoas, a.criancas, a.idosos, a.pets, a.remedios, riscos,
                             moradia=a.moradia, fogao=a.fogao)
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nsaêÂ­ sem gravar nada.", file=sys.stderr)
        return 1
    Path(a.saida).write_text(plano, encoding="utf-8")
    q = quantidades(a.pessoas, DIAS_MINIMO)
    print(f"ok: {a.saida} ê¢â¬â 72 h: {q['agua_l']:.0f} L de êÂ¡gua; revise em {REVISAR_MESES} meses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
