# FinPath — Prototype

A working proof-of-concept for the "Sovereign Technology for India" hackathon submission.

Covers three of the core engines from the project proposal:
1. **Financial Health Score** — real weighted formula (Section 10.1 of the proposal)
2. **Multi-Goal Planner** — conservative / balanced / aggressive scenario comparison
3. **Fraud Shield** — Hugging Face text classifier with a rule-based backup signal

---

## 1. Run it on your own laptop (5 minutes)

**Step 1 — Install Python** (skip if you already have it)
Download from [python.org](https://www.python.org/downloads/) — get version 3.10 or newer. During install on Windows, tick "Add Python to PATH."

**Step 2 — Open a terminal in this folder**
- Windows: open the `finpath_app` folder, type `cmd` in the address bar, press Enter
- Mac: right-click the folder → "New Terminal at Folder"

**Step 3 — Install the requirements**
```
pip install -r requirements.txt
```
This will take a few minutes the first time (it downloads Streamlit and the ML libraries).

**Step 4 — Run the app**
```
streamlit run app.py
```
Your browser should open automatically to `http://localhost:8501`. If not, open that link manually.

**Note on the Fraud Shield tab:** the first time you click "Check message," it will download a small AI model from Hugging Face (a few hundred MB, one-time only, needs internet). If that download is slow or blocked, the app automatically falls back to the rule-based scorer instead — it will still work, just tell you so in a caption under the result.

---

## 2. Put it on GitHub (for your submission)

1. Create a free account at [github.com](https://github.com) if you don't have one
2. Click "New repository," name it `finpath-prototype`, make it **Public**, create it
3. On your computer, in this folder's terminal, run:
```
git init
git add .
git commit -m "FinPath prototype - Idea Round resubmission"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/finpath-prototype.git
git push -u origin main
```
(Replace `YOUR-USERNAME` with your actual GitHub username. If `git` isn't installed, download it from [git-scm.com](https://git-scm.com/downloads) first.)

---

## 3. Deploy a live demo link (free, ~10 minutes)

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account
2. Click "New app," select your `finpath-prototype` repository, branch `main`, main file `app.py`
3. Click "Deploy" — wait a few minutes
4. You'll get a live public link like `https://finpath-prototype.streamlit.app` — this is your demo link for the submission

---

## 4. Record your demo video

Use your phone or a free screen recorder (Windows: Xbox Game Bar, `Win+G`. Mac: `Cmd+Shift+5`).

Suggested 2-3 minute flow:
1. Show the sidebar — enter a family's income, expenses, emergency fund
2. Switch to **Financial Health Score** tab — explain the score and its breakdown
3. Switch to **Multi-Goal Planner** — add 1-2 goals, show how the three scenarios differ
4. Switch to **Fraud Shield** — paste a scam-sounding message, show it get flagged; paste a normal message, show it pass
5. Close with one line: "This is a proof-of-concept — the full vision, including voice input, trilingual support, and government scheme matching, is detailed in the project proposal."

Upload to YouTube as **Unlisted**, copy the link for your submission.

---

## What this prototype deliberately does NOT include (and why)

To keep this honest: this is a scoped proof-of-concept, not the full product. Not built yet:
- Trilingual / voice interface
- Government schemes & scholarships matching
- Real-time investment suggestions
- Account Aggregator bank integration
- Persistent database (this version resets when you close the browser tab)

All of these are fully designed in the project proposal (with database schema, algorithms, and architecture) — this prototype exists to prove the **core planning and fraud-detection logic actually works**, which is what "Proof of Concept" stage means.
