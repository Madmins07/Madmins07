import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from repos import REPOS

U = "Madmins07"
SH = "style=flat-square&labelColor=07080D"

def badge(label, msg, color, logo=None):
    l = f"&logo={logo}&logoColor=EEF1ED" if logo else ""
    return f'<img src="https://img.shields.io/badge/{label}-{msg}-{color}?{SH}{l}" alt="{label} {msg}"/>'

def dyn(kind, name, color, label=None):
    lb = f"&label={label}" if label else ""
    return f'<img src="https://img.shields.io/github/{kind}/{U}/{name}?{SH}&color={color}{lb}" alt="{kind}"/>'

def head(name, r, extra_badges=""):
    from common import P
    b = []
    lang = r["lang"]; ac = P[r.get("accent", "cyan")].lstrip("#")
    if lang == "Python": b.append(badge("python", "3.10+", ac, "python"))
    elif lang == "Jupyter": b.append(badge("jupyter", "notebook", ac, "jupyter"))
    elif lang == "C++": b.append(badge("c++", "17", ac, "cplusplus"))
    elif lang == "JavaScript": b.append(badge("node", "18+", ac, "nodedotjs"))
    b.append(dyn("last-commit", name, "6F7693", "updated"))
    if r["license"]: b.append(dyn("license", name, "1C2032"))
    if r["homepage"]:
        host = r["homepage"].split("//")[1].rstrip("/").replace("-", "--")
        b.append(f'<a href="{r["homepage"]}">{badge("live", host, "F3F5FF")}</a>')
    b.append(extra_badges)
    return (f'<div align="center">\n  <img src="assets/banner.svg" alt="{r["title"]}. {r["tagline"]}" width="100%"/>\n</div>\n\n'
            f'<div align="center">\n  ' + "\n  ".join(x for x in b if x) + "\n</div>\n\n")

FOOT = ('\n---\n\n<div align="center">\n  <sub>Part of <a href="https://github.com/Madmins07">Madmins07</a> · '
        'Madhav Agarwal · IIT Kharagpur</sub>\n</div>\n')

def table(rows, h=("file", "what it does")):
    out = f"| {h[0]} | {h[1]} |\n|:--|:--|\n"
    for a, b in rows: out += f"| {a} | {b} |\n"
    return out

def colab(name, nb):
    return (f'<a href="https://colab.research.google.com/github/{U}/{name}/blob/main/{nb}">'
            f'<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/></a>')

def nbrows(name, items):
    return "| notebook | what it does | open |\n|:--|:--|:--|\n" + "".join(
        f"| [`{nb}`]({nb}) | {what} | {colab(name, nb)} |\n" for nb, what in items)

BODY = {}

BODY["cgpa_simulator"] = lambda n, r: f"""## about

Every student at Kharagpur has asked the same question the week before grades drop: *what do I need this semester?*
This app answers it properly. You give each course a credit weight and a probability for every grade from EX to F,
and the backend **convolves those distributions over every possible grade path**. The result is the exact probability
distribution of your semester CGPA. A Monte Carlo run (default 25,000 trials) sits alongside it so you can see the
simulated mean converge on the exact one.

- Expected CGPA, standard deviation, median, P10 / P25 / P75 / P90, best and worst case.
- Probability of clearing a target CGPA.
- Histogram, cumulative distribution curve, and per-course grade bars.
- Probability sliders auto-rebalance so each course always sums to 100%.

## stack

{table([("`frontend/`", "React 18 + Vite, Recharts for the charts, lucide icons."),
        ("`backend/`", "Express API with helmet and rate limiting; `src/simulation.js` holds the convolution engine."),
        ("`docker-compose.yml`", "Two containers, nginx in front of the frontend proxying `/api` to the backend."),], ("part", "what"))}
## run

```bash
npm run install:all      # installs backend and frontend
npm run dev:backend      # http://localhost:5001 (5000 is AirPlay on macOS)
npm run dev:frontend     # http://localhost:3000, proxies /api to the backend
```

With Docker:

```bash
docker compose up --build
# frontend on :3000, backend on :5050
```

## api

`POST /api/simulate`

```json
{{
  "targetCgpa": 8.0,
  "courses": [
    {{ "name": "Mathematics", "credits": 4,
      "probabilities": {{ "EX": 0.1, "A": 0.2, "B": 0.3, "C": 0.2, "D": 0.1, "P": 0.1, "F": 0.0 }} }}
  ]
}}
```

Returns `summary` (statistics and path counts), `distribution` (bucketed chart data), `exactDistribution`
(every reachable CGPA state), `gradeBreakdown` and `courseStats`.

`GET /api/grades` returns the grade order and grade-point map. `GET /health` is the health check.

## how the maths works

For each course, the grade points times credits form a discrete random variable. The semester total is the sum of
independent course variables, so its distribution is the convolution of theirs. The engine walks the courses once,
keeping a map from reachable credit-point totals to their probabilities, which is exact and runs in milliseconds
even for a full semester.
"""

BODY["OR2"] = lambda n, r: f"""## about

Course project for **IM21204 Operations Research II** at IIT Kharagpur. The problem: a student is moving and has to
decide which items go in **cabin baggage**, which go in **check-in baggage**, and which get shipped through
**packers and movers**, subject to weight and volume limits, item compatibility, and cost. It is a multi-objective
knapsack with three bins.

We formulated it two ways and compared them:

- **Dynamic programming**, with an efficiency score blending value per kilogram and value per litre.
- **Integer programming** in PuLP, solving the exact model.

The report covers the formulations, the trade-off between solution quality and runtime, and sensitivity to the
value-weight and value-volume ratios. A group submission; the hosted Streamlit app is deployed from a teammate's account.

## inside

{table([("`packing_optimizer.py`", "Both formulations, the comparison harness, and a CLI run over the sample data."),
        ("`app.py`", "Streamlit interface: upload your own item sheet, set limits and costs, see the allocation and charts."),
        ("`data/dorm_items.xlsx`", "Sample item sheet: a typical Indian college student's dorm inventory."),
        ("`docs/OR_Report.pdf`", "Full write-up with the LaTeX formulations and results."),])}
## run

```bash
pip install -r requirements.txt
streamlit run app.py              # interactive app
python packing_optimizer.py       # runs DP and IP on data/dorm_items.xlsx and prints the comparison
```
"""

def cp_index(r):
    base = r["path"]
    cf, lc = [], []
    for f in sorted(os.listdir(f"{base}/codeforces")):
        m = re.match(r"^(\d+)([A-Z]\d?)\.(cpp|py)$", f)
        link = f"https://codeforces.com/problemset/problem/{m.group(1)}/{m.group(2)}" if m else ""
        cf.append((f, link))
    over = {"Majority-element-2": "majority-element-ii", "Roman_to_Int": "roman-to-integer",
            "Valid_Parenthesis": "valid-parentheses", "Valid_Anagram2": "valid-anagram",
            "inorder-traversal-binary-tree": "binary-tree-inorder-traversal",
            "preorder-traversal-binary-tree": "binary-tree-preorder-traversal",
            "postorder-traversal-binary-tree": "binary-tree-postorder-traversal",
            "add-two-integers": "add-two-integers", "intersection-of-two-linked-lists": "intersection-of-two-linked-lists"}
    for f in sorted(os.listdir(f"{base}/Leetcode"), key=str.lower):
        stem = f.rsplit(".", 1)[0]
        slug = over.get(stem, re.sub(r"[_\s]+", "-", stem).lower())
        lc.append((f, f"https://leetcode.com/problems/{slug}/"))
    def rows(items, folder):
        return "| file | problem |\n|:--|:--|\n" + "".join(
            f"| [`{f}`]({folder}/{f}) | {('[' + f.rsplit('.',1)[0] + '](' + l + ')') if l else f.rsplit('.',1)[0]} |\n" for f, l in items)
    idx = (f"# index\n\nEvery accepted solution, linked to its problem page.\n\n"
           f"## Codeforces ({len(cf)})\n\n{rows(cf, 'codeforces')}\n## LeetCode ({len(lc)})\n\n{rows(lc, 'Leetcode')}")
    open(f"{base}/INDEX.md", "w").write(idx)
    return len(cf), len(lc)

def cp_body(n, r):
    ncf, nlc = cp_index(r)
    return f"""## about

Every accepted submission from the contest grind, kept as plain source files. Codeforces handle
[**Madmins07**](https://codeforces.com/profile/Madmins07), peak rating 1541 (Specialist).

| platform | solved | folder |
|:--|--:|:--|
| Codeforces | {ncf} | [`codeforces/`](codeforces) |
| LeetCode | {nlc} | [`Leetcode/`](Leetcode) |

The full problem-by-problem list, with links to each problem page, lives in [**INDEX.md**](INDEX.md).

## conventions

- Codeforces files are named by problem id, so `1549A.cpp` is problem A of contest 1549.
- LeetCode files are named by problem slug, so `two-sum.cpp` is *Two Sum*.
- Everything is C++17 unless the extension says otherwise.

## run one

```bash
g++ -std=c++17 -O2 -o sol codeforces/1549A.cpp && ./sol < input.txt
```
"""
BODY["Competitive-Programming"] = cp_body

BODY["Quantitative-Finance"] = lambda n, r: f"""## about

A small forecasting dashboard. Pick a ticker, pull five years of daily prices through **yfinance**, fit a
**Prophet** model, and project one to four years ahead. Raw prices, the forecast with its uncertainty band, and
the trend and seasonality components all render as interactive Plotly charts inside Streamlit.

Migrated in 2026 from the deprecated `fbprophet` package and `st.cache` to current `prophet`, `st.cache_data`,
and the current yfinance column layout.

## run

```bash
pip install -r requirements.txt
streamlit run main.py
```

## notes

- Prophet is a decomposable trend-plus-seasonality model. It is a reasonable baseline for a dashboard and a poor
  trading signal; treat the band as a visual, not a position.
- Data is cached for an hour per ticker.
"""

BODY["Time-series-models"] = lambda n, r: f"""## about

Forecasting the **USD/INR** exchange rate with ARIMA, the proper way round: test for stationarity first, read the
ACF and PACF to pick the order, fit, then evaluate with a rolling one-step walk-forward and RMSE instead of a single
in-sample fit.

## notebooks

{nbrows(n, [("ARIMA_USD_INR_PREDICTOR.ipynb", "ADF test, differencing, ACF/PACF, ARIMA(2,1,0) fit, walk-forward RMSE and plots.")])}
## data

The notebook reads `data.csv` with a `DEXINUS` column, which is the daily USD/INR series from FRED. Download it from
[fred.stlouisfed.org/series/DEXINUS](https://fred.stlouisfed.org/series/DEXINUS) and drop the CSV next to the notebook.
"""

BODY["Neural_Networks"] = lambda n, r: f"""## about

Handwritten digit classification on **MNIST** with a dense network in TensorFlow/Keras: load the dataset through
`tensorflow_datasets`, flatten and normalise, stack three ReLU layers (256, 128, 128) into a softmax over ten classes,
train, and evaluate on the held-out test split.

## notebooks

{nbrows(n, [("Neural_network_digitclass.ipynb", "Data pipeline, model definition, training curves, test accuracy, and a look at the misclassified digits.")])}
## run

The notebook pulls MNIST itself, so it runs end to end in Colab with no setup.
"""

BODY["Regression-Models"] = lambda n, r: f"""## about

Two regression models written from scratch in NumPy, with the gradient descent loop visible rather than hidden
inside a library call.

## notebooks

{nbrows(n, [("Linear_regression_scratch.ipynb", "Lot area against sale price from a house-price dataset: feature scaling, cost function, gradient descent, fitted line."),
            ("logistic_regression_from_scratch.ipynb", "Titanic survival on five features: sigmoid, log loss, gradient descent, accuracy on the test set.")])}
## data

The linear notebook downloads its CSV from a URL. The logistic notebook expects the Kaggle Titanic files
(`train.csv`, `test.csv`, `gender_submission.csv`) next to it; get them from
[kaggle.com/c/titanic](https://www.kaggle.com/c/titanic/data).
"""

BODY["Classification_models"] = lambda n, r: f"""## about

A survey of classifiers on the Kaggle **Titanic** problem, all through scikit-learn and XGBoost, so the comparison is
about the models and the feature cleaning rather than the plumbing. Plus a one-screen SVM baseline on Iris.

## notebooks

{nbrows(n, [("Titanic.ipynb", "Cleaning and encoding, then logistic regression, naive Bayes, KNN, SVM, decision tree, random forest and XGBoost, with accuracy and F1 for each."),
            ("SVM_scikit.ipynb", "Support vector classifier on Iris with accuracy and micro-F1.")])}
## data

`Titanic.ipynb` expects the Kaggle files (`train.csv`, `test.csv`, `gender_submission.csv`) next to it; get them from
[kaggle.com/c/titanic](https://www.kaggle.com/c/titanic/data). Iris ships with scikit-learn.
"""

BODY["KDAG_Core_Tasks"] = lambda n, r: f"""## about

The two selection tasks for the core team of the **Kharagpur Data Analytics Group**, solved without reaching for a
library that already does the job.

## notebooks

{nbrows(n, [("Kdag_Task1.ipynb", "Survey responses full of misspelt career names. Levenshtein edit distance implemented by hand, each response mapped to the closest of ten careers, then counted and plotted."),
            ("kdag_Task2.ipynb", "Night-time satellite imagery as a proxy for road networks. k-means clustering written from scratch with OpenCV and NumPy: random centroid initialisation, nearest-centroid assignment, update until convergence.")])}
## data

Task 1 reads `tassk1.xlsx` (the survey sheet handed out with the task). Task 2's test images are linked from inside
the notebook.
"""

BODY["Business_Club_Tasks"] = lambda n, r: f"""## about

Induction task for the Business Club: a guided exploratory analysis of the **Chipotle orders** dataset with pandas.
Shape and types, top-selling items, revenue, average order value, and the usual cleaning along the way.

## notebooks

{nbrows(n, [("Madhav_Agarwal_Level1A2.ipynb", "Loads the TSV straight from its URL and works through the questions step by step.")])}
"""

BODY["Microsoft-project"] = lambda n, r: f"""## about

A Yahoo Finance scraper in plain Python: `requests` fetches the page, `BeautifulSoup` pulls the numbers, `tabulate`
prints them, and CSV files keep state between runs.

{table([("`fetchStock('AAPL,MSFT')`", "Name, intraday price, change and change percent for each symbol."),
        ("`fetchtop()` / `fetchloss()`", "Live top gainers and losers; also refreshes `gainers.csv` / `losers.csv`."),
        ("`addtoPortfolio()` / `refreshPortfolio()`", "Build a holdings list in `portfolio.csv` and re-price it live."),
        ("`Newsletter()`", "Headlines from the Yahoo Finance front page."),], ("function", "what"))}
## run

```bash
pip install -r requirements.txt
python -c "import data_fetch_store as m; print(m.fetchStock('AAPL,MSFT'))"
```

## caveat

Scrapers track someone else's markup. Yahoo changes theirs often, so expect to adjust the selectors. The three CSVs
are sample outputs from when it was written.
"""

BODY["Python-timepass"] = lambda n, r: f"""## about

Things I do, not in my past time but to pass time. Two small Tkinter desktop apps.

{table([("`stopwatch/Fun_watch.py`", "Start, stop, reset. Hours, minutes, seconds."),
        ("`image-fun/image_viewer.py`", "Pick an image through the file dialog and show it.")])}
## run

```bash
pip install -r requirements.txt
python stopwatch/Fun_watch.py
python image-fun/image_viewer.py
```
"""

BODY["Snake-Game"] = lambda n, r: f"""## about

Snake, built twice.

{table([("`Snake-1/snake.py`", "Terminal version on `curses`. Arrow keys, a bordered window, score in the title bar."),
        ("`Snake_pygame/snake_2.py`", "Windowed version on `pygame`. Grid movement, growing tail, collision, score.")])}
## run

```bash
python Snake-1/snake.py            # terminal; on Windows first: pip install windows-curses
pip install -r requirements.txt
python Snake_pygame/snake_2.py     # window
```
"""

if __name__ == "__main__":
    for name, r in REPOS.items():
        md = head(name, r) + BODY[name](name, r) + FOOT
        open(os.path.join(r["path"], "README.md"), "w").write(md)
        print("README", name, len(md))
