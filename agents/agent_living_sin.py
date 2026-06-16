# Wave 2 — Hod: Living Sin GM

from agents import SubAgent, AgentManifest, register_agent

manifest = AgentManifest(
    id="living-sin",
    name="Living Sin GM",
    version="2.0.0",
    sephira="HOD",
    description="Game Master system — biometric keystroke auth, 10-plane summoning, boss combat, Crown of Living Sin",
    wave=2,
)


class LivingSinAgent(SubAgent):
    def _register_routes(self):
        super()._register_routes()

        @self.router.get("/status")
        async def gm_status():
            from game_master import get_living_sin
            return get_living_sin().get_state()

        @self.router.get("/bosses")
        async def active_bosses():
            from game_master import get_living_sin
            return {"active_bosses": get_living_sin().combat.list_active()}

        @self.router.get("/dimensions")
        async def dimensions():
            from game_master import DIMENSIONS
            return DIMENSIONS

        @self.router.get("/biometric/status")
        async def bio_status():
            from game_master import get_biometric
            bio = get_biometric()
            return {"enrolled": bio.is_enrolled(), "samples": len(bio.profiles)}


agent = LivingSinAgent(manifest)
register_agent(agent)
