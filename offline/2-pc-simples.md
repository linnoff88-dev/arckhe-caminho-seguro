# Opção 2 — Computador simples

Para notebook ou PC comum (sem placa de vídeo, 8 GB de memória ou menos). Windows, Linux ou Mac.

1. **Biblioteca:** instale o **Kiwix Desktop** (kiwix.org, grátis) e abra um arquivo de Wikipedia:
   - português "nopic" (texto completo, sem fotos) — **6,6 GB**; com pouco disco, a "mini" — **1,6 GB**;
   - medicina em inglês ("medicine nopic") — **1,0 GB**.
   Linux ou Mac, pelo terminal, o kit [sobreviver-ia](https://inematds.github.io/sobreviver-ia/guia/) faz isso
   sozinho e mostra antes o que vai baixar: `bash offline/instala-offline.sh --wiki pt --tipo mini --sem-ollama`
   (sem `--instalar` nada é baixado).
2. **Mapas:** Organic Maps no celular (opção 1) já resolve.
3. **IA pequena (opcional):** um modelo de 3 bilhões de parâmetros roda no processador, devagar.
   Linux/Mac: o mesmo script do sobreviver-ia sem o `--sem-ollama` instala o Ollama e o `llama3.2:3b`.
   Windows: instale o Ollama (ollama.com) e rode `ollama run llama3.2:3b`.
4. Teste com a internet ligada uma vez: abra um artigo, depois desligue o Wi-Fi e abra de novo.
