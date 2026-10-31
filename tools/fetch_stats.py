#!/usr/bin/env python3
"""Pull live numbers for the data panels. GITHUB_TOKEN (the Actions default) for GitHub; Codeforces is public. Writes stats.json."""
import json, os, sys, urllib.request, datetime as dt, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import SELECTED
USER = "Madmins07"; CF = "Madmins07"
out_path = sys.argv[1] if len(sys.argv) > 1 else "stats.json"
now = dt.datetime.now(dt.timezone.utc)
S = dict(generated=now.strftime("%Y-%m-%d"), selected=SELECTED)

def get(url, timeout=30):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "madmins07-profile"}), timeout=timeout))

# ---- Codeforces: rating history, solved problems, tags, difficulty
try:
    hist = get(f"https://codeforces.com/api/user.rating?handle={CF}")["result"]
    S["cf_history"] = [dict(t=c["ratingUpdateTimeSeconds"], r=c["newRating"], d=c["newRating"] - c["oldRating"], rank=c["rank"], name=c["contestName"]) for c in hist]
    subs = get(f"https://codeforces.com/api/user.status?handle={CF}&from=1&count=10000")["result"]
    solved = {}
    for s in subs:
        if s.get("verdict") == "OK":
            p = s["problem"]; solved.setdefault((p.get("contestId"), p.get("index")), p)
    tags = collections.Counter(t for p in solved.values() for t in p.get("tags", []))
    diff = collections.Counter(p.get("rating") for p in solved.values() if p.get("rating"))
    info = get(f"https://codeforces.com/api/user.info?handles={CF}")["result"][0]
    S["codeforces"] = dict(rating=info.get("rating"), rank=info.get("rank", ""), maxRating=info.get("maxRating"), solved=len(solved), contests=len(hist),
                           submissions=len(subs), tags=tags.most_common(8), difficulty=sorted(diff.items()),
                           best=max([c for c in S["cf_history"][1:]] or S["cf_history"], key=lambda c: c["d"]) if hist else None)
except Exception as e:
    print("codeforces skipped:", e); S["codeforces"] = {}

# ---- GitHub
TOKEN = os.environ.get("GITHUB_TOKEN")
if TOKEN:
    since = (now - dt.timedelta(days=365)).isoformat()
    Q = """query($u:String!,$from:DateTime!,$to:DateTime!){ user(login:$u){
      repositories(first:100, ownerAffiliations:OWNER, isFork:false, orderBy:{field:PUSHED_AT, direction:DESC}){ totalCount nodes{
        name description stargazerCount forkCount pushedAt primaryLanguage{name color} languages(first:6, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{name color} } } } }
      followers{totalCount}
      contributionsCollection(from:$from, to:$to){ totalCommitContributions contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } } } } }"""
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"u": USER, "from": since, "to": now.isoformat()}}).encode(),
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    u = json.load(urllib.request.urlopen(req))["data"]["user"]
    S["repos"] = {r["name"]: dict(description=r["description"] or "", stars=r["stargazerCount"], forks=r["forkCount"], pushed=r["pushedAt"][:10],
                                  language=(r["primaryLanguage"] or {}).get("name", ""), color=(r["primaryLanguage"] or {}).get("color", "#888")) for r in u["repositories"]["nodes"]}
    lang = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]; lang.setdefault(n, 0); lang[n] += e["size"]
    tot = sum(lang.values()) or 1
    S["languages"] = [[n, round(100 * v / tot, 1)] for n, v in sorted(lang.items(), key=lambda kv: -kv[1])[:6]]
    weeks = u["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    lon = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0; lon = max(lon, run)
    cur = 0
    for d in reversed(days):
        if d["contributionCount"] > 0: cur += 1
        elif d is days[-1]: continue
        else: break
    S["totals"] = dict(stars=sum(r["stars"] for r in S["repos"].values()), repos=u["repositories"]["totalCount"], followers=u["followers"]["totalCount"],
                       commits_year=u["contributionsCollection"]["totalCommitContributions"], contributions_year=u["contributionsCollection"]["contributionCalendar"]["totalContributions"])
    S["streak"] = dict(current=cur, longest=lon)
    S["weeks"] = [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]] for w in weeks]
else:
    print("GITHUB_TOKEN missing: GitHub section skipped")
json.dump(S, open(out_path, "w"), indent=1)
print("stats written:", S.get("totals"), S.get("streak"), {k: S["codeforces"].get(k) for k in ("rating", "solved", "contests")})
