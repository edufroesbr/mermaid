<#
.SYNOPSIS
  Instala a skill 'consulta-normas-tributarias' e o agente 'consultor-tributario'
  numa pasta .claude (skills + agents).

.DESCRIPTION
  Copia os arquivos versionados em tributario/ para <ClaudeDir>\skills e
  <ClaudeDir>\agents. Rode a partir de um clone deste repositório.

.PARAMETER ClaudeDir
  Pasta .claude de destino. Padrão: o LexFlow no Antigravity IDE do usuário.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tributario\install.ps1
  powershell -ExecutionPolicy Bypass -File tributario\install.ps1 -ClaudeDir "D:\outro\.claude"
#>
param(
  [string]$ClaudeDir = "$env:USERPROFILE\.gemini\antigravity-ide\scratch\Lex_Flow\.claude"
)
$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $MyInvocation.MyCommand.Path   # .../tributario

New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir "skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ClaudeDir "agents") | Out-Null

Copy-Item -Recurse -Force `
  (Join-Path $src "skills\consulta-normas-tributarias") `
  (Join-Path $ClaudeDir "skills\")

Copy-Item -Force `
  (Join-Path $src "agents\consultor-tributario.md") `
  (Join-Path $ClaudeDir "agents\")

Write-Host "OK: skill e agente instalados em $ClaudeDir" -ForegroundColor Green
Write-Host "  skills\consulta-normas-tributarias\  (SKILL.md + scripts\sijut2.py)"
Write-Host "  agents\consultor-tributario.md"
