# Wave 1 — Binah: Game Server

from agents import SubAgent, AgentManifest, register_agent

manifest = AgentManifest(
    id="server",
    name="Game Server",
    version="1.0.0",
    sephira="BINAH",
    description="FastAPI game server — 7 DB models, auth, WebSocket, CLOB, dredge, Living Sin GM, boss combat",
    wave=1,
)


class ServerAgent(SubAgent):
    def _register_routes(self):
        super()._register_routes()

        @self.router.get("/routes")
        async def list_routes():
            import sys
            sys.path.insert(0, str(self._server_dir()))
            from main import app
            routes = []
            for r in app.routes:
                if hasattr(r, "path") and hasattr(r, "methods"):
                    for m in r.methods:
                        routes.append({"method": m, "path": r.path})
            return {"routes": routes, "count": len(routes)}

        @self.router.get("/models")
        async def list_models():
            return {
                "models": ["User", "Hat", "InventoryItem", "Order", "MarketListing", "Trade", "DredgeLog"],
                "count": 7,
            }

        @self.router.get("/gm/status")
        async def gm_status():
            from game_master import get_living_sin
            ls = get_living_sin()
            return ls.get_state()

    def _server_dir(self):
        import pathlib
        return pathlib.Path(__file__).parent.parent / "server"


agent = ServerAgent(manifest)
register_agent(agent)
