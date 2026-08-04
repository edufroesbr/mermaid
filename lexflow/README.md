# lexflow — governança e alinhamento dos agentes jurídicos

Fonte única de verdade para manter **todos os agentes, subagentes e
orquestradores** (Claude Code, Cursor, Antigravity/Gemini) alinhados nas
entregas jurídicas — com anti-alucinação, rotas de verificação corretas e um
padrão de qualidade comum.

```
lexflow/
├── PADRAO-ENTREGA-JURIDICA.md      # O padrão. Todo agente deve referenciá-lo.
└── tools/
    └── auditar-agentes.ps1         # Varre .claude/.cursor/.gemini e aponta desalinhados
```

## Uso

1. **Ler o padrão:** `PADRAO-ENTREGA-JURIDICA.md` — regra anti-alucinação, rotas
   de verificação por tipo de fonte, estrutura mínima por peça e o checklist de
   certificação obrigatório antes de qualquer entrega.

2. **Auditar o alinhamento** (rode na sua máquina, apontando para a raiz do
   projeto que contém `.claude`, `.cursor` e/ou `.gemini`):

   ```powershell
   powershell -ExecutionPolicy Bypass -File lexflow\tools\auditar-agentes.ps1 -Root "C:\Users\edufr\.gemini\antigravity-ide\scratch\Lex_Flow"
   ```

   O relatório marca cada agente como **OK** (referencia o padrão),
   **DESALINHADO** (não referencia) ou **DUPLICADO** (mesma função em mais de uma
   ferramenta).

3. **Alinhar:** inserir em cada agente desalinhado o cabeçalho da seção 5.3 do
   padrão e consolidar os duplicados nesta pasta canônica.

## Relação com as demais entregas

- `tributario/` — skill `consulta-normas-tributarias` + agente
  `consultor-tributario` (uma das rotas de verificação exigidas pelo padrão).
- A skill `relatorio-processual-verificado` (autos) é a rota para fatos de
  processo citada no padrão.

> A pasta canônica idealmente deve ser **única** (ver decisão pendente no
> histórico): consolidar `tributario/` + agentes das três ferramentas sob
> `lexflow/` evita as versões conflitantes que causam falha de entrega.
