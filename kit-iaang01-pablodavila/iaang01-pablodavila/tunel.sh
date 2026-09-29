#!/usr/bin/env bash
# Abre el túnel a tu base de datos y lo deja corriendo.
#
# Para qué sirve: tu base NO está abierta a internet, a propósito. Este script
# crea un paso seguro entre tu computadora y ella, usando tu llave .hatch_key.
# Mientras esté corriendo, tu agente puede conectarse como si la base fuera
# local, en 127.0.0.1:15432.
#
# Úsalo así:
#   1. Abre una terminal, corre  ./tunel.sh  y DÉJALA ABIERTA.
#   2. En otra terminal trabaja normal. Tu código usa DATABASE_URL_LOCAL.
#
# Para cerrarlo: Ctrl+C en la ventana del túnel.
set -euo pipefail
cd "$(dirname "$0")"
chmod 600 .hatch_key 2>/dev/null || true

echo "Abriendo el túnel a tu base de datos…"
echo "  Deja esta ventana abierta mientras trabajes."
echo "  Tu base queda en:  127.0.0.1:15432   (usa DATABASE_URL_LOCAL)"
echo "  Para cerrar: Ctrl+C"
echo
# Se conecta a la IP y no a hatchvps.com a propósito: el dominio resuelve a
# Cloudflare, que solo deja pasar tráfico web. El SSH tiene que ir al servidor
# directo, igual que hace deploy.sh.

exec ssh -N \
  -o StrictHostKeyChecking=accept-new \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -i .hatch_key \
  -L 15432:127.0.0.1:56432 \
  iaang01-pablodavila@72.60.168.10
