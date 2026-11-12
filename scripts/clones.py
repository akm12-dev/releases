"""Relève les clones GitHub des dépôts de code AKM12 et les cumule dans un fichier JSON.

GitHub ne garde que les 14 derniers jours (un total par jour, en UTC) : ce script conserve
chaque jour vu pour obtenir un total depuis la publication des dépôts. Le fichier n'est
réécrit que si un chiffre a changé. Aucun chiffre n'est inventé : un dépôt illisible
garde ses valeurs précédentes et le script échoue pour le signaler.

Usage : STATS_TOKEN=<jeton> python3 scripts/clones.py <chemin/clones.json>
Jeton : fine-grained, propriétaire akm12-dev, permission « Administration : lecture » sur les dépôts ci-dessous.
"""
import datetime
import json
import os
import re
import sys
import urllib.request

OWNER = "akm12-dev"
REPOS = ["canon-scan-setup", "toshiba-lexmark-scan-setup", "edendisk", "sav-service-tool", "eyecontrol"]


def fetch_clones(repo: str, token: str) -> list:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{repo}/traffic/clones",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "akm12-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["clones"]


def fetch_software(token: str) -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/releases/releases?per_page=100",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "akm12-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        releases = json.load(r)
    out: dict = {}
    for rel in releases:
        m = re.match(r"^(.+)-v(\d+(?:\.\d+)*)$", rel["tag_name"])
        if not m or rel.get("draft"):
            continue
        sid, version = m.group(1), m.group(2)
        entry = out.setdefault(sid, {"downloads": 0, "version": version, "_date": rel["published_at"]})
        if rel["published_at"] > entry["_date"]:
            entry["version"], entry["_date"] = version, rel["published_at"]
        for a in rel["assets"]:
            if not re.search(r"\.(pdf|txt)$", a["name"], re.I):
                entry["downloads"] += int(a["download_count"])
    for entry in out.values():
        del entry["_date"]
    return out


def main() -> int:
    path = sys.argv[1]
    token = os.environ.get("STATS_TOKEN", "").strip()
    if not token:
        print("STATS_TOKEN manquant (secret du dépôt).", file=sys.stderr)
        return 1
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"repos": {}}
    before = json.dumps({k: data.get(k) for k in ("repos", "software")}, sort_keys=True)

    failed = []
    for repo in REPOS:
        entry = data["repos"].setdefault(repo, {"days": {}, "total": 0})
        try:
            clones = fetch_clones(repo, token)
        except Exception as e:  # noqa: BLE001 — on signale, on garde l'existant
            print(f"{repo} : lecture impossible ({e})", file=sys.stderr)
            failed.append(repo)
            continue
        for c in clones:
            if int(c["count"]) == 0:
                continue
            day = c["timestamp"][:10]
            # Le total d'un jour ne fait qu'augmenter : on garde le plus grand relevé.
            entry["days"][day] = max(entry["days"].get(day, 0), int(c["count"]))
        entry["total"] = sum(entry["days"].values())

    # Versions et téléchargements par logiciel (badges du profil GitHub) : mêmes règles que le site,
    # fichiers .pdf et .txt (guides, SHA256SUMS) exclus, toutes versions additionnées.
    try:
        software = fetch_software(token)
        data["software"] = software
    except Exception as e:  # noqa: BLE001
        print(f"releases : lecture impossible ({e})", file=sys.stderr)
        failed.append("releases")

    if json.dumps({k: data.get(k) for k in ("repos", "software")}, sort_keys=True) != before:
        data["updated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Chiffres mis à jour :", {r: data["repos"][r]["total"] for r in REPOS})
    else:
        print("Aucun changement.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
