<#
.SYNOPSIS
  Audita agentes/skills/rules nas pastas .claude, .cursor e .gemini de um projeto
  e aponta quem está DESALINHADO com o Padrão de Entrega Jurídica LexFlow.

.DESCRIPTION
  Varre, sob -Root, os locais onde cada ferramenta guarda instruções de agente:
    .claude\agents\*.md, .claude\skills\*\SKILL.md, .claude\CLAUDE.md
    .cursor\rules\*.mdc, .cursorrules
    .gemini\**  (GEMINI.md e configs), AGENTS.md
  Para cada arquivo, verifica se referencia o padrão (marcador
  'PADRAO-ENTREGA-JURIDICA' ou a frase do cabeçalho) e detecta possíveis
  duplicatas de função pelo nome. Não altera nada — só relata.

.PARAMETER Root
  Raiz do projeto (a pasta que contém .claude, .cursor e/ou .gemini).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File auditar-agentes.ps1 -Root "C:\Users\edufr\.gemini\antigravity-ide\scratch\Lex_Flow"
#>
param(
  [Parameter(Mandatory = $true)][string]$Root
)
$ErrorActionPreference = "Stop"

if (-not (Test-Path $Root)) { throw "Raiz nao encontrada: $Root" }

$MARCADOR = "PADRAO-ENTREGA-JURIDICA"          # referencia canonica ao padrao
$FRASE    = "Padr.o de Entrega Jur.dica LexFlow"  # regex tolerante a acento

# Locais conhecidos por ferramenta (glob relativo a -Root)
$alvos = @(
  @{ Ferramenta = "claude"; Glob = ".claude\agents\*.md" },
  @{ Ferramenta = "claude"; Glob = ".claude\skills\*\SKILL.md" },
  @{ Ferramenta = "claude"; Glob = ".claude\CLAUDE.md" },
  @{ Ferramenta = "claude"; Glob = "CLAUDE.md" },
  @{ Ferramenta = "cursor"; Glob = ".cursor\rules\*.mdc" },
  @{ Ferramenta = "cursor"; Glob = ".cursor\rules\*.md" },
  @{ Ferramenta = "cursor"; Glob = ".cursorrules" },
  @{ Ferramenta = "gemini"; Glob = ".gemini\**\*.md" },
  @{ Ferramenta = "gemini"; Glob = "GEMINI.md" },
  @{ Ferramenta = "gemini"; Glob = ".gemini\**\*.json" },
  @{ Ferramenta = "geral";  Glob = "AGENTS.md" }
)

$achados = @()
foreach ($a in $alvos) {
  $full = Join-Path $Root $a.Glob
  Get-ChildItem -Path $full -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $txt = Get-Content -Raw -ErrorAction SilentlyContinue $_.FullName
    $alinhado = ($txt -match $MARCADOR) -or ($txt -match $FRASE)
    $achados += [pscustomobject]@{
      Ferramenta = $a.Ferramenta
      Nome       = $_.BaseName
      Arquivo    = $_.FullName.Substring($Root.Length).TrimStart('\')
      Alinhado   = $alinhado
    }
  }
}

if ($achados.Count -eq 0) {
  Write-Host "Nenhum arquivo de agente/skill/rule encontrado sob $Root" -ForegroundColor Yellow
  Write-Host "Confira se .claude / .cursor / .gemini existem nessa raiz."
  return
}

# Duplicatas: mesmo Nome em mais de uma ferramenta
$dupNomes = $achados | Group-Object Nome | Where-Object { ($_.Group.Ferramenta | Sort-Object -Unique).Count -gt 1 } | ForEach-Object { $_.Name }

Write-Host ""
Write-Host "===== AUDITORIA DE ALINHAMENTO — LexFlow =====" -ForegroundColor Cyan
Write-Host "Raiz: $Root`n"

foreach ($f in $achados | Sort-Object Ferramenta, Nome) {
  $status = if ($f.Alinhado) { "OK  " } else { "DESALINHADO" }
  $cor    = if ($f.Alinhado) { "Green" } else { "Red" }
  $dup    = if ($dupNomes -contains $f.Nome) { "  [DUPLICADO]" } else { "" }
  Write-Host ("[{0,-11}] {1,-8} {2}{3}" -f $status, $f.Ferramenta, $f.Arquivo, $dup) -ForegroundColor $cor
}

$total   = $achados.Count
$ok      = ($achados | Where-Object Alinhado).Count
$desal   = $total - $ok
Write-Host ""
Write-Host "----- Resumo -----"
Write-Host ("Total de itens : {0}" -f $total)
Write-Host ("Alinhados      : {0}" -f $ok)        -ForegroundColor Green
Write-Host ("Desalinhados   : {0}" -f $desal)     -ForegroundColor $(if ($desal) {"Red"} else {"Green"})
Write-Host ("Duplicados     : {0}" -f $dupNomes.Count) -ForegroundColor $(if ($dupNomes.Count) {"Yellow"} else {"Green"})
if ($desal -gt 0 -or $dupNomes.Count -gt 0) {
  Write-Host "`nAcao: inserir o cabecalho do padrao (secao 5.3) nos DESALINHADOS e" -ForegroundColor Yellow
  Write-Host "consolidar os DUPLICADOS na pasta canonica lexflow\." -ForegroundColor Yellow
}
