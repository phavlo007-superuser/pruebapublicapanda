#!/usr/bin/env bash
# Publica este proyecto en hatchvps.  Uso:  ./deploy.sh  [carpeta]
set -euo pipefail
BASEDIR="$(cd "$(dirname "$0")" && pwd)"
USUARIO="iaang01-pablodavila"
HOST="72.60.168.10"
KEY="$BASEDIR/.hatch_key"
SRC="${1:-$BASEDIR}"
[ -f "$KEY" ] || { echo "Falta la llave .hatch_key (venía en tu kit)."; exit 1; }
chmod 600 "$KEY" 2>/dev/null || true
IGN='(^|/)(\.git|node_modules|venv|__pycache__)(/|$)'
cd "$SRC"
BATCH="$(mktemp)"
find . -mindepth 1 -type d | sed 's#^\./##' | { grep -vE "$IGN" || true; } \
  | while read -r d; do echo "-mkdir \"$d\""; done >> "$BATCH"
find . -type f | sed 's#^\./##' | { grep -vE "$IGN" || true; } \
  | while read -r f; do
      # Lo que solo sirve en la laptop no se sube: la llave (nunca), las
      # instrucciones del agente y el script del túnel. El .env SÍ se sube:
      # sin él la app desplegada no sabe conectarse a la base.
      case "$f" in .hatch_key|.hatch_key.pub|deploy.sh|tunel.sh|CLAUDE.md|AGENTS.md|LEEME.md|CREDENCIALES.txt|.DS_Store) continue;; esac
      echo "put \"$f\" \"$f\""
    done >> "$BATCH"
echo ">> Publicando '$SRC' ..."
sftp -i "$KEY" -o StrictHostKeyChecking=accept-new -b "$BATCH" "$USUARIO@$HOST" >/dev/null
rm -f "$BATCH"
echo ">> Listo -> https://hatchvps.com/iaang01/pablodavila/"
