# FieldTech Industrial Sensors

Estrutura de pesquisa, ainda sem modelos publicados. Meta: selecionar até 20 modelos exatos por tipo, com cobertura mundial. As 400 posições são metas de seleção, não 400 dispositivos distintos: um modelo pode aparecer em mais de um filtro, mas terá um único pack.

## Tipos e ordem de preenchimento

| Etapa | Tipos | Meta por tipo |
| --- | --- | --- |
| 1 — presença e manutenção | Fotoelétrico emissor/receptor; com refletor; difuso; supressão de fundo; laser emissor/receptor; laser com refletor; laser difuso; indutivo | 20 |
| 2 — aplicações especializadas | Laser de distância/deslocamento; transparentes; fibra óptica; forquilha/etiquetas; contraste/cor; capacitivo; ultrassônico; magnético de cilindro | 20 |
| 3 — variáveis de processo | Pressão/vácuo; temperatura; nível; vazão | 20 |

Laser é fonte de luz, não princípio de detecção. Registrar separadamente tecnologia, princípio, fonte de luz e aplicação. “Espelho” significa refletor compatível indicado pelo fabricante; não presumir que um espelho comum serve. Sensores de segurança, cortinas e scanners ficam para uma categoria própria com requisitos de validação específicos.

## Seleção e evidência

“20 mais vendidos mundialmente” é o objetivo de pesquisa, não uma classificação já comprovada. Ranking exige fonte, período, mercados, métrica (unidades ou receita) e modelos comparáveis. Não converter catálogo de fabricante, presença em distribuidores ou posição em busca em prova de vendas. Quando faltar evidência, identificar a seleção como **prioridade inferida para técnicos**, registrar justificativa e manter `salesRankingConfirmed: false`.

Pesquisar o grupo de fabricantes do [manifesto](manifest.json); ele é uma lista de investigação, sem ordem de vendas. Confirmar código completo: família comercial não substitui variante PNP/NPN, cabo/conector, alimentação, alcance e interface. No emissor/receptor, identificar os dois códigos e a compatibilidade; contar o par como uma solução. Família e variantes relacionadas devem permanecer visíveis sem inflar o ranking.

## Dados de cada pack

- Identidade: fabricante, família, código exato, região, revisão e situação comercial.
- Detecção: tecnologia, princípio, fonte de luz, alcance, zona cega, alvo de referência e condições de medição.
- Elétrica: alimentação, saída PNP/NPN/push-pull/relé/analógica, NO/NC, Light-ON/Dark-ON, conector, pinagem e diagrama oficial.
- Instalação: alinhamento, refletor ou fibra compatível, montagem, interferência entre sensores e condições ambientais.
- Ajustes: teach-in, sensibilidade, supressão de fundo, filtros, temporizações e IO-Link quando documentados para a variante.
- Diagnóstico: LEDs, mensagens, códigos e testes orientados por sintoma. Não inventar alarmes para sensores que só têm LEDs.
- Campo: limpeza, checagem da alimentação, verificação da entrada do CLP, checklist e limites de substituição.
- Evidência por item: URL oficial, título do documento, revisão, página/seção, data de consulta e variante aplicável. Valor não encontrado permanece desconhecido; ausência de documentação não significa recurso inexistente.

## Fluxo de pesquisa, publicação e drop

1. Registrar candidato e tipo em `manifest.json`, com status `pending-research` e justificativa de seleção.
2. Confirmar modelo e obter manual/datasheet oficial; classificar `model-confirmed`, sem declarar parâmetros verificados ainda.
3. Extrair fatos com referências e revisar variante, unidades, pinagem e LEDs. Classificar `manual-verified` apenas após revisão.
4. Criar pack bilíngue en/pt em `packs/<fabricante>/<modelo>.json`; validar com esquema específico de sensores antes de `published`.
5. Publicar em manifesto próprio e gerar bundle/drop próprio depois que houver packs. O manifesto legado de drives permanece com seu contrato atual.

Os diretórios de packs e o drop serão criados com os primeiros modelos verificados. Esta mudança entrega taxonomia e fila, não implementa ainda o importador de sensores nem adapta automaticamente a interface FieldTech. Não usar o validador ou bundle de drives para publicar sensores: o esquema de parâmetros/alarmes de inversores não representa esse domínio.

Trabalhar no mesmo repositório por diretórios. Branches de trabalho como `sensors/photoelectric-wave-1` servem à revisão e são integradas depois; não são categorias permanentes. Guardar URLs oficiais dos manuais; redistribuir PDFs apenas quando autorizado pela licença.

## Fontes da classificação

- [SICK — princípios de detecção e fontes de luz](https://www.sick.com/in/en/photoelectric-sensors-portfolio/s/next-generation).
- [ifm — categorias de sensores industriais](https://www.ifm.com/us/en/category).

Princípios ópticos e categorias gerais têm suporte nessas fontes. A divisão em 20 grupos, a ordem de execução e o grupo de fabricantes são decisões de planejamento; nenhum ranking mundial de modelos foi confirmado nesta etapa.
