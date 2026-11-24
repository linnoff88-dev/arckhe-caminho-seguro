# OpÃ§Ã£o 2 â€” Computador simples

Para notebook ou PC comum (sem placa de vÃ­deo, 8 GB de memÃ³ria ou menos). Windows, Linux ou Mac.

1. **Biblioteca:** instale o **Kiwix Desktop** (kiwix.org, grÃ¡tis) e abra um arquivo de Wikipedia:
   - portuguÃªs "nopic" (texto completo, sem fotos) â€” **6,6 GB**; com pouco disco, a "mini" â€” **1,6 GB**;
   - medicina em inglÃªs ("medicine nopic") â€” **1,0 GB**.
   Linux ou Mac, pelo terminal, o kit [sobreviver-ia](https://linnoff88-dev.github.io/ faz isso
   sozinho e mostra antes o que vai baixar: `bash offline/instala-offline.sh --wiki pt --tipo mini --sem-ollama`
   (sem `--instalar` nada Ã© baixado).
2. **Mapas:** Organic Maps no celular (opÃ§Ã£o 1) jÃ¡ resolve.
3. **IA pequena (opcional):** um modelo de 3 bilhÃµes de parÃ¢metros roda no processador, devagar.
   Linux/Mac: o mesmo script do sobreviver-ia sem o `--sem-ollama` instala o Ollama e o `llama3.2:3b`.
   Windows: instale o Ollama (ollama.com) e rode `ollama run llama3.2:3b`.
4. Teste com a internet ligada uma vez: abra um artigo, depois desligue o Wi-Fi e abra de novo.
