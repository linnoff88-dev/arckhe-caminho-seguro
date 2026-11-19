#!/usr/bin/env python3
"""caminho.py — monta o SEU plano do caminho seguro (kit grátis INEMA).

Responde perguntas simples (ou recebe por opções) e grava um plano em Markdown, com
quantidades para 72 horas e para 14 dias, os 5 passos e os checklists dos riscos da sua região.

Uso:
  python3 caminho.py                       # perguntas no terminal
  python3 caminho.py --pessoas 4 --criancas 1 --riscos enchente,apagao --saida meu-plano.md
  python3 caminho.py --pessoas 2 --moradia apartamento --fogao inducao
  python3 caminho.py --listar-riscos

Nada sai do seu computador: o script não usa internet.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

AGUA_L_PESSOA_DIA = 2.0      # Defesa Civil: 2 litros por pessoa por dia, só para beber
KCAL_PESSOA_DIA = 2000       # referência de adulto
DIAS_MINIMO = 3              # kit de 72 horas (Defesa Civil / União Europeia)
DIAS_META = 14               # meta do caminho seguro
REVISAR_MESES = 6

RISCOS = {
    "enchente": "Enchente, alagamento e deslizamento",
    "vendaval": "Vendaval, tornado, granizo e ciclone",
    "calor": "Calor extremo, seca e fogo",
    "apagao": "Apagão longo (luz, internet, celular)",
    "digital": "Ataque digital e golpe depois de vazamento",
    "conflito": "Conflito, violência e falta de abastecimento",
}

MORADIAS = {
    "casa": "Casa na cidade",
    "sitio": "Casa com quintal grande, chácara ou sítio",
    "apartamento": "Apartamento",
}

FOGOES = {
    "botijao": "Fogão a gás de botijão",
    "encanado": "Fogão de gás encanado",
    "eletrico": "Fogão elétrico ou cooktop de indução",
    "lenha": "Fogão a lenha",
}
FOGAO_SINONIMOS = {"inducao": "eletrico", "indução": "eletrico", "elétrico": "eletrico", "gas": "botijao",
                   "gás": "botijao", "sítio": "sitio", "chacara": "sitio", "chácara": "sitio", "apto": "apartamento"}

# 72 h = comida pronta, sem fogo. 14 dias = comida seca + um jeito de cozinhar sem luz.
SEM_COZINHAR_72H = [
    "Primeiro a geladeira (segura o frio cerca de 4 h fechada), depois o freezer (cheio, cerca de 48 h), depois a despensa",
    "Lata pronta: atum, sardinha, salsicha, carne, feijão e grão-de-bico prontos, milho, ervilha",
    "Pão de forma, torrada, biscoito, pasta de amendoim, castanhas",
    "Frutas que duram fora da geladeira e frutas secas; leite de caixinha ou em pó; aveia com leite frio, granola, barra de cereal",
    "Abridor de lata manual e pratos descartáveis (poupa água de lavar)",
]

COZINHAR = {
    "botijao": [
        "Fósforo ou isqueiro no kit: o acendedor elétrico não funciona sem luz (teste hoje com o fogão fora da tomada)",
        "Anotar quando trocou o botijão e trocar antes de acabar (13 kg dura de 3 semanas a 2 meses para 4 pessoas)",
        "Botijão em pé, em lugar ventilado, longe de tomada e de calor",
    ],
    "encanado": [
        "Teste hoje: desligue o disjuntor do fogão e acenda uma boca com fósforo",
        "Fósforo ou isqueiro no kit; se o gás for cortado, siga o plano do fogão elétrico",
    ],
    "eletrico": [
        "Sem luz o fogão não cozinha: guarde comida pronta para mais dias, não só para 72 horas",
        "Fogareiro portátil a cartucho para ferver e esquentar, só ao ar livre ou na varanda aberta; um cartucho para cada 1 a 2 dias",
        "Detector de monóxido de carbono a pilha em casa",
    ],
    "lenha": [
        "Lenha seca, cortada e coberta, longe da parede da casa, com gravetos e papel para acender",
        "Limpar a chaminé uma vez por ano",
    ],
}

MORAR = {
    "casa": [
        "Fogão a lenha com chaminé pode ficar dentro de casa; fogareiro de tijolos ou improvisado, só ao ar livre, longe de mato seco e de criança",
        "Sem quintal: fogareiro a cartucho ao ar livre, com detector de monóxido em casa",
    ],
    "sitio": [
        "Fogão a lenha com chaminé é o melhor plano para semanas; sem ele, fogareiro de tijolos ao ar livre",
        "Lenha seca guardada debaixo de telhado; respeitar a proibição de queimada na seca, com balde de água do lado",
    ],
    "apartamento": [
        "Nada de lenha, carvão, churrasqueira ou fogueira no apartamento, na sacada ou na varanda; fogareiro a cartucho só na varanda aberta, se o prédio permitir",
        "Se o prédio fechar o gás (enchente, vazamento), vale o plano do fogão elétrico: comida pronta",
        "Botijão é proibido em muitos prédios: conferir a regra do seu antes de comprar; nunca botijão reserva dentro do apartamento",
        "Combinar com os vizinhos: quem tem gás que funciona esquenta água para quem não tem",
    ],
}

NUNCA_DENTRO = ("Nunca carvão, churrasqueira, braseiro ou gerador dentro de casa, na garagem fechada ou perto de janela "
                "(monóxido de carbono não tem cheiro e mata). Dor de cabeça e enjoo em várias pessoas ao mesmo tempo: "
                "saia para o ar livre e ligue 193.")

COMUNICAR = [
    "Bateria portátil (power bank) carregada: 10.000 mAh dá cerca de 1 a 2 cargas do celular; recarregar todo mês",
    "Carregador USB de carro (motor ligado, carro ao ar livre) e, para muitos dias, painel solar pequeno",
    "Rádio AM/FM a pilha ou manivela, pilhas extras e as frequências das rádios da cidade no papel",
    "Celular em economia de bateria, ligado em horários combinados; SMS passa quando a internet não passa",
    "Walkie-talkie homologado de uso livre para a família e os vizinhos (sem licença)",
    "Quem quiser ir além: Rádio do Cidadão (cadastro grátis na Anatel) ou radioamador (prova do COER, LABRE do estado)",
    "Nunca transmitir na frequência da polícia, bombeiros, SAMU ou aviação: é crime e atrapalha o socorro",
]

DESLOCAR = [
    "Tanque nunca abaixo da metade (carro elétrico: bateria acima da metade); sem luz a bomba do posto não funciona",
    "Kit do carro: água, comida leve, lanterna, carregador, mapa de papel ou offline, cobertor, primeiros socorros",
    "Duas rotas até o ponto de encontro e até um parente fora da cidade, uma sem ponte nem rua que alaga; saber ir a pé",
    "Reserva de combustível só em casa ou sítio, pouca, em galão com selo do Inmetro, fora de casa; nunca em apartamento",
    "Sem carro: bicicleta com pneu cheio e carona combinada com um vizinho; apartamento: sem luz o elevador para, combinar quem ajuda os idosos",
    "Sem nenhum aparelho: ponto de encontro com horário, bilhete na porta e um parente fora da cidade que todos avisam",
]

CHECK_RISCO = {
    "enchente": [
        "Saber se a sua rua ou bairro já alagou e qual é o caminho até um lugar alto",
        "Documentos, remédios e o kit num lugar ALTO da casa, em saco à prova d'água",
        "Cadastrar o celular no alerta da Defesa Civil (SMS 40199 com o seu CEP)",
        "Saber desligar a chave geral de luz e o registro do gás",
        "Nunca atravessar água correndo, a pé ou de carro",
    ],
    "vendaval": [
        "Escolher o cômodo mais protegido: no centro da casa, sem janela, andar mais baixo",
        "Ter calçado fechado, apito e capacete ou travesseiro perto desse cômodo",
        "Saber os sinais: céu esverdeado, granizo, ronco contínuo como de trem",
        "Recolher objetos soltos do quintal quando vier o alerta",
        "Depois: cuidado com fio caído e telhado solto",
    ],
    "calor": [
        "Água extra para os dias quentes e sais de reidratação no kit",
        "Saber quem da família tem mais risco: idoso, bebê, quem toma remédio contínuo",
        "Um cômodo mais fresco, com pano úmido e ventilação cruzada",
        "Plano de saída se houver fogo perto: duas rotas e um ponto de encontro",
        "Máscara para fumaça no kit",
    ],
    "apagao": [
        "Lanterna e rádio a pilha (ou a manivela) com pilhas extras",
        "Carregador portátil (power bank) sempre carregado",
        "Comida pronta para 3 dias, que não precisa de fogo nem de geladeira",
        "Fósforo ou isqueiro: o fogão a gás acende sem luz, o acendedor elétrico não",
        "Dinheiro vivo para alguns dias de compras",
        "Números importantes escritos no papel, não só no celular",
    ],
    "digital": [
        "Verificação em duas etapas: APLICATIVO autenticador no e-mail (não SMS), PIN no WhatsApp, token do app no banco",
        "Senha diferente em cada conta importante (um gerenciador de senhas ajuda)",
        "Desconfiar de mensagem com seu nome e CPF certos pedindo dado, senha ou Pix",
        "Conferir no Registrato do Banco Central contas e chaves Pix no seu nome",
        "Combinar uma palavra-senha da família para pedido de dinheiro por mensagem",
    ],
    "conflito": [
        "Comida e água para 14 dias, guardadas sem chamar atenção",
        "Rotas para casa de parentes e um ponto de encontro fora do bairro",
        "Documentos e cópias num envelope fácil de pegar",
        "Rede de vizinhos de confiança com um jeito de se avisar",
        "Seguir só avisos de órgãos oficiais; não espalhar boato",
    ],
}

PASSOS = [
    ("1. Casa: o kit de 72 horas, depois 14 dias",
     "passos/1-casa-72h.md"),
    ("1b. Comer e cozinhar sem luz", "passos/1b-cozinhar-sem-luz.md"),
    ("2. Não depender só do online", "passos/2-fora-do-online.md"),
    ("2b. Comunicar quando o sistema cai", "passos/2b-comunicar-sem-rede.md"),
    ("2c. Deslocamento: tanque e rotas", "passos/2c-deslocamento.md"),
    ("3. Proteção digital", "passos/3-digital.md"),
    ("4. Saúde e pessoas", "passos/4-saude-e-pessoas.md"),
    ("5. Trabalho: a migração para a IA", "passos/5-trabalho-ia.md"),
]


def quantidades(pessoas: int, dias: int) -> dict:
    """Água (L), garrafões de 5 L, calorias e uma sugestão de comida para `pessoas` × `dias`."""
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
        # alimento seco (arroz, feijão, macarrão, aveia) tem ~3.500 kcal por kg
        "kg_seco": round(kcal / 3500, 1),
    }


def br(n: float, casas: int = 0) -> str:
    """Número no jeito brasileiro: 24.000 e 6,9."""
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
    """Comer sem cozinhar nas 72 h; depois, como cozinhar sem luz conforme moradia e fogão."""
    if moradia == "apartamento" and fogao == "lenha":
        raise ValueError("fogão a lenha em apartamento não entra no plano: escolha botijao, encanado ou eletrico")
    L = ["## Comer e cozinhar sem luz", "",
         "**72 horas: ninguém cozinha.** A família come o que já está pronto.", ""]
    L += [f"- [ ] {c}" for c in SEM_COZINHAR_72H] + [""]
    L += ["**Mais de 3 dias: como cozinhar.** O estoque de arroz, macarrão e feijão precisa de fogo e de água "
          "extra para cozinhar (os 2 L por dia são só para beber).", ""]
    fogoes = [fogao] if fogao else list(COZINHAR)
    if moradia == "apartamento" and not fogao:
        fogoes = ["botijao", "encanado", "eletrico"]
    moradias = [moradia] if moradia else list(MORAR)
    for f in fogoes:
        L += [f"### {FOGOES[f]}", ""] + [f"- [ ] {c}" for c in COZINHAR[f]] + [""]
    for m in moradias:
        L += [f"### {MORADIAS[m]}", ""] + [f"- [ ] {c}" for c in MORAR[m]] + [""]
    L += ["- [ ] Truques: comida que cozinha rápido, feijão de lata, panela tampada, garrafa térmica e calor guardado "
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
    fogao = normaliza(fogao, FOGOES, "fogão")
    q3 = quantidades(pessoas, DIAS_MINIMO)
    q14 = quantidades(pessoas, DIAS_META)
    titulo = f"Plano do caminho seguro — {nome}" if nome else "Plano do caminho seguro"
    L = [f"# {titulo}", "",
         f"Feito em {hoje:%d/%m/%Y}. **Revisar em {rev:%d/%m/%Y}** (validade de comida, remédio e pilha).", "",
         f"Casa: {pessoas} pessoa(s)"
         + (f", {criancas} criança(s)" if criancas else "")
         + (f", {idosos} idoso(s)" if idosos else "")
         + (f", {pets} pet(s)" if pets else "") + "."
         + (f" {MORADIAS[moradia]}." if moradia else "")
         + (f" {FOGOES[fogao]}." if fogao else ""), "",
         "## Quanto guardar", "",
         "| | 72 horas (mínimo) | 14 dias (meta) |",
         "|---|---|---|",
         f"| Água para beber (2 L por pessoa por dia) | {q3['agua_l']:.0f} L ({q3['garrafoes_5l']} garrafões de 5 L) "
         f"| {q14['agua_l']:.0f} L ({q14['garrafoes_5l']} garrafões de 5 L) |",
         f"| Comida | ~{br(q3['kcal'])} kcal de comida pronta, sem cozinhar "
         + (f"| ~{br(q14['kcal'])} kcal, a maior parte comida pronta (o fogão elétrico não cozinha sem luz) |"
          if fogao == "eletrico" else
          f"| ~{br(q14['kcal'])} kcal (≈ {br(q14['kg_seco'], 1)} kg de alimento seco, que precisa de fogo) |"),
         "", "Água de higiene e de cozinhar é à parte. 72 h: lata pronta, biscoito, pão, castanhas, leite de caixinha "
         "(ninguém cozinha). 14 dias: o que a família já come e que dura (arroz, feijão, macarrão, aveia, enlatados), "
         "com um jeito de cozinhar sem luz. Gire: use e reponha.", ""]
    if criancas:
        L += ["- [ ] Fralda, leite/fórmula, remédio infantil e um brinquedo ou livro para cada criança"]
    if idosos:
        L += ["- [ ] Óculos reserva, aparelho auditivo/pilhas e a lista de remédios de cada idoso"]
    if pets:
        L += ["- [ ] Ração e água do pet para os mesmos 14 dias, guia, caixa de transporte e cartão de vacina"]
    if remedios or idosos:
        L += ["- [ ] Remédios de uso contínuo para 14 dias a mais e cópia da receita guardada no kit"]
    if criancas or idosos or pets or remedios:
        L += [""]
    L += secao_cozinhar(moradia, fogao)
    L += ["## Comunicar quando o sistema cai", ""] + [f"- [ ] {c}" for c in COMUNICAR] + [""]
    L += ["## Deslocamento", ""] + [f"- [ ] {c}" for c in DESLOCAR] + [""]
    L += ["## Os 5 passos", ""]
    for t, arq in PASSOS:
        L += [f"- [ ] **{t}** — ver `{arq}`"]
    L += [""]
    if riscos:
        L += ["## Os riscos da sua região", ""]
        for r in riscos:
            L += [f"### {RISCOS[r]}", ""] + [f"- [ ] {c}" for c in CHECK_RISCO[r]] + [""]
    L += ["## Folha da geladeira", "",
          "- Defesa Civil **199** · Bombeiros **193** · SAMU **192** · Polícia **190**",
          "- Ponto de encontro da família: ______________________",
          "- Quem busca as crianças: ______________________",
          "- Parente fora da cidade (contato de todos): ______________________", "",
          "## Trabalho", "",
          "- [ ] Descobrir o meu nível de IA (certificado grátis): https://inematds.github.io/nivel-ia/guia/#certificado",
          "- [ ] Escolher a próxima tarefa do meu trabalho para a IA fazer comigo",
          "- [ ] Aprender de graça no https://inema.club", "",
          "_Kit caminho-seguro (INEMA, grátis). Não substitui a orientação da Defesa Civil da sua cidade._", ""]
    return "\n".join(L)


def perguntar(msg: str, padrao: str = "") -> str:
    r = input(f"{msg}{f' [{padrao}]' if padrao else ''}: ").strip()
    return r or padrao


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monta o seu plano do caminho seguro (grátis, sem internet).")
    ap.add_argument("--nome", default=None, help="nome da família (aparece no título)")
    ap.add_argument("--pessoas", type=int)
    ap.add_argument("--criancas", type=int, default=0)
    ap.add_argument("--idosos", type=int, default=0)
    ap.add_argument("--pets", type=int, default=0)
    ap.add_argument("--remedios", action="store_true", help="alguém toma remédio de uso contínuo")
    ap.add_argument("--riscos", default=None, help="lista: " + ",".join(RISCOS))
    ap.add_argument("--moradia", default=None, help="onde mora: " + ",".join(MORADIAS))
    ap.add_argument("--fogao", default=None, help="fogão: " + ",".join(FOGOES) + " (inducao = eletrico)")
    ap.add_argument("--saida", default="meu-plano.md")
    ap.add_argument("--listar-riscos", action="store_true")
    a = ap.parse_args(argv)

    if a.listar_riscos:
        for k, v in RISCOS.items():
            print(f"{k:10} {v}")
        return 0
    try:
        if a.pessoas is None:  # modo perguntas
            print("Caminho seguro — o seu plano (Enter aceita o padrão)\n")
            a.nome = perguntar("Nome da família", a.nome or "")
            a.pessoas = int(perguntar("Quantas pessoas moram na casa", "2"))
            a.criancas = int(perguntar("Quantas são crianças", "0"))
            a.idosos = int(perguntar("Quantas são idosas", "0"))
            a.pets = int(perguntar("Quantos pets", "0"))
            a.remedios = perguntar("Alguém toma remédio de uso contínuo? (s/n)", "n").lower().startswith("s")
            print("Riscos: " + ", ".join(RISCOS))
            a.riscos = perguntar("Quais riscos tem na sua região (separe por vírgula)", "apagao,digital")
            a.moradia = perguntar("Onde mora (" + ", ".join(MORADIAS) + ")", "casa")
            a.fogao = perguntar("Qual é o seu fogão (" + ", ".join(FOGOES) + ")", "botijao")
        riscos = parse_riscos(a.riscos or "apagao,digital")
        plano = montar_plano(a.nome or "", a.pessoas, a.criancas, a.idosos, a.pets, a.remedios, riscos,
                             moradia=a.moradia, fogao=a.fogao)
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nsaí sem gravar nada.", file=sys.stderr)
        return 1
    Path(a.saida).write_text(plano, encoding="utf-8")
    q = quantidades(a.pessoas, DIAS_MINIMO)
    print(f"ok: {a.saida} — 72 h: {q['agua_l']:.0f} L de água; revise em {REVISAR_MESES} meses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
