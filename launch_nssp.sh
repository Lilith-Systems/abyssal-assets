#!/bin/bash
# NSSP Full Stack Launcher — MSN Router + Game + Lyra + Hermes + CP Telemetry
set -e

PUB_ROOT="${PUB_ROOT:-$HOME/Desktop/AI/Pub}"
VENV="$PUB_ROOT/.venv-pub"
ABYSSAL="$HOME/Desktop/AI/abyssal-assets"
INVITE="$HOME/Desktop/AI/invite"

echo "=========================================="
echo " NSSP FULL STACK LAUNCHER"
echo "=========================================="

# Kill existing
echo "[Cleanup] Stopping existing services..."
for port in 8000 8007 3211 4242 8768; do
    pid=$(lsof -ti :$port 2>/dev/null) && kill $pid 2>/dev/null && echo "  Freed port $port"
done
sleep 1

# Start MSN Router (28 agents, port 8007)
echo "[1/4] MSN Router (28 agents, port 8007)..."
source "$VENV/bin/activate"
nohup python "$ABYSSAL/msn_router.py" 8007 > /tmp/msn_router.log 2>&1 &
echo "  PID $!"

# Start Game Server (port 8000)
echo "[2/4] Abyssal Assets Game Server (port 8000)..."
nohup python "$ABYSSAL/server/main.py" > /tmp/abyssal_game.log 2>&1 &
echo "  PID $!"

# Wait for MSN
echo "[Wait] Waiting for MSN Router..."
for i in $(seq 1 15); do
    if curl -sf http://localhost:8007/api >/dev/null 2>&1; then
        echo "  MSN Router ready"
        break
    fi
    sleep 1
done

# Start MSN Coordination (port 8768)
echo "[3/4] MSN Coordination Server (port 8768)..."
nohup "$VENV/bin/python" \
    "$HOME/.local/share/Steam/steamapps/common/Cyberpunk 2077/r6/mods/msn_integration/msn_coordination_server.py" \
    > /tmp/msn_coordination.log 2>&1 &
echo "  PID $!"

# Verify agents
echo "[4/4] Verifying deployment..."
source "$VENV/bin/activate"
python "$ABYSSAL/deploy_waves.py" 8007 2>&1 | head -5

echo ""
echo "=========================================="
echo " NSSP STACK READY"
echo "=========================================="
echo " MSN Router:   http://localhost:8007  (28 agents)"
echo " Game Server:  http://localhost:8000"
echo " Lyra:         http://localhost:3211"
echo " Hermes:       http://localhost:4242"
echo " MSN Coord:    ws://localhost:8768"
echo ""
echo " NSSP API:     http://localhost:8007/api/nssp"
echo "  - /nssp/status, /nssp/roast, /nssp/sovereignty"
echo "  - /nssp/nessie/status, /nssp/nessie/sighting"
echo "  - /nssp/abyssal/status, /nssp/bridge/telemetry"
echo "  - /nssp/integration (full system health)"
echo ""
echo " To play: steam steam://rungameid/1091500"
echo "=========================================="
