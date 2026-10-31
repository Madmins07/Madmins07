#!/usr/bin/env python3
"""Apply repository descriptions, topics and homepages (and optionally profile fields) to github.com/Madmins07.

Run it yourself from a terminal:
    python3 tools_apply_metadata.py            # repos only
    PROFILE=1 python3 tools_apply_metadata.py  # also company/blog/hireable on the profile

Token: GITHUB_TOKEN env var if set, otherwise the token your git already stores for github.com
(read through `git credential fill`, never printed). Needs the classic `repo` scope, plus `user` for PROFILE=1.
"""
import json, os, subprocess, sys, urllib.request, urllib.error

OWNER = "Madmins07"
REPOS = json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "repos.json")).read())
PROFILE_FIELDS = {"company": "Amoh · IIT Kharagpur", "blog": "https://amoh.ai", "location": "Kolkata, IN", "hireable": None}

def token():
    t = os.environ.get("GITHUB_TOKEN")
    if t: return t
    out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("password="): return line.split("=", 1)[1]
    sys.exit("No token found. Set GITHUB_TOKEN or sign in to git over HTTPS first.")

TOKEN = token()

def api(method, path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

ok = fail = 0
for name, r in REPOS.items():
    st, body = api("PATCH", f"/repos/{OWNER}/{name}", {"description": r["desc"], "homepage": r["homepage"]})
    st2, body2 = api("PUT", f"/repos/{OWNER}/{name}/topics", {"names": r["topics"]})
    good = st == 200 and st2 == 200
    ok += good; fail += not good
    print(f"{'ok  ' if good else 'FAIL'} {name:<28} desc={st} topics={st2} {'' if good else (body.get('message') or body2.get('message'))}")

st, _ = api("PATCH", f"/repos/{OWNER}/{OWNER}", {"description": "Profile README. Obsidian, sage, ink.", "homepage": "https://amoh.ai"})
print(f"{'ok  ' if st == 200 else 'FAIL'} {OWNER:<28} desc={st}")

if os.environ.get("PROFILE"):
    st, body = api("PATCH", "/user", PROFILE_FIELDS)
    print(f"{'ok  ' if st == 200 else 'FAIL'} profile fields {st} {body.get('message', '')}")
    # social links: swap the old LinkedIn slug for madmins07
    st, accounts = api("GET", "/user/social_accounts")
    old = [a["url"] for a in (accounts if isinstance(accounts, list) else []) if "linkedin.com" in a["url"] and "madmins07" not in a["url"]]
    if old:
        st, _ = api("DELETE", "/user/social_accounts", {"account_urls": old})
        print(f"{'ok  ' if st == 204 else 'FAIL'} removed old LinkedIn link {st}")
    st, body = api("POST", "/user/social_accounts", {"account_urls": ["https://www.linkedin.com/in/madmins07/"]})
    print(f"{'ok  ' if st == 201 else 'FAIL'} LinkedIn → madmins07 {st} {body.get('message', '') if isinstance(body, dict) else ''}")

print(f"\n{ok} repos updated, {fail} failed.")
print("Pins are not settable through the API. Pin these six by hand at https://github.com/Madmins07 (Customize your pins):")
print("  cgpa_simulator, OR2, Competitive-Programming, Time-series-models, KDAG_Core_Tasks, Quantitative-Finance")
