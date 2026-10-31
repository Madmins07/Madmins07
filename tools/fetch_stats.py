#!/usr/bin/env python3
"""Pull live numbers for the profile panels. Needs GITHUB_TOKEN (the Actions default token is enough). Writes stats.json."""
import json, os, sys, urllib.request, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import SELECTED

USER = "Madmins07"
TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN: sys.exit("GITHUB_TOKEN missing")
now = dt.datetime.now(dt.timezone.utc); since = (now - dt.timedelta(days=365)).isoformat()
Q = """query($u:String!,$from:DateTime!,$to:DateTime!){ user(login:$u){
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, orderBy:{field:PUSHED_AT, direction:DESC}){
    totalCount nodes{ name description stargazerCount forkCount pushedAt primaryLanguage{name color}
      languages(first:6, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{name color} } } } }
  followers{totalCount}
  contributionsCollection(from:$from, to:$to){ totalCommitContributions restrictedContributionsCount
    contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } } } } }"""
req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"u": USER, "from": since, "to": now.isoformat()}}).encode(),
                             headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
u = json.load(urllib.request.urlopen(req))["data"]["user"]
repos = {r["name"]: dict(description=r["description"] or "", stars=r["stargazerCount"], forks=r["forkCount"], pushed=r["pushedAt"][:10],
                         language=(r["primaryLanguage"] or {}).get("name", ""), color=(r["primaryLanguage"] or {}).get("color", "#888")) for r in u["repositories"]["nodes"]}
lang = {}
for r in u["repositories"]["nodes"]:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]; lang.setdefault(n, [0, e["node"]["color"] or "#888"]); lang[n][0] += e["size"]
tot = sum(v[0] for v in lang.values()) or 1
languages = [[n, round(100 * v[0] / tot, 1), v[1]] for n, v in sorted(lang.items(), key=lambda kv: -kv[1][0])[:6]]
days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
cur = lon = run = 0
for d in days:
    run = run + 1 if d["contributionCount"] > 0 else 0; lon = max(lon, run)
cur = 0
for d in reversed(days):
    if d["contributionCount"] > 0: cur += 1
    elif d is days[-1]: continue
    else: break
cf = {}
try:
    c = json.load(urllib.request.urlopen(f"https://codeforces.com/api/user.info?handles={USER}"))["result"][0]
    cf = dict(rating=c.get("rating"), rank=c.get("rank", ""), maxRating=c.get("maxRating"))
except Exception as e: print("codeforces skipped:", e)
out = dict(generated=now.strftime("%Y-%m-%d"), repos=repos, selected=SELECTED,
           totals=dict(stars=sum(r["stars"] for r in repos.values()), repos=u["repositories"]["totalCount"], followers=u["followers"]["totalCount"],
                       commits_year=u["contributionsCollection"]["totalCommitContributions"], contributions_year=u["contributionsCollection"]["contributionCalendar"]["totalContributions"]),
           languages=languages, streak=dict(current=cur, longest=lon), codeforces=cf,
           weeks=[[d["contributionCount"] for d in w["contributionDays"]] for w in u["contributionsCollection"]["contributionCalendar"]["weeks"]])
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "stats.json", "w"), indent=1)
print("stats written:", out["totals"], out["streak"], out["codeforces"])
