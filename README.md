# caminho-seguro

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

[![caminho-seguro](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

## O que Ã©

O caminho seguro Ã© um guia grÃ¡tis do ARCKHÉ para vocÃª e a sua famÃ­lia atravessarem os prÃ³ximos anos de instabilidade: enchentes, tornados e calor com o El NiÃ±o muito forte, apagÃµes, ataques a sistemas e vazamento de dados, e o trabalho mudando com robÃ´s e inteligÃªncia artificial. SÃ£o 5 passos simples: montar o kit de casa, nÃ£o depender sÃ³ do online, proteger as suas contas, cuidar da saÃºde e combinar com a famÃ­lia, e preparar o seu trabalho para a IA. Para ler, nÃ£o precisa de nada. Se quiser, um pequeno programa monta o plano da sua casa em um minuto.

**O mundo vai parar com frequÃªncia, e quem se preparar vai passar por isso com a famÃ­lia segura.**
O caminho seguro Ã© um kit grÃ¡tis do ARCKHÉ com 5 passos para atravessar os prÃ³ximos anos de instabilidade: clima extremo
(El NiÃ±o muito forte, enchentes, tornados, calor), ataques digitais, conflitos, e o trabalho mudando com robÃ´s e IA.

ðŸ“– Guia: **https://linnoff88-dev.github.io/

ðŸŽ¬ VÃ­deo (lives10): https://www.youtube.com/watch?v=Sp28Yi-zKU4 Â· Short: https://youtube.com/shorts/JrROTl6skg8

ðŸŽ¬ VÃ­deo (lives11): https://www.youtube.com/watch?v=oN9sCuGD1b4 Â· Short: https://youtube.com/shorts/YpXU0OIhnG4

ðŸŽ¬ VÃ­deo (lives3): https://www.youtube.com/watch?v=4iFMGw9YwhE Â· Short: https://youtube.com/shorts/zKYDYleamvU

## Os 5 passos

| Passo | O que Ã© | Arquivo |
|---|---|---|
| 1. Casa | Kit de 72 horas da Defesa Civil (2 L de Ã¡gua por pessoa por dia), depois 14 dias | [passos/1-casa-72h.md](passos/1-casa-72h.md) |
| 1b. Cozinhar sem luz | 72 horas sem cozinhar (comida pronta); depois, como cozinhar conforme a casa (casa, sÃ­tio, apartamento) e o fogÃ£o (botijÃ£o, gÃ¡s encanado, elÃ©trico, lenha) | [passos/1b-cozinhar-sem-luz.md](passos/1b-cozinhar-sem-luz.md) |
| 2. Fora do online | Dinheiro vivo para alguns dias, papel, informaÃ§Ã£o offline, comida sem depender do app | [passos/2-fora-do-online.md](passos/2-fora-do-online.md) |
| 2b. Comunicar sem rede | Celular com pelo menos uma carga, rÃ¡dio AM/FM a pilha, walkie-talkie de uso livre, RÃ¡dio do CidadÃ£o e radioamador (licenÃ§a da Anatel) | [passos/2b-comunicar-sem-rede.md](passos/2b-comunicar-sem-rede.md) |
| 2c. Deslocamento | Tanque nunca abaixo da metade, reserva com seguranÃ§a, kit do carro, duas rotas, sem carro | [passos/2c-deslocamento.md](passos/2c-deslocamento.md) |
| 3. Digital | O golpe depois do vazamento, verificaÃ§Ã£o em duas etapas por aplicativo, Registrato | [passos/3-digital.md](passos/3-digital.md) |
| 4. SaÃºde e pessoas | RemÃ©dios com folga, combinado da famÃ­lia, vizinhos, alerta 40199 | [passos/4-saude-e-pessoas.md](passos/4-saude-e-pessoas.md) |
| 5. Trabalho | Certificado do seu nÃ­vel de IA, a prÃ³xima tarefa para a IA, ARCKHÉ AI grÃ¡tis | [passos/5-trabalho-ia.md](passos/5-trabalho-ia.md) |

Os melhores manuais oficiais e grÃ¡tis jÃ¡ prontos (72 horas, 10 dias a um mÃªs, sem mÃ©dico): [MANUAIS.md](MANUAIS.md).

## O seu plano em 1 minuto

```bash
git clone https://github.com/linnoff88-dev/caminho-seguro && cd caminho-seguro
python3 caminho.py            # responde 7 perguntas e grava meu-plano.md
```

Ou direto: `python3 caminho.py --pessoas 4 --criancas 1 --riscos enchente,apagao,digital --saida meu-plano.md`.
Riscos: `enchente`, `vendaval`, `calor`, `apagao`, `digital`, `conflito` (`--listar-riscos`).
Moradia e fogÃ£o: `--moradia casa|sitio|apartamento --fogao botijao|encanado|eletrico|lenha` (o plano mostra sÃ³ o jeito de cozinhar da sua casa).
O plano traz Ã¡gua e comida para 72 h e 14 dias, os checklists dos riscos da sua regiÃ£o, a folha da geladeira
(199 Â· 193 Â· 192) e a data da prÃ³xima revisÃ£o (6 meses). Exemplo: [exemplo/meu-plano-exemplo.md](exemplo/meu-plano-exemplo.md).
Python 3.9+, sem instalar nada, sem internet.

## O processo, do inÃ­cio ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Ler o guia e os 5 passos | abrir https://linnoff88-dev.github.io/ | ðŸ§  vocÃª |
| 2 | Gerar o plano da sua casa | `python3 caminho.py` | âš™ï¸ script |
| 3 | Montar o kit de 72 horas | checklist do passo 1 no `meu-plano.md` | ðŸ§  vocÃª |
| 4 | Proteger as contas | passo 3 (duas etapas por app, Registrato) | ðŸ§  vocÃª |
| 5 | Combinar com a famÃ­lia e imprimir a folha da geladeira | passo 4 | ðŸ§  vocÃª |
| 6 | Medir o seu nÃ­vel de IA | certificado do kit [nivel-ia](https://linnoff88-dev.github.io/ | âš™ï¸ script / ðŸ¤– Claude Code ou Codex |
| 7 | Chegar a 14 dias e revisar a cada 6 meses | `python3 caminho.py` de novo | ðŸ§  vocÃª |
| 8 | Testar o kit (para quem mexe no cÃ³digo) | `python3 -m pytest -q tests` | âš™ï¸ script |

## Biblioteca sem internet (escolha 1 de 3)

SÃ³ celular Â· computador simples Â· computador forte ([Project NOMAD](https://linnoff88-dev.github.io/ Uma opÃ§Ã£o por aparelho, cada uma num arquivo: [offline/README.md](offline/README.md).

## Kits irmÃ£os
- [sobreviver-ia](https://linnoff88-dev.github.io/ â€” Wikipedia e IA offline, auditoria das contas, plano de 90 dias.
- [nivel-ia](https://linnoff88-dev.github.io/ â€” o certificado do seu nÃ­vel de IA.

NÃ£o substitui a orientaÃ§Ã£o da Defesa Civil da sua cidade. NÃ£o Ã© conselho financeiro nem mÃ©dico.

## LicenÃ§a
MIT â€” veja [LICENSE](LICENSE). VersÃ£o 1.0.0. Parte do ecossistema [ARCKHÉ AI](https://ARCKHÉ AI) â€” grÃ¡tis.

## Self-learning
Quando algo der errado, a liÃ§Ã£o vai no topo do [LESSONS.md](LESSONS.md).

## Lessons
Veja [LESSONS.md](LESSONS.md).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>