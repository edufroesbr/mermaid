# Tributário — Skill + Agente especializados em normas tributárias

Ferramentas de **consulta e busca de normas e entendimentos tributários
federais** (Receita Federal / SIJUT2), para uso em matéria tributária
especializada, âmbito **administrativo** e **judicial**.

Contém:

```
tributario/
├── skills/consulta-normas-tributarias/
│   ├── SKILL.md                     # metodologia + referência de acesso ao SIJUT2
│   └── scripts/sijut2.py            # cliente/raspador do SIJUT2 (CLI)
└── agents/consultor-tributario.md   # subagente que faz a pesquisa e retorna citações verificadas
```

## O que faz

- **Skill `consulta-normas-tributarias`** — aciona automaticamente sempre que a
  tarefa envolver matéria tributária especializada e for preciso consultar,
  citar ou conferir a vigência de norma da RFB (IN, ADI, ADE, Parecer Normativo,
  Solução de Consulta/Divergência COSIT/DISIT etc.). Documenta os endpoints do
  SIJUT2, as regras de citação rastreável e a conferência de vigência.
- **Agente `consultor-tributario`** — subagente para o qual o Claude delega a
  pesquisa normativa tributária, devolvendo citações verificadas na fonte
  primária (com `idAto`/URL e vigência conferida), separando o que vincula a
  administração do que pesa no Judiciário.
- **Script `sijut2.py`** — cliente de linha de comando para o SIJUT2 (não há API
  JSON oficial; o SIJUT2 é HTML renderizado no servidor).

## Instalação (uso global no Claude Code)

Copie a skill e o agente para as pastas do usuário do Claude Code:

```bash
# a partir da raiz do repositório
cp -r tributario/skills/consulta-normas-tributarias ~/.claude/skills/
mkdir -p ~/.claude/agents
cp tributario/agents/consultor-tributario.md ~/.claude/agents/
```

A skill passa a ser reconhecida pelo mecanismo de skills; o agente fica
disponível como `subagent_type: consultor-tributario`.

> Observação: neste repositório o diretório `/.claude/` está no `.gitignore`, por
> isso a cópia canônica versionada fica em `tributario/`. As pastas `~/.claude/`
> não são versionadas — reinstale a partir de `tributario/` quando trocar de
> máquina/ambiente.

### Instaladores prontos

A partir de um clone deste repositório:

```bash
# Linux/macOS — instala em ~/.claude (ou passe outra pasta)
bash tributario/install.sh
bash tributario/install.sh /caminho/para/.claude
```

```powershell
# Windows (PowerShell) — por padrão instala no LexFlow do Antigravity IDE
powershell -ExecutionPolicy Bypass -File tributario\install.ps1
powershell -ExecutionPolicy Bypass -File tributario\install.ps1 -ClaudeDir "D:\outro\.claude"
```

### Instalar no LexFlow (Windows) sem clonar o repo

Cola no PowerShell — clona a branch num temporário, copia para o `.claude` do
LexFlow e limpa:

```powershell
$Lex = "C:\Users\edufr\.gemini\antigravity-ide\scratch\Lex_Flow\.claude"
$tmp = Join-Path $env:TEMP "mermaid-trib"
if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
git clone --depth 1 -b claude/tax-norms-specialized-agent-a5i7ay https://github.com/edufroesbr/mermaid.git $tmp
New-Item -ItemType Directory -Force -Path "$Lex\skills","$Lex\agents" | Out-Null
Copy-Item -Recurse -Force "$tmp\tributario\skills\consulta-normas-tributarias" "$Lex\skills\"
Copy-Item -Force "$tmp\tributario\agents\consultor-tributario.md" "$Lex\agents\"
Remove-Item -Recurse -Force $tmp
Write-Host "OK: skill + agente instalados em $Lex"
```

## Uso do script

```bash
cd tributario/skills/consulta-normas-tributarias/scripts

# Códigos de tipo de ato (ex.: 59 = Parecer Normativo/PN)
python3 sijut2.py tipos

# Só montar a URL de busca (funciona OFFLINE — cole no navegador)
python3 sijut2.py url --tipo 59 --termo '"crédito presumido"' --ano 2024

# Buscar atos (lista idAto + título)
python3 sijut2.py buscar --tipo 59 --termo '"ágio"' --ano 2023

# Ler o texto integral consolidado de um ato
python3 sijut2.py texto --id 123456 --visao compilado
```

Requer Python 3 e `requests` (`pip install requests`).

## Acesso à rede / proxy

O script respeita `HTTPS_PROXY` e o bundle de CA (`REQUESTS_CA_BUNDLE` /
`SSL_CERT_FILE`). Se o domínio `normas.receita.fazenda.gov.br` retornar
**403/407 ou falha de túnel**, ele está **bloqueado pela política de egresso do
ambiente** (é o caso, por exemplo, de algumas sessões do Claude Code na web) —
não é bug. Rode de um ambiente com acesso liberado ou use o subcomando `url`
para consultar manualmente no navegador. Nunca desabilite a verificação de TLS.
