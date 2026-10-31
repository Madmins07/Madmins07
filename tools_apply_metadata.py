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
REPOS = json.loads(r'''{"cgpa_simulator": {"desc": "Exact-distribution semester CGPA simulator: set per-course grade probabilities, get expected CGPA, percentiles and P(target), computed by convolution over every grade path. React + Express.", "homepage": "https://cgpa-simulator-omega.vercel.app", "topics": ["cgpa", "probability", "simulator", "react", "vite", "express", "recharts", "docker", "iit-kharagpur"]}, "OR2": {"desc": "Multi-objective baggage packing optimiser comparing dynamic programming and integer programming (PuLP), with a Streamlit app. IIT Kharagpur IM21204 Operations Research II.", "homepage": "https://uditangshu-or2-app-hjvctt.streamlit.app", "topics": ["operations-research", "integer-programming", "dynamic-programming", "pulp", "streamlit", "optimization", "knapsack", "iit-kharagpur"]}, "Competitive-Programming": {"desc": "Accepted solutions from Codeforces and LeetCode, in C++ (and one in Python), indexed by problem.", "homepage": "https://codeforces.com/profile/Madmins07", "topics": ["competitive-programming", "codeforces", "leetcode", "cpp", "algorithms", "data-structures"]}, "Quantitative-Finance": {"desc": "Streamlit app that pulls daily prices with yfinance and forecasts one to four years ahead with Prophet, with interactive Plotly charts.", "homepage": "", "topics": ["quantitative-finance", "time-series", "prophet", "yfinance", "streamlit", "forecasting", "python"]}, "Time-series-models": {"desc": "ARIMA forecasting of the USD/INR exchange rate: ADF stationarity testing, ACF/PACF diagnostics, and rolling one-step evaluation.", "homepage": "", "topics": ["time-series", "arima", "statsmodels", "forecasting", "econometrics", "jupyter-notebook", "forex"]}, "Neural_Networks": {"desc": "Dense neural network for MNIST digit classification in TensorFlow/Keras, from data pipeline to evaluation.", "homepage": "", "topics": ["neural-networks", "tensorflow", "keras", "mnist", "deep-learning", "jupyter-notebook"]}, "Regression-Models": {"desc": "Linear regression (house prices) and logistic regression (Titanic) implemented from scratch in NumPy with hand-written gradient descent.", "homepage": "", "topics": ["regression", "linear-regression", "logistic-regression", "numpy", "gradient-descent", "machine-learning", "from-scratch"]}, "Classification_models": {"desc": "Titanic survival prediction compared across logistic regression, naive Bayes, KNN, SVM, decision tree, random forest and XGBoost; plus an SVM baseline on Iris.", "homepage": "", "topics": ["classification", "scikit-learn", "xgboost", "titanic", "machine-learning", "jupyter-notebook"]}, "KDAG_Core_Tasks": {"desc": "KDAG core selection tasks: Levenshtein-distance spelling correction for survey data, and k-means clustering written from scratch for night-time satellite imagery.", "homepage": "", "topics": ["kdag", "levenshtein-distance", "k-means", "clustering", "opencv", "numpy", "iit-kharagpur"]}, "Business_Club_Tasks": {"desc": "Business Club induction task: exploratory data analysis of the Chipotle orders dataset with pandas and NumPy.", "homepage": "", "topics": ["pandas", "exploratory-data-analysis", "data-analysis", "jupyter-notebook"]}, "Microsoft-project": {"desc": "Yahoo Finance scraper in Python (requests + BeautifulSoup): live quotes, top gainers and losers, a CSV-backed portfolio tracker, and a headline fetcher.", "homepage": "", "topics": ["web-scraping", "beautifulsoup", "yahoo-finance", "stock-market", "python", "portfolio"]}, "Python-timepass": {"desc": "Small Tkinter desktop toys built to pass time: a stopwatch and an image viewer.", "homepage": "", "topics": ["python", "tkinter", "gui", "pillow", "mini-projects"]}, "Snake-Game": {"desc": "Snake, twice: a terminal version with curses and a windowed version with pygame.", "homepage": "", "topics": ["snake-game", "pygame", "curses", "python", "game"]}}''')
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

print(f"\n{ok} repos updated, {fail} failed.")
print("Pins are not settable through the API. Pin these six by hand at https://github.com/Madmins07 (Customize your pins):")
print("  cgpa_simulator, OR2, Competitive-Programming, Time-series-models, KDAG_Core_Tasks, Quantitative-Finance")
