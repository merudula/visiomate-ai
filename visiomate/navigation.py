"""Walking navigation using OpenStreetMap (Nominatim geocoding + OSRM routing). Free, no API key."""
import requests

UA = {"User-Agent": "VisioMateAI/0.1 (assistive project)"}


def get_location(cfg: dict):
    nav = cfg.get("navigation", {})
    if nav.get("lat") and nav.get("lon"):
        return float(nav["lat"]), float(nav["lon"])
    # IP-based fallback (city level only!). Replace with a GPS module for real use.
    try:
        j = requests.get("https://ipinfo.io/json", timeout=6).json()
        lat, lon = j["loc"].split(",")
        return float(lat), float(lon)
    except Exception:
        return None


def geocode(place: str, near=None):
    params = {"q": place, "format": "json", "limit": 1}
    if near:
        params["viewbox"] = f"{near[1]-0.3},{near[0]+0.3},{near[1]+0.3},{near[0]-0.3}"
    r = requests.get("https://nominatim.openstreetmap.org/search", params=params, headers=UA, timeout=10).json()
    return (float(r[0]["lat"]), float(r[0]["lon"])) if r else None


def _step_text(step) -> str:
    m = step["maneuver"]
    kind, mod = m.get("type", ""), m.get("modifier", "")
    road = step.get("name") or "the path"
    dist = int(step["distance"])
    if kind == "arrive":
        return "You have arrived at your destination."
    verb = {"left": "turn left", "right": "turn right", "slight left": "bear left",
            "slight right": "bear right", "sharp left": "turn sharp left",
            "sharp right": "turn sharp right", "uturn": "make a U turn"}.get(mod, "continue straight")
    if kind == "depart":
        return f"Start walking on {road} for {dist} metres."
    return f"{verb.capitalize()} onto {road}, then walk {dist} metres."


class Navigator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.steps = []
        self.i = 0

    def start(self, destination: str) -> str:
        here = get_location(self.cfg)
        if not here:
            return "I could not find your current location."
        dest = geocode(destination, here)
        if not dest:
            return f"I could not find {destination}."
        url = f"https://router.project-osrm.org/route/v1/foot/{here[1]},{here[0]};{dest[1]},{dest[0]}"
        r = requests.get(url, params={"steps": "true", "overview": "false"}, timeout=12).json()
        if r.get("code") != "Ok":
            return "I could not find a walking route."
        route = r["routes"][0]
        self.steps = [_step_text(s) for s in route["legs"][0]["steps"]]
        self.i = 0
        km = route["distance"] / 1000
        mins = int(route["duration"] / 60)
        return f"Route found. {km:.1f} kilometres, about {mins} minutes. " + self.next()

    def next(self) -> str:
        if not self.steps:
            return "No active route. Say navigate to, and a place name."
        if self.i >= len(self.steps):
            return "You have reached the end of the route."
        s = self.steps[self.i]
        self.i += 1
        return s
