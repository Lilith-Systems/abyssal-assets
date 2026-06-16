# Wave 2 — Gevurah: Bestiary / Monsters

from agents import SubAgent, AgentManifest, register_agent

manifest = AgentManifest(
    id="bestiary",
    name="Cryptid Bestiary",
    version="1.0.0",
    sephira="GEVURAH",
    description="Monster definitions — 7 tiers, 6 fully defined cryptids, drop tables, AI mechanics",
    wave=2,
)


class BestiaryAgent(SubAgent):
    def _register_routes(self):
        super()._register_routes()

        @self.router.get("/monsters")
        async def list_monsters():
            from pathlib import Path
            import importlib.util
            monsters_path = Path(__file__).parent.parent / "shared" / "types" / "monsters.ts"
            return {"path": str(monsters_path), "exists": monsters_path.exists(), "size": monsters_path.stat().st_size if monsters_path.exists() else 0}

        @self.router.get("/bosses")
        async def list_bosses():
            from game_master import BOSS_DEFINITIONS
            return {"bosses": list(BOSS_DEFINITIONS.keys()), "definitions": BOSS_DEFINITIONS}

        @self.router.get("/tiers")
        async def get_tiers():
            return {
                "tiers": ["noob", "common", "uncommon", "rare", "epic", "legendary", "mythic"],
                "count": 7,
            }


agent = BestiaryAgent(manifest)
register_agent(agent)
