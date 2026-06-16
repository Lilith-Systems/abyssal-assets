# Abyssal Assets — The Loch Exchange

A multiplayer cryptid hat trading simulator built on FastAPI + Phaser 3.

## Current State
- **Server**: 852-line FastAPI app with 7 DB models, auth, WebSocket, CLOB routes
- **Client**: Phaser 3/TypeScript with market CLOB (1539 lines) and dredge mini-game (838 lines)
- **Monsters**: 7 tiers defined in TypeScript, 6 fully specified (Loch Minnow → Lilith True Form)
- **Skills**: 24 skills across 6 categories, XP curves, synergies — all typed
- **GDD**: 583-line game design document — 12 Acts, skill web, drop tables, bestiary

## What's Needed
1. **Database alive** — run `python server/main.py` to create SQLite + seed 17 hats
2. **Monster farming** — implement hunting/combat, wire drop tables to inventory
3. **Dredge → Craft → Trade loop** — connect mini-game to crafting recipes to market
4. **Boss fights** — Kraken Matriarch, Nessie, Lilith as world events
5. **Linux conversion items** — no bat/ps1 here, but server needs env vars extracted

## Key Commands
```bash
# Start server
cd server && python main.py

# Start client
cd client && npm run dev

# Full stack
# Terminal 1: python server/main.py (port 8000)
# Terminal 2: npm run dev --prefix client (port 3000)
```

## Environment
- System: Garuda Linux (Arch-based), RTX 3060 6GB, 62GB RAM
- Python: 3.14, venv at ~/Desktop/AI/Pub/.venv-pub/ (198 packages)
- Ollama: nemotron-mini (4.2B) for local inference
- Lyra: dialogue server at localhost:3211
