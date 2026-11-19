# caminho-seguro

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![caminho-seguro](guia/assets/banner-es.jpg)](https://inematds.github.io/caminho-seguro/guia/es/)

## Qué es

El camino seguro es una guía gratis de INEMA para que tú y tu familia atraviesen los próximos años de inestabilidad: inundaciones, tornados y calor con un El Niño muy fuerte, apagones, ataques a sistemas y filtraciones de datos, y el trabajo cambiando con robots e inteligencia artificial. Son 5 pasos simples: armar el kit de casa, no depender solo de internet, proteger tus cuentas, cuidar la salud y acordar un plan familiar, y preparar tu trabajo para la IA. Para leerla no necesitas nada. Si quieres, un pequeño programa arma el plan de tu casa en un minuto.

**El mundo se detendrá con frecuencia, y quienes se preparen podrán atravesarlo con su familia a salvo.**  
El camino seguro es un kit gratis de INEMA con 5 pasos para afrontar los próximos años de inestabilidad: clima extremo  
(El Niño muy fuerte, inundaciones, tornados, calor), ataques digitales, conflictos y el trabajo cambiando con robots e IA.

📖 Guía: **https://inematds.github.io/caminho-seguro/guia/es/**

🎬 Video (lives10): https://www.youtube.com/watch?v=Sp28Yi-zKU4 · Short: https://youtube.com/shorts/JrROTl6skg8

🎬 Video (lives11): https://www.youtube.com/watch?v=oN9sCuGD1b4 · Short: https://youtube.com/shorts/YpXU0OIhnG4

🎬 Video (lives3): https://www.youtube.com/watch?v=4iFMGw9YwhE · Short: https://youtube.com/shorts/zKYDYleamvU


## Los 5 pasos

| Paso | Qué es | Archivo |
|---|---|---|
| 1. Casa | Kit de 72 horas de Defensa Civil (2 L de agua por persona al día), después 14 días | [passos/1-casa-72h.md](passos/1-casa-72h.md) |
| 1b. Cocinar sin electricidad | 72 horas sin cocinar (comida lista); después, cómo cocinar según la vivienda (casa, finca, apartamento) y la cocina (bombona, gas por tubería, eléctrica, leña) | [passos/1b-cozinhar-sem-luz.md](passos/1b-cozinhar-sem-luz.md) |
| 2. Fuera de línea | Dinero en efectivo para algunos días, papel, información sin conexión, comida sin depender de la app | [passos/2-fora-do-online.md](passos/2-fora-do-online.md) |
| 2b. Comunicarse sin red | Celular con al menos una carga, radio AM/FM a pilas, walkie-talkie de uso libre, Radio del Ciudadano y radioaficionado (licencia de Anatel) | [passos/2b-comunicar-sem-rede.md](passos/2b-comunicar-sem-rede.md) |
| 2c. Desplazamiento | Tanque nunca por debajo de la mitad, reserva segura, kit del auto, dos rutas, sin auto | [passos/2c-deslocamento.md](passos/2c-deslocamento.md) |
| 3. Digital | La estafa después de la filtración, verificación en dos pasos mediante una aplicación, Registrato | [passos/3-digital.md](passos/3-digital.md) |
| 4. Salud y personas | Medicamentos de reserva, acuerdo familiar, vecinos, alerta 40199 | [passos/4-saude-e-pessoas.md](passos/4-saude-e-pessoas.md) |
| 5. Trabajo | Certificado de tu nivel de IA, la próxima tarea para la IA, inema.club gratis | [passos/5-trabalho-ia.md](passos/5-trabalho-ia.md) |

Los mejores manuales oficiales y gratuitos ya disponibles (72 horas, de 10 días a un mes, sin médico): [MANUAIS.md](MANUAIS.md).

## Tu plan en 1 minuto

```bash
git clone https://github.com/inematds/caminho-seguro && cd caminho-seguro
python3 caminho.py            # responde 7 preguntas y guarda meu-plano.md
```

O directamente: `python3 caminho.py --pessoas 4 --criancas 1 --riscos enchente,apagao,digital --saida meu-plano.md`.  
Riesgos: `enchente`, `vendaval`, `calor`, `apagao`, `digital`, `conflito` (`--listar-riscos`).  
Vivienda y cocina: `--moradia casa|sitio|apartamento --fogao botijao|encanado|eletrico|lenha` (el plan muestra solo la forma de cocinar que corresponde a tu vivienda).
El plan incluye agua y comida para 72 h y 14 días, las listas de verificación de los riesgos de tu región, la hoja para el refrigerador  
(199 · 193 · 192) y la fecha de la próxima revisión (6 meses). Ejemplo: [exemplo/meu-plano-exemplo.md](exemplo/meu-plano-exemplo.md).  
Python 3.9+, sin instalar nada y sin internet.

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Leer la guía y los 5 pasos | abrir https://inematds.github.io/caminho-seguro/guia/ | 🧠 tú |
| 2 | Generar el plan de tu casa | `python3 caminho.py` | ⚙️ script |
| 3 | Preparar el kit de 72 horas | lista de verificación del paso 1 en `meu-plano.md` | 🧠 tú |
| 4 | Proteger las cuentas | paso 3 (verificación en dos pasos por app, Registrato) | 🧠 tú |
| 5 | Acordar un plan con la familia e imprimir la hoja para el refrigerador | paso 4 | 🧠 tú |
| 6 | Medir tu nivel de IA | certificado del kit [nivel-ia](https://inematds.github.io/nivel-ia/guia/#certificado) | ⚙️ script / 🤖 Claude Code o Codex |
| 7 | Llegar a 14 días y revisar cada 6 meses | `python3 caminho.py` de nuevo | 🧠 tú |
| 8 | Probar el kit (para quienes modifican el código) | `python3 -m pytest -q tests` | ⚙️ script |

## Biblioteca sin internet (elige 1 de 3)

Solo celular · computadora sencilla · computadora potente ([Project NOMAD](https://inematds.github.io/project-nomad/guia/es/)). Una opción por aparato, cada una en su archivo (en portugués): [offline/README.md](offline/README.md).

## Kits hermanos

- [sobreviver-ia](https://inematds.github.io/sobreviver-ia/guia/) — Wikipedia e IA sin conexión, auditoría de las cuentas, plan de 90 días.
- [nivel-ia](https://inematds.github.io/nivel-ia/guia/) — el certificado de tu nivel de IA.

No sustituye las indicaciones de Defensa Civil de tu ciudad. No es asesoramiento financiero ni médico.

## Licencia

MIT — consulta [LICENSE](LICENSE). Versión 1.0.0. Parte del ecosistema [INEMA.CLUB](https://inema.club) — gratis.

## Aprendizaje autónomo

Cuando algo salga mal, la lección irá al principio de [LESSONS.md](LESSONS.md).

## Lecciones

Consulta [LESSONS.md](LESSONS.md).