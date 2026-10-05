# Arquivo Político

A história por trás do voto: contexto das eleições brasileiras e trajetórias políticas documentadas.

Esta edição reúne a página inicial, a eleição presidencial de 2002 e os seis candidatos, com fontes por trecho, cronologias, propostas, atuação nos cargos e limites da pesquisa.

## GitHub Pages

Em **Settings → Pages**, selecione **Deploy from a branch**, branch **main** e pasta **/docs**. Endereço previsto após ativação: `https://gabsgabsz.github.io/arquivo-politico/`.

## Gerar o site

Requer Python 3, sem dependências externas:

```sh
python build.py
```

Edite `content/profiles.json` para alterar as trajetórias e `content/candidates.json` para dados dos cartões e créditos fotográficos. Geradores: `build.py` e `profiles.py`. Estilos e scripts: `profile.css` e `static/`. A pasta `docs/` contém o site pronto.

Para hospedar na raiz de um domínio: `BASE_PATH="" python build.py`. Para outro repositório: `BASE_PATH="/nome-do-repositorio" python build.py`.

## Critérios editoriais e direitos

Propostas, execução e resultados são tratados separadamente. Investigações e decisões judiciais têm datas e desfechos documentados. As limitações constam de cada ficha. Não é certidão judicial nem inventário exaustivo.

Créditos e licenças de fotografias aparecem no site. Materiais de terceiros conservam seus direitos e condições de uso. O retrato de Rui Costa Pimenta é carregado do Wikimedia Commons; os demais estão em `static/assets/`. As fontes são vinculadas diretamente nas páginas.
