#!/usr/bin/env bash
# Instala a skill 'consulta-normas-tributarias' e o agente 'consultor-tributario'
# numa pasta .claude (skills + agents). Rode a partir de um clone deste repositório.
#
# Uso:
#   bash tributario/install.sh                 # instala em ~/.claude
#   bash tributario/install.sh /caminho/.claude
set -euo pipefail
CLAUDE_DIR="${1:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../tributario

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"
cp -r "$SRC/skills/consulta-normas-tributarias" "$CLAUDE_DIR/skills/"
cp "$SRC/agents/consultor-tributario.md" "$CLAUDE_DIR/agents/"

echo "OK: skill e agente instalados em $CLAUDE_DIR"
echo "  skills/consulta-normas-tributarias/  (SKILL.md + scripts/sijut2.py)"
echo "  agents/consultor-tributario.md"
