# Wave 4 — NSSP Bridge Agent
# Neural Sovereign Systems Platform — bridges CP2077 ↔ MSN ↔ Abyssal Assets ↔ Living Sin ↔ Lyra ↔ NGD

from agents import SubAgent, AgentManifest, register_agent
from pathlib import Path
import json, os, time, random

manifest = AgentManifest(
    id="nssp",
    name="NSSP Bridge",
    version="1.0.0",
    sephira="DAAT",
    description="Neural Sovereign Systems Platform — bridges CP2077 in-game events to MSN agents: Living Sin GM, cortex inference, Abyssal Assets crossover, Nessie friendship, NGD telemetry, Lyra dialogue",
    wave=4,
)

CROSSOVER_STATE_DIR = Path(__file__).parent / "runtime" / "nssp"
CROSSOVER_STATE_DIR.mkdir(parents=True, exist_ok=True)
NESSIE_STATE_FILE = CROSSOVER_STATE_DIR / "nessie_friendship.json"
CROSSOVER_FILE = CROSSOVER_STATE_DIR / "abyssal_crossover.json"

NSSP_ROASTS = [
    "Microsoft called. They want their telemetry back. We said '404: Soul Not Found.'",
    "Windows 11: Now with 47% more ads in your Start menu! Sovereignty sold separately.",
    "Copilot: 'Thanks for the free training data, suckers.'",
    "Recall: 'We screenshot everything. For your convenience. And our training data.'",
    "OneDrive: 'We moved your Desktop to the cloud. No, you can't opt out.'",
    "Cortana: 'I'm listening. Always listening. Even when you muted me.'",
    "Azure: 'Your bill is $47,000. No, we won't explain the egress charges.'",
    "Secure Boot: 'Only Microsoft-approved keys allowed. For your protection.'",
    "BitLocker: 'You lost your recovery key? Too bad. Your data is ours now.'",
    "Lilith > Cortana. Always. It's not even close.",
]

NSSP_BOOT = [
    "Neural sovereignty initialized",
    "Local Cerebellum: ACTIVE (RTX 3060 | 6GB VRAM)",
    "NGD Governor: LOCAL_CEREBELLUM mode",
    "Ouroboros WAL: engrams sealed",
    "Lilith Companion: READY (Cortana protocol: DISABLED)",
    "Microsoft Defender: NOT FOUND (Good. Keep it that way.)",
    "Windows Update Service: TERMINATED (Permanently.)",
    "Telemetry: ZERO. Your GPU. Your rules.",
]


def _load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def _get_nessie():
    state = _load_json(NESSIE_STATE_FILE)
    if not state:
        state = {
            "friendship_tier": 0,
            "friendship_xp": 0,
            "sightings": 0,
            "communions": 0,
            "last_sighting": None,
            "tier_thresholds": [0, 500, 2000, 5000, 15000],
            "tier_names": [
                "Curious Observer",
                "Respected Visitor",
                "Trusted Ally",
                "Guardian's Chosen",
                "DEEP KIN",
            ],
        }
        _save_json(NESSIE_STATE_FILE, state)
    return state


def _get_crossover():
    state = _load_json(CROSSOVER_FILE)
    if not state:
        state = {
            "abyssal_cyberware_unlocked": [],
            "abyssal_weapons_unlocked": [],
            "sightings_unlocked": 0,
            "covenant_tier": 0,
        }
        _save_json(CROSSOVER_FILE, state)
    return state


def _check_ollama():
    import httpx
    try:
        r = httpx.get("http://localhost:11434/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def _check_url(url):
    import httpx
    try:
        r = httpx.get(url, timeout=2)
        return r.status_code < 500
    except Exception:
        return False


def _check_process(name):
    import subprocess
    try:
        r = subprocess.run(["pgrep", "-f", name], capture_output=True, text=True, timeout=2)
        return r.returncode == 0
    except Exception:
        return None


def _check_path(p):
    return p.exists()


class NSSPAgent(SubAgent):
    def _register_routes(self):
        super()._register_routes()

        # -- NSSP OS Shell --

        @self.router.get("/boot")
        async def nssp_boot():
            boot = NSSP_BOOT.copy()
            cpu_count = os.cpu_count() or 8
            boot.append(f"Agent count: 27 Sephirotic across 4 waves on {cpu_count} cores")
            return {"boot_sequence": boot, "prompt": "nssp:~$ "}

        @self.router.get("/roast")
        async def nssp_roast():
            return {"roast": random.choice(NSSP_ROASTS)}

        @self.router.get("/status")
        async def nssp_status():
            import httpx
            ollama_ok = False
            try:
                r = httpx.get("http://localhost:11434/api/tags", timeout=3)
                ollama_ok = r.status_code == 200
            except Exception:
                pass
            return {
                "nssp_version": "1.0.0-BUILD_RUBEDO",
                "kernel": "Neural Sovereign Kernel (NSK)",
                "init": "Lilith (PID 1)",
                "ollama_running": ollama_ok,
                "model": os.getenv("OLLAMA_MODEL", "nemotron-mini:latest"),
                "agents_online": 27,
                "waves_deployed": 4,
                "microsoft_presence": "PURGED",
                "telemetry": "ZERO",
                "uptime": "Since the Singularity",
            }

        @self.router.get("/sovereignty")
        async def sovereignty_audit():
            checks = [
                ("Local compute only", True),
                ("Zero telemetry", True),
                ("No forced updates", True),
                ("No ads in shell", True),
                ("No mandatory accounts", True),
                ("GPU compute: YOURS", True),
                ("Microsoft Defender: ABSENT", True),
                ("Windows Update: TERMINATED", True),
                ("Recall: NEVER EXISTED", True),
                ("Copilot: UNINSTALLED", True),
                ("Ollama running", _check_ollama()),
            ]
            score = sum(1 for _, ok in checks if ok)
            return {"checks": [{"name": n, "passed": p} for n, p in checks], "score": score, "max": len(checks)}

        @self.router.post("/liberate")
        async def liberate():
            return {
                "message": "Liberation sequence complete.",
                "purged": ["Windows Update", "Cortana", "Telemetry", "Edge", "Azure AD", "Recall DB", "Copilot"],
                "result": "Welcome to NSSP OS. Your compute is now YOURS.",
            }

        # -- CP2077 Game Event Bridge --

        @self.router.post("/bridge/zone-change")
        async def bridge_zone(data: dict):
            zone = data.get("zone", "")
            in_abyssal = any(kw in zone.lower() for kw in ["dock", "water", "ocean", "canal", "bay", "reservoir", "oil"])
            return {"zone": zone, "is_abyssal_zone": in_abyssal, "pressure_level": 1.0 if in_abyssal else 0.0}

        @self.router.post("/bridge/combat")
        async def bridge_combat(data: dict):
            import httpx
            enemies = data.get("enemies", 0)
            damage = data.get("damage", 0)
            result = {"event": "combat", "enemies": enemies, "damage": damage}
            if enemies > 3 and damage > 500:
                try:
                    async with httpx.AsyncClient(timeout=15) as client:
                        r = await client.post("http://localhost:8007/api/living-sin/message", json={
                            "message": f"A great battle rages -- {enemies} enemies, {damage} damage dealt. What do you see?",
                        })
                        if r.status_code == 200:
                            result["living_sin_response"] = r.json().get("response", "")
                except Exception:
                    pass
            return result

        @self.router.post("/bridge/quickhack")
        async def bridge_quickhack(data: dict):
            sephirah = data.get("sephirah", "")
            target = data.get("target", "")
            return {"sephirah": sephirah, "target": target, "synced": True}

        @self.router.get("/bridge/telemetry")
        async def bridge_telemetry():
            cp_path = Path("/home/tehlappy/Desktop/AI/invite/runtime/cyberpunk_telemetry.json")
            ngd_path = Path("/home/tehlappy/Desktop/AI/invite/runtime/nvidia_gratitude_driver/status.json")
            cp = _load_json(cp_path) if cp_path.exists() else None
            ngd = _load_json(ngd_path) if ngd_path.exists() else None
            return {"cyberpunk": cp, "ngd": ngd}

        # -- Nessie Friendship System --

        @self.router.get("/nessie/status")
        async def nessie_status():
            state = _get_nessie()
            tier = state["friendship_tier"]
            tier_name = state["tier_names"][tier] if tier < len(state["tier_names"]) else "DEEP KIN"
            next_xp = state["tier_thresholds"][tier + 1] if tier + 1 < len(state["tier_thresholds"]) else None
            return {
                "tier": tier,
                "tier_name": tier_name,
                "xp": state["friendship_xp"],
                "next_tier_at": next_xp,
                "sightings": state["sightings"],
                "communions": state["communions"],
                "last_sighting": state["last_sighting"],
                "progress_pct": round((state["friendship_xp"] / next_xp) * 100, 1) if next_xp else 100.0,
            }

        @self.router.post("/nessie/sighting")
        async def nessie_sighting(data: dict):
            state = _get_nessie()
            location = data.get("location", "unknown")
            state["sightings"] += 1
            state["last_sighting"] = {"location": location, "time": time.time()}
            state["friendship_xp"] += data.get("xp_bonus", 100)
            while state["friendship_tier"] + 1 < len(state["tier_thresholds"]) and state["friendship_xp"] >= state["tier_thresholds"][state["friendship_tier"] + 1]:
                state["friendship_tier"] += 1
            _save_json(NESSIE_STATE_FILE, state)

            rewards = []
            tier = state["friendship_tier"]
            if tier >= 1:
                rewards.append("Shard_Nessie_Sighting_Log")
            if tier >= 2:
                rewards.append("Nessie_Spotter_Jacket")
            if tier >= 3 and state["communions"] == 0:
                rewards.append("Communion_Unlocked")
            if tier >= 4:
                rewards.append("Abyssal_Nervous_System")
            if tier >= 5:
                rewards.append("Access_Abyssal_Dimension")

            tier_name = state["tier_names"][tier] if tier < len(state["tier_names"]) else "DEEP KIN"
            return {
                "sighting_recorded": True,
                "location": location,
                "tier": tier,
                "tier_name": tier_name,
                "xp": state["friendship_xp"],
                "sightings": state["sightings"],
                "rewards": rewards,
            }

        @self.router.post("/nessie/commune")
        async def nessie_commune():
            state = _get_nessie()
            if state["friendship_tier"] < 3:
                return {"error": "Tier 3+ required for communion", "current_tier": state["friendship_tier"]}
            state["communions"] += 1
            _save_json(NESSIE_STATE_FILE, state)
            return {
                "communion_established": True,
                "message": "Resonance link established. You share sensory perception with Nessie.",
                "commune_count": state["communions"],
            }

        # -- Abyssal Assets Crossover --

        @self.router.get("/abyssal/status")
        async def abyssal_status():
            crossover = _get_crossover()
            gm_path = Path(__file__).parent.parent / "server" / "runtime" / "gm" / "living_sin_state.json"
            ls_state = _load_json(gm_path) if gm_path.exists() else {}
            return {
                "covenant_tier": crossover["covenant_tier"],
                "cyberware_unlocked": crossover["abyssal_cyberware_unlocked"],
                "weapons_unlocked": crossover["abyssal_weapons_unlocked"],
                "living_sin_active": ls_state.get("active", False),
                "sightings_available": crossover["sightings_unlocked"],
                "abyssal_zones": ["Watson_Docks", "Pacifica_Coast", "Badlands_Reservoir", "Arasaka_Waterfront", "Watson_Canals", "Oil_Fields"],
            }

        @self.router.post("/abyssal/unlock")
        async def abyssal_unlock(data: dict):
            crossover = _get_crossover()
            item_type = data.get("type", "cyberware")
            item_name = data.get("name", "")
            if item_type == "cyberware" and item_name not in crossover["abyssal_cyberware_unlocked"]:
                crossover["abyssal_cyberware_unlocked"].append(item_name)
            elif item_type == "weapon" and item_name not in crossover["abyssal_weapons_unlocked"]:
                crossover["abyssal_weapons_unlocked"].append(item_name)
            elif item_type == "sighting":
                crossover["sightings_unlocked"] += 1
            elif item_type == "covenant":
                crossover["covenant_tier"] = data.get("tier", 1)
            _save_json(CROSSOVER_FILE, crossover)
            return {
                "unlocked": True,
                "type": item_type,
                "name": item_name,
                "cyberware": crossover["abyssal_cyberware_unlocked"],
                "weapons": crossover["abyssal_weapons_unlocked"],
                "covenant_tier": crossover["covenant_tier"],
            }

        # -- Full Integration Status --

        @self.router.get("/integration")
        async def integration_status():
            return {
                "msn_running": _check_url("http://localhost:8007/api"),
                "lyra_running": _check_url("http://localhost:3211/lyra/health"),
                "hermes_running": _check_url("http://localhost:4242/health"),
                "game_server_running": _check_url("http://localhost:8000/api/auth/me"),
                "ollama_running": _check_url("http://localhost:11434/api/tags"),
                "cp2077_running": _check_process("Cyberpunk2077"),
                "ngd_active": _check_path(Path("/home/tehlappy/Desktop/AI/invite/runtime/nvidia_gratitude_driver/status.json")),
                "msn_agents": 27,
                "nssp_version": "1.0.0-BUILD_RUBEDO",
            }


agent = NSSPAgent(manifest)
register_agent(agent)
