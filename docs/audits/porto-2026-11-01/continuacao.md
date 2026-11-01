# Porto — continuação de 1 de novembro de 2026

Estado: parcial. Lotes publicados após autorização direta do utilizador nesta conversa.

## Alterações publicadas

15 recintos receberam descrições e fontes nas fichas existentes do Notion e nos ficheiros municipais da planta: Regilde, Unhão, São Jorge de Vizela, Vila Verde (Felgueiras), Canelas (Penafiel), Luzim, antigo São Martinho de Recesinhos, Rio de Moinhos, Termas de São Vicente, Jugueiros (Termas de São Vicente), Arcos, Malta, Retorta e Touguinha; Valpedre completa os 15.

Foram preservados limites administrativos, coordenadas, IDs, fotografias, áreas e anos já existentes. Não se alterou a interface. Datas de projetos, ampliações, trasladações e registos de utilização não foram convertidas em inaugurações.

Retorta: o Mapa n.º 29/2025, Diário da República de 14-08-2025, distingue Cemitério de Retorta (bem 500) e Cemitério novo Retorta (bem 502). A ficha Notion regista a distinção; no ficheiro municipal, o segundo bem ficou em pendingCemeteries, sem coordenadas e sem duplicar o ponto existente.

## Verificação

18 concelhos; 275 fichas administrativas; 424 pontos; zero descrições com o antigo texto genérico de registo cartográfico. Verificação pelo script do repositório: zero erros estruturais.

54 fotografias identificadas (52 com kind ground e 2 com kind photograph); 370 alternativas de satélite. 3 áreas numéricas; 8 anos numéricos de abertura e 1 período de abertura. Estes números não comprovam exaustividade, confirmação cadastral ou validação de todas as designações.

O contador groundPhotos do script antigo inclui apenas kind ground; por isso mostra 52, embora existam mais 2 fotografias com kind photograph. A contagem de pendências inclui bens já relacionados com outros pontos e projetos, não apenas recintos existentes ainda por localizar.

## Pendências

Prosseguir procura de fotografias identificadas e confirmação de áreas e inaugurações. Comparar integralmente as freguesias com a divisão oficial atual. Localizar o Cemitério do Santo de Idães e esclarecer Retorta, os projetos em construção e as correspondências de recintos partilhados. Não declarar o distrito concluído.

A publicação dos dados foi efetuada pelo conector GitHub porque o git local não dispõe de credenciais de escrita. Último commit de dados deste lote: ecbbfdc4c091190c472c3f478c4c658de99b9988. A publicação anterior, 69c0ec63dd13c7e5928d347b256457fd1ebfa8cb, terminou o workflow com sucesso. Nenhuma ferramenta informou esgotamento de Work.


## Continuação — 1 de novembro de 2026, segunda revisão

- Oito notas patrimoniais de Penafiel acrescentadas primeiro no Notion e depois na planta: Irivo, Luzim, Oldrões, Novelas, Milhundos, Rio de Moinhos, Rio Mau e São Miguel de Paredes. Áreas de terrenos e datas de aquisição mantidas separadas da área global e da inauguração.
- Oito fotografias identificadas substituem o satélite: Avintes, Gião, Oliveira do Douro, Vandoma, Novelas, Marecos, Meiral e Chouselas. Fontes institucionais e imagens inspecionadas individualmente. As fotografias anteriores de Penafiel e Milhundos foram preservadas no campo Foto da ficha partilhada.
- Novelas: inventário municipal refere enterramentos de 1911 e declara desconhecer a inauguração; ligação direta antiga indisponível, consulta efetuada no índice público. Amarante: cronologia de 1881 documentada em bibliografia académica, distinguindo o projeto não executado de Santa Clara, de 1866; não convertida em inauguração formal.
- Santo de Idães: ponto editorial do All About Portugal em Seromonheiro (41.3292310619, -8.2558519683), cruzado com recinto visível na imagem aérea e inclusão nos limites de Idães. Associação ao Santo provisória, explicitada no Notion e na planta, sem alegar coordenada oficial ou confirmação cadastral. Fotografia já identificada preservada. Bom Jesus conserva um único ponto em Barrosas (Santo Estêvão).
- Cobertura administrativa conferida diretamente com o serviço oficial CAOP2025 da DGT: 275 freguesias, correspondência exata de concelho e nome, sem faltas ou extras. O Notion contém igualmente as 275 fichas nos 18 concelhos, confirmado por consulta agrupada.
- A planta passa a apresentar também as referências guardadas em documentarySource, documentarySources e historicalEvidence. Verificação funcional do extrator com 95 registos reais e fontes em formatos diferentes.

### Estado quantitativo desta revisão

18 concelhos; 275 fichas; 425 pontos; 63 fotografias identificadas (61 ground e 2 photograph); 362 alternativas de satélite. Mantêm-se 3 áreas numéricas, 8 anos numéricos e 1 período de abertura. Os JSON publicados dos 18 concelhos foram analisados com sucesso. As 58 ligações de fotografias existentes antes das últimas substituições responderam com conteúdo de imagem; o endereço de Vila Caiz requereu codificação normal de caracteres Unicode. As novas imagens foram descarregadas e inspecionadas.

### Pendências atuais

O bem «Cemitério novo Retorta» continua sem localização distinta confirmada. Santo de Idães exige confirmação cadastral da associação. Bom Jesus, Santa Marinha/Afurada e a ala Meixomil/Paços são relações entre fichas, sem duplicar recintos. O Novo Cemitério de Ferreira é projeto, não tratado como recinto aberto. Continuam por confirmar áreas, inaugurações, coordenadas oficiais e fotografias em numerosos registos. A cobertura administrativa está confirmada; a exaustividade do inventário cemiterial não está demonstrada. Não declarar o distrito documentalmente concluído.

Fontes de cobertura: https://www.dgterritorio.gov.pt/atividades/cartografia/cartografia-tematica/caop e serviço https://infogeo.dgterritorio.gov.pt/arcgis/rest/services/Hosted/FreguesiaCAOP2025/FeatureServer/7 (consulta apenas de leitura, filtro distrito_ilha = Porto).
