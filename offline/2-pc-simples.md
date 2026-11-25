ï»¿# OpêÂ§êÂ£o 2 ê¢â¬â Computador simples

Para notebook ou PC comum (sem placa de vêÂ­deo, 8 GB de memêÂ³ria ou menos). Windows, Linux ou Mac.

1. **Biblioteca:** instale o **Kiwix Desktop** (kiwix.org, grêÂ¡tis) e abra um arquivo de Wikipedia:
   - portuguêÂªs "nopic" (texto completo, sem fotos) ê¢â¬â **6,6 GB**; com pouco disco, a "mini" ê¢â¬â **1,6 GB**;
   - medicina em inglêÂªs ("medicine nopic") ê¢â¬â **1,0 GB**.
   Linux ou Mac, pelo terminal, o kit [sobreviver-ia](https://linnoff88-dev.github.io/ faz isso
   sozinho e mostra antes o que vai baixar: `bash offline/instala-offline.sh --wiki pt --tipo mini --sem-ollama`
   (sem `--instalar` nada êÂ© baixado).
2. **Mapas:** Organic Maps no celular (opêÂ§êÂ£o 1) jêÂ¡ resolve.
3. **IA pequena (opcional):** um modelo de 3 bilhêÂµes de parêÂ¢metros roda no processador, devagar.
   Linux/Mac: o mesmo script do sobreviver-ia sem o `--sem-ollama` instala o Ollama e o `llama3.2:3b`.
   Windows: instale o Ollama (ollama.com) e rode `ollama run llama3.2:3b`.
4. Teste com a internet ligada uma vez: abra um artigo, depois desligue o Wi-Fi e abra de novo.
