# Padrão de Entrega Jurídica — LexFlow (fonte única de alinhamento)

> **Este arquivo é a fonte única de verdade para a qualidade das entregas
> jurídicas.** Todo agente, subagente e orquestrador — em qualquer ferramenta
> (Claude Code, Cursor, Antigravity/Gemini) — DEVE referenciar e obedecer este
> padrão ao produzir petições, pareceres, contratos, contestações, recursos,
> relatórios ou qualquer conteúdo jurídico. Um agente que não referencia este
> arquivo está **desalinhado** e deve ser corrigido (ver `tools/auditar-agentes`).

Uso interno Advocacia Vale de Oliva / AAGE / LexFlow.

---

## 0. Por que existe

Entregas jurídicas embasam atos com efeito real: uma petição protocolada, um
prazo, uma tese sustentada em juízo, um valor cobrado. As falhas recorrentes das
LLMs em conteúdo jurídico têm causa conhecida:

1. **Alucinação normativa/jurisprudencial** — inventar número de lei, ementa,
   tema repetitivo, súmula ou dispositivo que não existe ou não diz aquilo.
2. **Desalinhamento entre agentes** — Cursor, Gemini e Claude com instruções
   diferentes e conflitantes, produzindo padrões incompatíveis para a mesma peça.
3. **Rota de verificação errada** — buscar norma no lugar errado (ou não buscar),
   citar agregador (JusBrasil) como fonte primária, usar redação revogada.

Este padrão elimina as três. É de cumprimento **obrigatório**, não sugestão.

---

## 1. Regra nº 1 — Zero alucinação factual e normativa

**Nunca** afirme, a partir da memória do modelo, qualquer um destes dados:
número/data/ementa de norma, número de lei/artigo, súmula, tema repetitivo,
número de acórdão, valor, prazo, data, nome de parte ou identificador de
processo. Modelos alucinam esses dados com altíssima confiança.

Toda afirmação desse tipo deve ser **verificada na fonte primária no momento da
redação** e **citada com a fonte**. O que não puder ser verificado agora recebe
o marcador literal **`[A CONFERIR]`** no texto — nunca é preenchido com o que
"provavelmente" é.

> Regra de ouro: uma citação marcada `[A CONFERIR]` é honesta e recuperável.
> Uma citação alucinada apresentada como certa é um erro que derruba a peça e
> expõe o cliente e o escritório. Na dúvida, marque `[A CONFERIR]`.

---

## 2. Rotas corretas de verificação (por tipo de fonte)

Cada tipo de fonte tem **uma rota certa**. Usar a rota errada é a causa nº 1 de
citação inválida. Use sempre:

| Preciso de… | Rota correta | Ferramenta / skill |
|---|---|---|
| Norma infralegal da RFB (IN, ADI, ADE, Parecer Normativo, Solução de Consulta/Divergência) | SIJUT2 (Receita Federal) | skill **`consulta-normas-tributarias`** / `sijut2.py` |
| Lei, Lei Complementar, Decreto, MP | Planalto (planalto.gov.br) / DOU (in.gov.br) | fonte oficial — nunca de memória |
| Jurisprudência judicial (repetitivos, temas, súmulas) | STF, STJ, TRFs (portais oficiais) | portais dos tribunais; agregador só como *apoio*, nunca fonte única |
| Contencioso administrativo federal (acórdãos/súmulas CARF) | CARF (gov.br/carf) | fonte oficial |
| Fatos de um processo (datas, valores, IDs, peças) | Autos, na fonte primária | skill **`relatorio-processual-verificado`** (identificador nativo do sistema) |
| Tributo estadual/municipal | Legislação/atos do ente (SEFAZ) | fonte oficial |

Proibições:
- ❌ Citar JusBrasil/agregador como se fosse a fonte primária.
- ❌ Usar SIJUT2 para buscar lei (é do Planalto) ou jurisprudência (é dos tribunais).
- ❌ Aplicar a redação atual de uma norma a um fato gerador antigo (vale a redação
  vigente à época do fato).

---

## 3. Rotas de entrega por tipo de peça

Cada peça tem estrutura mínima e requisitos próprios. Não entregue peça sem
conferir os itens da sua linha.

| Peça | Estrutura mínima | Requisitos que NÃO podem faltar |
|---|---|---|
| **Petição inicial** | Endereçamento · qualificação das partes · fatos · fundamentos jurídicos · pedidos · valor da causa · provas | Competência conferida; pedido certo e determinado; fundamentos com norma/jurisprudência verificadas; valor da causa coerente |
| **Contestação** | Preliminares · mérito · impugnação específica dos fatos · pedidos | Ônus da impugnação específica (art. 341 CPC — [A CONFERIR] no caso); prazo conferido nos autos |
| **Recurso** | Cabimento · tempestividade · preparo · razões · pedido | Prazo e tempestividade conferidos; requisitos de admissibilidade; prequestionamento quando exigível |
| **Parecer** | Consulta · premissas · análise · conclusão objetiva · ressalvas | Todas as premissas normativas verificadas; ressalvas explícitas para o não confirmado |
| **Contrato** | Partes · objeto · obrigações · preço · prazo · rescisão · foro | Cláusulas coerentes entre si; sem lacuna remissiva a cláusula inexistente |
| **Relatório/dossiê processual** | Ver skill `relatorio-processual-verificado` | Cada fato rastreável ao identificador nativo dos autos |

Para toda peça: linguagem jurídica correta e objetiva, sem "encheção" retórica,
sem afirmação sem lastro, e com cada fundamento rastreável à sua fonte.

---

## 4. Certificação anti-alucinação (checklist obrigatório antes de entregar)

Antes de considerar QUALQUER entrega jurídica pronta, o agente confirma, item a
item. Se algum item falhar, corrige ou marca `[A CONFERIR]` — não entrega assim.

- [ ] **Normas** — toda norma citada foi *aberta e conferida* na rota correta
      (número, órgão, data, vigência e redação aplicável à época do fato)?
- [ ] **Jurisprudência** — todo acórdão/súmula/tema citado *existe* e *diz* o que
      afirmo? (ementa/tese conferidas na fonte oficial)
- [ ] **Fatos** — todo valor, prazo, data e nome foi *extraído da fonte*, não
      estimado de memória?
- [ ] **Processo** — toda referência a autos usa o *identificador nativo* correto
      do sistema (PJe/PROJUDI/e-SAJ/Eproc)?
- [ ] **Pedidos/prazos** — pedido certo e determinado; prazos conferidos?
- [ ] **Lastro** — não há nenhuma afirmação sem fonte? (varredura final: cada
      frase de conteúdo tem origem verificável ou marcador `[A CONFERIR]`)
- [ ] **Coerência** — a peça não se contradiz nem remete a item inexistente?

Ao final, o agente declara ao usuário o **grau de verificação**: o que foi
conferido na fonte e o que restou `[A CONFERIR]`. Entrega sem essa declaração é
entrega incompleta.

---

## 5. Governança de agentes — regra de alinhamento (pasta única)

Para eliminar o desalinhamento entre ferramentas:

1. **Fonte única.** A pasta canônica (`lexflow/`) é a única fonte de verdade de
   agentes e skills. Nada de agente "solto" criado direto no `.cursor`, `.gemini`
   ou `.claude` — isso gera as versões conflitantes que causam a falha.
2. **Um agente por função.** Não pode haver dois agentes com a mesma função e
   instruções divergentes em ferramentas diferentes. Um só, canônico, distribuído.
3. **Cabeçalho obrigatório.** Todo agente/skill deve conter, no topo, a linha:
   > *Segue o Padrão de Entrega Jurídica LexFlow — ver `PADRAO-ENTREGA-JURIDICA.md`.*
   A ausência dessa linha é o critério objetivo de "desalinhado".
4. **Fluxo de mudança.** Criar/editar agente ou skill acontece **só na pasta
   canônica**; depois um passo de distribuição copia para o local que cada
   ferramenta espera (`.claude/agents`, `.claude/skills`, `.cursor/rules`,
   `GEMINI.md`/config do Antigravity). Nunca o contrário.
5. **Auditoria periódica.** Rodar `tools/auditar-agentes` para listar todo agente
   nas três pastas e apontar os que não referenciam este padrão.

---

## 6. Como auditar e alinhar

```bash
# Windows (PowerShell) — varre .claude, .cursor e .gemini sob a raiz do projeto
powershell -ExecutionPolicy Bypass -File lexflow\tools\auditar-agentes.ps1 -Root "C:\Users\edufr\.gemini\antigravity-ide\scratch\Lex_Flow"
```

O relatório lista cada agente/skill/rule encontrado e marca:
- ✅ **alinhado** — referencia este padrão;
- ⚠️ **desalinhado** — não referencia (precisa de cabeçalho + revisão);
- 🔁 **duplicado** — mesma função em mais de uma ferramenta (consolidar na pasta única).

A partir do relatório, corrige-se cada agente desalinhado (inserindo o cabeçalho
da seção 5.3 e ajustando as instruções a este padrão) e consolida-se os
duplicados na pasta canônica.
