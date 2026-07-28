---
name: consulta-normas-tributarias
description: Use SEMPRE que a tarefa envolver matéria tributária especializada — âmbito administrativo (fisco, consulta fiscal, contencioso administrativo/CARF) ou judicial — e for preciso consultar, localizar, citar ou conferir a vigência de normas e entendimentos tributários federais. Acionar para pedidos como "qual a norma/IN/ADI/parecer normativo sobre X", "o que a Receita entende sobre Y", "há Solução de Consulta COSIT a respeito", "existe súmula/jurisprudência do CARF sobre Z", "qual o entendimento do STJ/STF sobre este tributo", "essa Instrução Normativa está em vigor?", "fundamente juridicamente esta tese tributária", ou sempre que uma peça, parecer ou resposta depender do teor exato de norma infralegal da RFB (IN, ADI, ADE, PN, SC/SD COSIT/DISIT, Portaria, Nota) buscável no SIJUT2 da Receita Federal. Não usar para cálculo puro de tributo sem discussão de norma, nem para direito não tributário.
license: Proprietary — uso interno Advocacia Vale de Oliva / AAGE / LexFlow.
---

# Consulta e Busca de Normas e Entendimentos Tributários

## Por que esta skill existe

Uma tese tributária — administrativa ou judicial — se sustenta no **teor exato**
e na **vigência atual** da norma que a embasa. Norma tributária infralegal muda
o tempo todo: uma Instrução Normativa é revogada por outra, um Parecer Normativo
é superado, uma Solução de Consulta COSIT altera o entendimento anterior, um
dispositivo é alterado por ato posterior. Citar o número errado, a redação
revogada, ou um entendimento já superado não é detalhe: derruba a peça, expõe o
cliente a autuação e compromete a credibilidade perante o fisco ou o Judiciário.

Esta skill documenta **como consultar a fonte primária** (com destaque para o
SIJUT2 da Receita Federal), **como raspar/acessar de forma programática**, e
**como citar e conferir vigência** — para que toda afirmação sobre uma norma
tributária seja rastreável ao ato original, na redação vigente no momento da
redação.

## Princípio central (barreira nº 1)

**Nunca afirme o número, a data, a redação ou a vigência de uma norma tributária
a partir da memória do modelo.** Modelos de linguagem alucinam números de IN,
datas de publicação e ementas com altíssima confiança. Antes de escrever "a IN
RFB nº X/AAAA dispõe que…", **verifique no SIJUT2 (ou na fonte primária cabível)
o ato, sua ementa e sua situação (vigente/revogado/alterado)**, e cite o `idAto`
ou a URL de origem.

Se a fonte não puder ser confirmada no momento (site fora do ar, domínio
bloqueado pela rede, ato não localizado), **declare isso expressamente**
("não confirmado no SIJUT2 nesta consulta", "a verificar a vigência") em vez de
preencher a lacuna com o que "provavelmente" é. Uma citação marcada como
"a confirmar" é honesta; uma citação alucinada apresentada como certa é um erro
grave.

---

## Passo 1 — Classificar a matéria: qual fonte primária?

Antes de buscar, decida **onde** a resposta mora. Fisco federal e contencioso
têm fontes distintas:

| Natureza da questão | Fonte primária | Onde consultar |
|---|---|---|
| **Norma infralegal da RFB** (IN, ADI, ADE, Parecer Normativo, Portaria, Nota, Ato Declaratório) | O próprio ato | **SIJUT2** — foco desta skill |
| **Entendimento da RFB em consulta fiscal** (Solução de Consulta / Solução de Divergência COSIT/DISIT) | A SC/SD | **SIJUT2** (indexa as SC/SD) |
| **Lei, Lei Complementar, Decreto, Medida Provisória** | O texto legal | planalto.gov.br (Planalto) / in.gov.br (DOU) |
| **Contencioso administrativo federal** (acórdãos e súmulas) | CARF | carf.economia.gov.br / gov.br/carf |
| **Jurisprudência judicial** (repetitivos, temas, súmulas) | STF, STJ, TRFs | portais dos tribunais (STF, STJ, JusBrasil como apoio, nunca como fonte única) |
| **Tributo estadual/municipal** | Legislação e atos do ente | portais das SEFAZ estaduais/municipais |

O SIJUT2 cobre a **produção normativa infralegal da Receita Federal** e as
**Soluções de Consulta/Divergência**. Não é a fonte para leis (Planalto) nem
para jurisprudência judicial. Não force o SIJUT2 a responder o que não é dele.

## Passo 2 — Hierarquia e efeito vinculante (para pesar o que se encontra)

Ao encontrar um ato, saiba **quanto ele pesa**. Ordem de força, do maior para o
menor, e a quem vincula (⚠️ confirme sempre a base legal atual do ato no próprio
SIJUT2 — os números de IN abaixo são referência e devem ser verificados):

1. **Constituição, Lei Complementar, Lei, Decreto** — hierarquia superior; ato
   infralegal que os contrarie é inválido.
2. **Parecer Normativo (PN) COSIT** — interpretação **vinculante para toda a
   administração tributária federal**. Muito forte no âmbito administrativo.
3. **Ato Declaratório Interpretativo (ADI RFB)** — interpretação vinculante para
   a administração.
4. **Instrução Normativa (IN RFB)** — regulamenta a aplicação da lei; vincula a
   administração e, na prática, o contribuinte quanto a obrigações acessórias.
5. **Solução de Consulta COSIT / Solução de Divergência** — tem **efeito
   vinculante no âmbito da RFB** e aproveita quem se enquadre na mesma situação
   (ver a IN que rege o processo de consulta — historicamente IN RFB 1.396/2013,
   atualizada por norma posterior; **verifique a IN vigente no SIJUT2**). A SC de
   unidade regional (DISIT) vincula em âmbito mais restrito que a COSIT.
6. **Nota, Despacho, Portaria interna** — força menor / operacional.

Implicações práticas:
- No **contencioso administrativo**, PN e SC COSIT vinculam a própria fiscalização
  — são armas fortes na defesa.
- No **judicial**, o ato infralegal da RFB **não vincula o juiz**; serve para
  demonstrar o entendimento do fisco (útil para atacar a autuação por
  contrariar a própria norma da RFB, ou para sustentar boa-fé/legítima
  expectativa), mas a tese de mérito se ancora em lei e jurisprudência.
- Uma SC **não vincula quem não é o consulente** — mas revela a interpretação
  oficial e, se COSIT, orienta toda a RFB.

---

## Passo 3 — SIJUT2: acesso, endpoints e raspagem

**Base:** `https://normas.receita.fazenda.gov.br/sijut2consulta/`

O SIJUT2 é uma aplicação Struts2 que **renderiza HTML no servidor — não há API
JSON oficial**. Os dois endpoints úteis:

| Endpoint | Função | Parâmetros-chave |
|---|---|---|
| `consulta.action` | Formulário e **lista de resultados** | `termoBusca`, `tiposAtosSelecionados` (código do tipo), `numero_ato`, `ano_ato`/`anoAtoFacet`, `tipoData`, `dt_inicio`, `dt_fim`, `orgaosSelecionados`, `p` (página) |
| `link.action` | **Texto integral** de um ato | `idAto=<id>`, `visao=<compilado\|anotado\|original>` |

`visao`:
- **`compilado`** → texto **consolidado atual** (com as alterações já
  incorporadas). É o que você quer para saber "o que vale hoje".
- **`anotado`** → texto com marcações de cada alteração/revogação (útil para ver
  o histórico e a redação por época).
- **`original`** → redação original de publicação.

### Operadores de busca (no `termoBusca`)
- `"expressão exata"` → aspas para frase literal.
- `palavra1 AND palavra2` → exige ambas.
- `palavra1 NOT palavra2` → exclui a segunda.
- Vários termos sem operador → busca ampla.

### Código do tipo de ato (`tiposAtosSelecionados`)
Cada tipo tem um código numérico. **Confirmado: `59` = Parecer Normativo (PN).**
Não presuma os demais — obtenha a lista atual direto do formulário:

```bash
python3 scripts/sijut2.py tipos      # imprime "codigo<TAB>rótulo" de cada tipo
```

(ou, no navegador, selecione o tipo no formulário e leia o valor de
`tiposAtosSelecionados` na URL resultante).

### Script de raspagem — `scripts/sijut2.py`

```bash
# Descobrir os códigos de tipo de ato
python3 scripts/sijut2.py tipos

# Só montar a URL de busca (funciona OFFLINE — cole no navegador se preciso)
python3 scripts/sijut2.py url --tipo 59 --termo '"crédito presumido"' --ano 2024

# Buscar (lista idAto + título de cada ato)
python3 scripts/sijut2.py buscar --tipo 59 --termo '"ágio"' --ano 2023

# Texto integral de um ato pelo idAto (consolidado atual)
python3 scripts/sijut2.py texto --id 123456 --visao compilado

# Ver o histórico de alterações de um ato
python3 scripts/sijut2.py texto --id 123456 --visao anotado

# Em caso de layout alterado, inspecionar o HTML bruto
python3 scripts/sijut2.py buscar --tipo 59 --termo teste --raw
```

O fluxo típico é **`buscar` → pegar o `idAto` do ato certo → `texto --id <idAto>`**
para ler o teor e conferir a vigência.

### Cuidados de rede e etiqueta
- O script respeita `HTTPS_PROXY` e o bundle de CA em `REQUESTS_CA_BUNDLE`/
  `SSL_CERT_FILE` (ambientes com proxy corporativo, como o Claude Code na web).
- Se o retorno for **403/407 ou falha de túnel**, o domínio da Receita está
  **bloqueado pela política de egresso do ambiente** — não é bug: rode de um
  ambiente com acesso liberado, ou faça a consulta manualmente no navegador com
  a URL do subcomando `url`. **Nunca** desabilite verificação de TLS nem tente
  contornar a política.
- Raspe com moderação: uma requisição por vez, sem paralelismo agressivo. O
  `User-Agent` do script é identificável de propósito.

---

## Passo 4 — Conferir a vigência (barreira nº 2)

Encontrar o ato não basta — é preciso saber se **vale hoje** e em que redação.

1. Abra o ato em `visao=compilado` e verifique a **situação** exibida
   (vigente, revogado, alterado). Um ato revogado citado como vigente é erro
   grave.
2. Se a tese depende da redação de um dispositivo específico, use
   `visao=anotado` para ver **qual redação valia na data do fato gerador** —
   norma tributária aplica-se conforme a vigência à época do fato, não à data de
   hoje.
3. Verifique se há **ato posterior** que altere ou revogue (busque pelo número/
   tema; o cabeçalho do ato compilado costuma indicar as alterações).
4. Para Solução de Consulta: confirme se não foi **reformada por Solução de
   Divergência** ou superada por SC COSIT posterior.

Registre no trabalho a **data da consulta** e a visão utilizada.

## Passo 5 — Citar de forma rastreável

Toda referência a norma deve permitir que o leitor a localize e confira. Padrão
mínimo:

> **Tipo + número + órgão + data** — *ementa/objeto resumido* — **situação
> (vigente/revogado)** — *fonte: SIJUT2, idAto=NNN* (data da consulta).

Exemplos:
- "Parecer Normativo COSIT nº 1, de 11/10/2018 (vigente) — [tese] — SIJUT2,
  idAto=98765, consultado em 28/07/2026."
- "Solução de Consulta COSIT nº 100, de DD/MM/AAAA — [entendimento] — verificar
  eventual reforma por SD."

Nunca cite apenas "a IN da Receita" ou "o parecer normativo" sem número, órgão,
data e fonte. Se um desses dados não foi confirmado, marque-o como "a confirmar".

---

## Fluxos por âmbito

**Âmbito administrativo (defesa/impugnação, consulta fiscal, recurso ao CARF):**
1. Localize no SIJUT2 os atos da RFB aplicáveis (IN, ADI, PN, SC COSIT) — eles
   **vinculam a fiscalização**.
2. Se a autuação contraria a própria norma/SC da RFB, isso é fundamento central.
3. Complemente com **súmulas e acórdãos do CARF** (fonte própria, fora do SIJUT2).
4. Confira vigência à data do fato gerador (Passo 4).

**Âmbito judicial:**
1. Ancore a tese de mérito em **lei/LC + jurisprudência** (STF/STJ, temas
   repetitivos, súmulas) — o ato infralegal não vincula o juiz.
2. Use os atos do SIJUT2 para (a) demonstrar o entendimento do fisco, (b) atacar
   autuação que contraria a própria norma da RFB, ou (c) sustentar boa-fé/
   legítima expectativa do contribuinte.
3. Cite lei e jurisprudência pela fonte própria; cite atos da RFB pelo SIJUT2.

## Padrão de saída

Ao responder uma consulta tributária, entregue:
- **Resposta objetiva** à pergunta.
- **Fundamentos normativos** citados no padrão rastreável (Passo 5), com vigência
  conferida e `idAto`/URL.
- **Distinção de âmbito** quando relevante (o que vincula a administração vs. o
  que pesa no Judiciário).
- **Ressalvas explícitas** para tudo que não foi confirmado na fonte primária
  nesta consulta ("a verificar", "não localizado no SIJUT2").

## Armadilhas frequentes (não cometer)
- Alucinar número/data/ementa de IN ou PN a partir da memória — **sempre** o
  SIJUT2 confirma.
- Tratar Solução de Consulta como se vinculasse terceiros que não o consulente.
- Citar redação revogada como vigente (esqueceu de conferir a `visao`).
- Aplicar a redação atual a um fato gerador antigo (ignorar a vigência à época).
- Usar SIJUT2 para buscar lei (é do Planalto) ou jurisprudência judicial (é dos
  tribunais).
- Apresentar resultado de agregador (JusBrasil etc.) como fonte primária.
