#!/usr/bin/env python3
"""caminho.py â€” monta o SEU plano do caminho seguro (kit grÃ¡tis ARCKHÉ).

Responde perguntas simples (ou recebe por opÃ§Ãµes) e grava um plano em Markdown, com
quantidades para 72 horas e para 14 dias, os 5 passos e os checklists dos riscos da sua regiÃ£o.

Uso:
  python3 caminho.py                       # perguntas no terminal
  python3 caminho.py --pessoas 4 --criancas 1 --riscos enchente,apagao --saida meu-plano.md
  python3 caminho.py --pessoas 2 --moradia apartamento --fogao inducao
  python3 caminho.py --listar-riscos

Nada sai do seu computador: o script nÃ£o usa internet.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

AGUA_L_PESSOA_DIA = 2.0      # Defesa Civil: 2 litros por pessoa por dia, sÃ³ para beber
KCAL_PESSOA_DIA = 2000       # referÃªncia de adulto
DIAS_MINIMO = 3              # kit de 72 horas (Defesa Civil / UniÃ£o Europeia)
DIAS_META = 14               # meta do caminho seguro
REVISAR_MESES = 6

RISCOS = {
    "enchente": "Enchente, alagamento e deslizamento",
    "vendaval": "Vendaval, tornado, granizo e ciclone",
    "calor": "Calor extremo, seca e fogo",
    "apagao": "ApagÃ£o longo (luz, internet, celular)",
    "digital": "Ataque digital e golpe depois de vazamento",
    "conflito": "Conflito, violÃªncia e falta de abastecimento",
}

MORADIAS = {
    "casa": "Casa na cidade",
    "sitio": "Casa com quintal grande, chÃ¡cara ou sÃ­tio",
    "apartamento": "Apartamento",
}

FOGOES = {
    "botijao": "FogÃ£o a gÃ¡s de botijÃ£o",
    "encanado": "FogÃ£o de gÃ¡s encanado",
    "eletrico": "FogÃ£o elÃ©trico ou cooktop de induÃ§Ã£o",
    "lenha": "FogÃ£o a lenha",
}
FOGAO_SINONIMOS = {"inducao": "eletrico", "induÃ§Ã£o": "eletrico", "elÃ©trico": "eletrico", "gas": "botijao",
                   "gÃ¡s": "botijao", "sÃ­tio": "sitio", "chacara": "sitio", "chÃ¡cara": "sitio", "apto": "apartamento"}

# 72 h = comida pronta, sem fogo. 14 dias = comida seca + um jeito de cozinhar sem luz.
SEM_COZINHAR_72H = [
    "Primeiro a geladeira (segura o frio cerca de 4 h fechada), depois o freezer (cheio, cerca de 48 h), depois a despensa",
    "Lata pronta: atum, sardinha, salsicha, carne, feijÃ£o e grÃ£o-de-bico prontos, milho, ervilha",
    "PÃ£o de forma, torrada, biscoito, pasta de amendoim, castanhas",
    "Frutas que duram fora da geladeira e frutas secas; leite de caixinha ou em pÃ³; aveia com leite frio, granola, barra de cereal",
    "Abridor de lata manual e pratos descartÃ¡veis (poupa Ã¡gua de lavar)",
]

COZINHAR = {
    "botijao": [
        "FÃ³sforo ou isqueiro no kit: o acendedor elÃ©trico nÃ£o funciona sem luz (teste hoje com o fogÃ£o fora da tomada)",
        "Anotar quando trocou o botijÃ£o e trocar antes de acabar (13 kg dura de 3 semanas a 2 meses para 4 pessoas)",
        "BotijÃ£o em pÃ©, em lugar ventilado, longe de tomada e de calor",
    ],
    "encanado": [
        "Teste hoje: desligue o disjuntor do fogÃ£o e acenda uma boca com fÃ³sforo",
        "FÃ³sforo ou isqueiro no kit; se o gÃ¡s for cortado, siga o plano do fogÃ£o elÃ©trico",
    ],
    "eletrico": [
        "Sem luz o fogÃ£o nÃ£o cozinha: guarde comida pronta para mais dias, nÃ£o sÃ³ para 72 horas",
        "Fogareiro portÃ¡til a cartucho para ferver e esquentar, sÃ³ ao ar livre ou na varanda aberta; um cartucho para cada 1 a 2 dias",
        "Detector de monÃ³xido de carbono a pilha em casa",
    ],
    "lenha": [
        "Lenha seca, cortada e coberta, longe da parede da casa, com gravetos e papel para acender",
        "Limpar a chaminÃ© uma vez por ano",
    ],
}

MORAR = {
    "casa": [
        "FogÃ£o a lenha com chaminÃ© pode ficar dentro de casa; fogareiro de tijolos ou improvisado, sÃ³ ao ar livre, longe de mato seco e de crianÃ§a",
        "Sem quintal: fogareiro a cartucho ao ar livre, com detector de monÃ³xido em casa",
    ],
    "sitio": [
        "FogÃ£o a lenha com chaminÃ© Ã© o melhor plano para semanas; sem ele, fogareiro de tijolos ao ar livre",
        "Lenha seca guardada debaixo de telhado; respeitar a proibiÃ§Ã£o de queimada na seca, com balde de Ã¡gua do lado",
    ],
    "apartamento": [
        "Nada de lenha, carvÃ£o, churrasqueira ou fogueira no apartamento, na sacada ou na varanda; fogareiro a cartucho sÃ³ na varanda aberta, se o prÃ©dio permitir",
        "Se o prÃ©dio fechar o gÃ¡s (enchente, vazamento), vale o plano do fogÃ£o elÃ©trico: comida pronta",
        "BotijÃ£o Ã© proibido em muitos prÃ©dios: conferir a regra do seu antes de comprar; nunca botijÃ£o reserva dentro do apartamento",
        "Combinar com os vizinhos: quem tem gÃ¡s que funciona esquenta Ã¡gua para quem nÃ£o tem",
    ],
}

NUNCA_DENTRO = ("Nunca carvÃ£o, churrasqueira, braseiro ou gerador dentro de casa, na garagem fechada ou perto de janela "
                "(monÃ³xido de carbono nÃ£o tem cheiro e mata). Dor de cabeÃ§a e enjoo em vÃ¡rias pessoas ao mesmo tempo: "
                "saia para o ar livre e ligue 193.")

COMUNICAR = [
    "Bateria portÃ¡til (power bank) carregada: 10.000 mAh dÃ¡ cerca de 1 a 2 cargas do celular; recarregar todo mÃªs",
    "Carregador USB de carro (motor ligado, carro ao ar livre) e, para muitos dias, painel solar pequeno",
    "RÃ¡dio AM/FM a pilha ou manivela, pilhas extras e as frequÃªncias das rÃ¡dios da cidade no papel",
    "Celular em economia de bateria, ligado em horÃ¡rios combinados; SMS passa quando a internet nÃ£o passa",
    "Walkie-talkie homologado de uso livre para a famÃ­lia e os vizinhos (sem licenÃ§a)",
    "Quem quiser ir alÃ©m: RÃ¡dio do CidadÃ£o (cadastro grÃ¡tis na Anatel) ou radioamador (prova do COER, LABRE do estado)",
    "Nunca transmitir na frequÃªncia da polÃ­cia, bombeiros, SAMU ou aviaÃ§Ã£o: Ã© crime e atrapalha o socorro",
]

DESLOCAR = [
    "Tanque nunca abaixo da metade (carro elÃ©trico: bateria acima da metade); sem luz a bomba do posto nÃ£o funciona",
    "Kit do carro: Ã¡gua, comida leve, lanterna, carregador, mapa de papel ou offline, cobertor, primeiros socorros",
    "Duas rotas atÃ© o ponto de encontro e atÃ© um parente fora da cidade, uma sem ponte nem rua que alaga; saber ir a pÃ©",
    "Reserva de combustÃ­vel sÃ³ em casa ou sÃ­tio, pouca, em galÃ£o com selo do Inmetro, fora de casa; nunca em apartamento",
    "Sem carro: bicicleta com pneu cheio e carona combinada com um vizinho; apartamento: sem luz o elevador para, combinar quem ajuda os idosos",
    "Sem nenhum aparelho: ponto de encontro com horÃ¡rio, bilhete na porta e um parente fora da cidade que todos avisam",
]

CHECK_RISCO = {
    "enchente": [
        "Saber se a sua rua ou bairro jÃ¡ alagou e qual Ã© o caminho atÃ© um lugar alto",
        "Documentos, remÃ©dios e o kit num lugar ALTO da casa, em saco Ã  prova d'Ã¡gua",
        "Cadastrar o celular no alerta da Defesa Civil (SMS 40199 com o seu CEP)",
        "Saber desligar a chave geral de luz e o registro do gÃ¡s",
        "Nunca atravessar Ã¡gua correndo, a pÃ© ou de carro",
    ],
    "vendaval": [
        "Escolher o cÃ´modo mais protegido: no centro da casa, sem janela, andar mais baixo",
        "Ter calÃ§ado fechado, apito e capacete ou travesseiro perto desse cÃ´modo",
        "Saber os sinais: cÃ©u esverdeado, granizo, ronco contÃ­nuo como de trem",
        "Recolher objetos soltos do quintal quando vier o alerta",
        "Depois: cuidado com fio caÃ­do e telhado solto",
    ],
    "calor": [
        "Ãgua extra para os dias quentes e sais de reidrataÃ§Ã£o no kit",
        "Saber quem da famÃ­lia tem mais risco: idoso, bebÃª, quem toma remÃ©dio contÃ­nuo",
        "Um cÃ´modo mais fresco, com pano Ãºmido e ventilaÃ§Ã£o cruzada",
        "Plano de saÃ­da se houver fogo perto: duas rotas e um ponto de encontro",
        "MÃ¡scara para fumaÃ§a no kit",
    ],
    "apagao": [
        "Lanterna e rÃ¡dio a pilha (ou a manivela) com pilhas extras",
        "Carregador portÃ¡til (power bank) sempre carregado",
        "Comida pronta para 3 dias, que nÃ£o precisa de fogo nem de geladeira",
        "FÃ³sforo ou isqueiro: o fogÃ£o a gÃ¡s acende sem luz, o acendedor elÃ©trico nÃ£o",
        "Dinheiro vivo para alguns dias de compras",
        "NÃºmeros importantes escritos no papel, nÃ£o sÃ³ no celular",
    ],
    "digital": [
        "VerificaÃ§Ã£o em duas etapas: APLICATIVO autenticador no e-mail (nÃ£o SMS), PIN no WhatsApp, token do app no banco",
        "Senha diferente em cada conta importante (um gerenciador de senhas ajuda)",
        "Desconfiar de mensagem com seu nome e CPF certos pedindo dado, senha ou Pix",
        "Conferir no Registrato do Banco Central contas e chaves Pix no seu nome",
        "Combinar uma palavra-senha da famÃ­lia para pedido de dinheiro por mensagem",
    ],
    "conflito": [
        "Comida e Ã¡gua para 14 dias, guardadas sem chamar atenÃ§Ã£o",
        "Rotas para casa de parentes e um ponto de encontro fora do bairro",
        "Documentos e cÃ³pias num envelope fÃ¡cil de pegar",
        "Rede de vizinhos de confianÃ§a com um jeito de se avisar",
        "Seguir sÃ³ avisos de Ã³rgÃ£os oficiais; nÃ£o espalhar boato",
    ],
}

PASSOS = [
    ("1. Casa: o kit de 72 horas, depois 14 dias",
     "passos/1-casa-72h.md"),
    ("1b. Comer e cozinhar sem luz", "passos/1b-cozinhar-sem-luz.md"),
    ("2. NÃ£o depender sÃ³ do online", "passos/2-fora-do-online.md"),
    ("2b. Comunicar quando o sistema cai", "passos/2b-comunicar-sem-rede.md"),
    ("2c. Deslocamento: tanque e rotas", "passos/2c-deslocamento.md"),
    ("3. ProteÃ§Ã£o digital", "passos/3-digital.md"),
    ("4. SaÃºde e pessoas", "passos/4-saude-e-pessoas.md"),
    ("5. Trabalho: a migraÃ§Ã£o para a IA", "passos/5-trabalho-ia.md"),
]


def quantidades(pessoas: int, dias: int) -> dict:
    """Ãgua (L), garrafÃµes de 5 L, calorias e uma sugestÃ£o de comida para `pessoas` Ã— `dias`."""
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
        # alimento seco (arroz, feijÃ£o, macarrÃ£o, aveia) tem ~3.500 kcal por kg
        "kg_seco": round(kcal / 3500, 1),
    }


def br(n: float, casas: int = 0) -> str:
    """NÃºmero no jeito brasileiro: 24.000 e 6,9."""
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
    """Comer sem cozinhar nas 72 h; depois, como cozinhar sem luz conforme moradia e fogÃ£o."""
    if moradia == "apartamento" and fogao == "lenha":
        raise ValueError("fogÃ£o a lenha em apartamento nÃ£o entra no plano: escolha botijao, encanado ou eletrico")
    L = ["## Comer e cozinhar sem luz", "",
         "**72 horas: ninguÃ©m cozinha.** A famÃ­lia come o que jÃ¡ estÃ¡ pronto.", ""]
    L += [f"- [ ] {c}" for c in SEM_COZINHAR_72H] + [""]
    L += ["**Mais de 3 dias: como cozinhar.** O estoque de arroz, macarrÃ£o e feijÃ£o precisa de fogo e de Ã¡gua "
          "extra para cozinhar (os 2 L por dia sÃ£o sÃ³ para beber).", ""]
    fogoes = [fogao] if fogao else list(COZINHAR)
    if moradia == "apartamento" and not fogao:
        fogoes = ["botijao", "encanado", "eletrico"]
    moradias = [moradia] if moradia else list(MORAR)
    for f in fogoes:
        L += [f"### {FOGOES[f]}", ""] + [f"- [ ] {c}" for c in COZINHAR[f]] + [""]
    for m in moradias:
        L += [f"### {MORADIAS[m]}", ""] + [f"- [ ] {c}" for c in MORAR[m]] + [""]
    L += ["- [ ] Truques: comida que cozinha rÃ¡pido, feijÃ£o de lata, panela tampada, garrafa tÃ©rmica e calor guardado "
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
    fogao = normaliza(fogao, FOGOES, "fogÃ£o")
    q3 = quantidades(pessoas, DIAS_MINIMO)
    q14 = quantidades(pessoas, DIAS_META)
    titulo = f"Plano do caminho seguro â€” {nome}" if nome else "Plano do caminho seguro"
    L = [f"# {titulo}", "",
         f"Feito em {hoje:%d/%m/%Y}. **Revisar em {rev:%d/%m/%Y}** (validade de comida, remÃ©dio e pilha).", "",
         f"Casa: {pessoas} pessoa(s)"
         + (f", {criancas} crianÃ§a(s)" if criancas else "")
         + (f", {idosos} idoso(s)" if idosos else "")
         + (f", {pets} pet(s)" if pets else "") + "."
         + (f" {MORADIAS[moradia]}." if moradia else "")
         + (f" {FOGOES[fogao]}." if fogao else ""), "",
         "## Quanto guardar", "",
         "| | 72 horas (mÃ­nimo) | 14 dias (meta) |",
         "|---|---|---|",
         f"| Ãgua para beber (2 L por pessoa por dia) | {q3['agua_l']:.0f} L ({q3['garrafoes_5l']} garrafÃµes de 5 L) "
         f"| {q14['agua_l']:.0f} L ({q14['garrafoes_5l']} garrafÃµes de 5 L) |",
         f"| Comida | ~{br(q3['kcal'])} kcal de comida pronta, sem cozinhar "
         + (f"| ~{br(q14['kcal'])} kcal, a maior parte comida pronta (o fogÃ£o elÃ©trico nÃ£o cozinha sem luz) |"
          if fogao == "eletrico" else
          f"| ~{br(q14['kcal'])} kcal (â‰ˆ {br(q14['kg_seco'], 1)} kg de alimento seco, que precisa de fogo) |"),
         "", "Ãgua de higiene e de cozinhar Ã© Ã  parte. 72 h: lata pronta, biscoito, pÃ£o, castanhas, leite de caixinha "
         "(ninguÃ©m cozinha). 14 dias: o que a famÃ­lia jÃ¡ come e que dura (arroz, feijÃ£o, macarrÃ£o, aveia, enlatados), "
         "com um jeito de cozinhar sem luz. Gire: use e reponha.", ""]
    if criancas:
        L += ["- [ ] Fralda, leite/fÃ³rmula, remÃ©dio infantil e um brinquedo ou livro para cada crianÃ§a"]
    if idosos:
        L += ["- [ ] Ã“culos reserva, aparelho auditivo/pilhas e a lista de remÃ©dios de cada idoso"]
    if pets:
        L += ["- [ ] RaÃ§Ã£o e Ã¡gua do pet para os mesmos 14 dias, guia, caixa de transporte e cartÃ£o de vacina"]
    if remedios or idosos:
        L += ["- [ ] RemÃ©dios de uso contÃ­nuo para 14 dias a mais e cÃ³pia da receita guardada no kit"]
    if criancas or idosos or pets or remedios:
        L += [""]
    L += secao_cozinhar(moradia, fogao)
    L += ["## Comunicar quando o sistema cai", ""] + [f"- [ ] {c}" for c in COMUNICAR] + [""]
    L += ["## Deslocamento", ""] + [f"- [ ] {c}" for c in DESLOCAR] + [""]
    L += ["## Os 5 passos", ""]
    for t, arq in PASSOS:
        L += [f"- [ ] **{t}** â€” ver `{arq}`"]
    L += [""]
    if riscos:
        L += ["## Os riscos da sua regiÃ£o", ""]
        for r in riscos:
            L += [f"### {RISCOS[r]}", ""] + [f"- [ ] {c}" for c in CHECK_RISCO[r]] + [""]
    L += ["## Folha da geladeira", "",
          "- Defesa Civil **199** Â· Bombeiros **193** Â· SAMU **192** Â· PolÃ­cia **190**",
          "- Ponto de encontro da famÃ­lia: ______________________",
          "- Quem busca as crianÃ§as: ______________________",
          "- Parente fora da cidade (contato de todos): ______________________", "",
          "## Trabalho", "",
          "- [ ] Descobrir o meu nÃ­vel de IA (certificado grÃ¡tis): https://linnoff88-dev.github.io/
          "- [ ] Escolher a prÃ³xima tarefa do meu trabalho para a IA fazer comigo",
          "- [ ] Aprender de graÃ§a no https://ARCKHÉ AI", "",
          "_Kit caminho-seguro (ARCKHÉ, grÃ¡tis). NÃ£o substitui a orientaÃ§Ã£o da Defesa Civil da sua cidade._", ""]
    return "\n".join(L)


def perguntar(msg: str, padrao: str = "") -> str:
    r = input(f"{msg}{f' [{padrao}]' if padrao else ''}: ").strip()
    return r or padrao


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Monta o seu plano do caminho seguro (grÃ¡tis, sem internet).")
    ap.add_argument("--nome", default=None, help="nome da famÃ­lia (aparece no tÃ­tulo)")
    ap.add_argument("--pessoas", type=int)
    ap.add_argument("--criancas", type=int, default=0)
    ap.add_argument("--idosos", type=int, default=0)
    ap.add_argument("--pets", type=int, default=0)
    ap.add_argument("--remedios", action="store_true", help="alguÃ©m toma remÃ©dio de uso contÃ­nuo")
    ap.add_argument("--riscos", default=None, help="lista: " + ",".join(RISCOS))
    ap.add_argument("--moradia", default=None, help="onde mora: " + ",".join(MORADIAS))
    ap.add_argument("--fogao", default=None, help="fogÃ£o: " + ",".join(FOGOES) + " (inducao = eletrico)")
    ap.add_argument("--saida", default="meu-plano.md")
    ap.add_argument("--listar-riscos", action="store_true")
    a = ap.parse_args(argv)

    if a.listar_riscos:
        for k, v in RISCOS.items():
            print(f"{k:10} {v}")
        return 0
    try:
        if a.pessoas is None:  # modo perguntas
            print("Caminho seguro â€” o seu plano (Enter aceita o padrÃ£o)\n")
            a.nome = perguntar("Nome da famÃ­lia", a.nome or "")
            a.pessoas = int(perguntar("Quantas pessoas moram na casa", "2"))
            a.criancas = int(perguntar("Quantas sÃ£o crianÃ§as", "0"))
            a.idosos = int(perguntar("Quantas sÃ£o idosas", "0"))
            a.pets = int(perguntar("Quantos pets", "0"))
            a.remedios = perguntar("AlguÃ©m toma remÃ©dio de uso contÃ­nuo? (s/n)", "n").lower().startswith("s")
            print("Riscos: " + ", ".join(RISCOS))
            a.riscos = perguntar("Quais riscos tem na sua regiÃ£o (separe por vÃ­rgula)", "apagao,digital")
            a.moradia = perguntar("Onde mora (" + ", ".join(MORADIAS) + ")", "casa")
            a.fogao = perguntar("Qual Ã© o seu fogÃ£o (" + ", ".join(FOGOES) + ")", "botijao")
        riscos = parse_riscos(a.riscos or "apagao,digital")
        plano = montar_plano(a.nome or "", a.pessoas, a.criancas, a.idosos, a.pets, a.remedios, riscos,
                             moradia=a.moradia, fogao=a.fogao)
    except ValueError as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    except (EOFError, KeyboardInterrupt):
        print("\nsaÃ­ sem gravar nada.", file=sys.stderr)
        return 1
    Path(a.saida).write_text(plano, encoding="utf-8")
    q = quantidades(a.pessoas, DIAS_MINIMO)
    print(f"ok: {a.saida} â€” 72 h: {q['agua_l']:.0f} L de Ã¡gua; revise em {REVISAR_MESES} meses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
