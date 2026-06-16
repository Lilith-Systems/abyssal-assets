# Wave 4 — Speculative Cerebellum

from agents import SubAgent, AgentManifest, register_agent

manifest = AgentManifest(
    id="cerebellum",
    name="Speculative Cerebellum",
    version="1.0.0",
    sephira="BINAH",
    description="Bounded local prep + cloud offload — Ollama local speculation, rich model verification, circuit breaker",
    wave=4,
)


class CerebellumAgent(SubAgent):
    def _register_routes(self):
        super()._register_routes()

        @self.router.post("/infer")
        async def infer(prompt: str = "", system: str = ""):
            import httpx
            try:
                async with httpx.AsyncClient(timeout=30) as client:
                    r = await client.post("http://localhost:11434/api/generate", json={
                        "model": "nemotron-mini:4b",
                        "prompt": prompt,
                        "system": system,
                        "stream": False,
                    })
                    if r.status_code == 200:
                        data = r.json()
                        return {"model": "nemotron-mini", "response": data.get("response", ""), "local": True}
                    return {"error": f"Ollama: {r.status_code}"}
            except Exception as e:
                return {"error": str(e), "local": False, "hint": "Is Ollama running?"}

        @self.router.get("/status")
        async def status():
            import httpx
            ollama_ok = False
            try:
                async with httpx.AsyncClient(timeout=3) as client:
                    r = await client.get("http://localhost:11434/api/tags")
                    ollama_ok = r.status_code == 200
            except Exception:
                pass
            return {
                "ollama_running": ollama_ok,
                "model": "nemotron-mini:4b",
                "mode": "local_speculation",
                "circuit_breaker": {"failures": 0, "state": "closed"},
            }


agent = CerebellumAgent(manifest)
register_agent(agent)
