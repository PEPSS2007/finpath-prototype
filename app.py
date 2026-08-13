"""
FinPath — Prototype
An AI-powered financial life companion for Indian families.

This is a scoped proof-of-concept covering the three core engines described
in the project proposal:
  1. Financial Health Score
  2. Multi-Goal Planner with Scenario Exploration (conservative/balanced/aggressive)
  3. Fraud Shield (Hugging Face classifier with a rule-based backup signal)

Run locally with:
    pip install streamlit --break-system-packages
    streamlit run app.py

Optional (for the real ML fraud classifier instead of the rule-based fallback):
    pip install transformers torch --break-system-packages
"""

import streamlit as st

st.set_page_config(page_title="FinPath — Prototype", page_icon="💰", layout="wide")

# ----------------------------------------------------------------------
# Session state initialisation
# ----------------------------------------------------------------------
if "goals" not in st.session_state:
    st.session_state.goals = []  # each: {"name":..., "target":..., "years":..., "priority":...}
if "fraud_checks" not in st.session_state:
    st.session_state.fraud_checks = []  # each: {"text":..., "score":..., "flagged":...}

# ----------------------------------------------------------------------
# Sidebar — Family Financial Profile (shared across all tabs)
# ----------------------------------------------------------------------
st.sidebar.title("👪 Family Financial Profile")
st.sidebar.caption("Enter this once — every tab uses it.")

monthly_income = st.sidebar.number_input("Monthly household income (₹)", min_value=0, value=60000, step=1000)
monthly_expenses = st.sidebar.number_input("Monthly household expenses (₹)", min_value=0, value=35000, step=1000)
existing_emi = st.sidebar.number_input("Existing monthly EMI (₹)", min_value=0, value=5000, step=500)
dependents = st.sidebar.number_input("Number of dependents", min_value=0, value=2, step=1)
emergency_fund = st.sidebar.number_input("Current emergency fund (₹)", min_value=0, value=60000, step=5000)
monthly_investment = st.sidebar.number_input("Amount currently invested per month (₹)", min_value=0, value=2000, step=500)

monthly_surplus = monthly_income - monthly_expenses - existing_emi
st.sidebar.metric("Monthly surplus (before goals)", f"₹{monthly_surplus:,.0f}")

# ----------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Financial Health Score", "🎯 Multi-Goal Planner", "🛡️ Fraud Shield"])

# ========================================================================
# TAB 1 — FINANCIAL HEALTH SCORE
# ========================================================================
with tab1:
    st.header("Financial Health Score")
    st.caption("A single 0–100 number summarising the family's financial standing, "
               "computed exactly as specified in the project proposal (Section 10.1).")

    # --- Component calculations (weights match the proposal) ---
    savings_ratio = max(0, monthly_surplus) / monthly_income if monthly_income > 0 else 0
    debt_ratio = existing_emi / monthly_income if monthly_income > 0 else 0
    emergency_ratio = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
    investment_ratio = monthly_investment / monthly_income if monthly_income > 0 else 0
    goal_progress = 0
    if st.session_state.goals:
        progress_values = [min(1.0, g["saved"] / g["target"]) for g in st.session_state.goals if g["target"] > 0]
        goal_progress = sum(progress_values) / len(progress_values) if progress_values else 0

    # Normalise each component to a 0-1 "goodness" score before weighting
    savings_score = min(1.0, savings_ratio / 0.30)          # saving 30%+ of income = full marks
    debt_score = max(0.0, 1.0 - debt_ratio / 0.40)           # EMI above 40% of income = zero marks
    emergency_score = min(1.0, emergency_ratio / 6.0)        # 6 months' expenses = full marks
    investment_score = min(1.0, investment_ratio / 0.15)     # investing 15%+ of income = full marks

    health_score = round(
        savings_score * 30 +
        debt_score * 25 +
        emergency_score * 20 +
        investment_score * 15 +
        goal_progress * 10
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Financial Health Score", f"{health_score} / 100")
        if health_score >= 75:
            st.success("Strong position. Ready for growth-focused investing.")
        elif health_score >= 50:
            st.warning("Stable, but with real gaps to close.")
        else:
            st.error("At risk. Emergency buffer and debt need attention first.")

    with col2:
        st.write("**Score breakdown**")
        st.progress(savings_score, text=f"Savings ratio: {savings_ratio*100:.1f}% of income (30% weight)")
        st.progress(debt_score, text=f"Debt burden: {debt_ratio*100:.1f}% of income (25% weight)")
        st.progress(emergency_score, text=f"Emergency buffer: {emergency_ratio:.1f} months' expenses (20% weight)")
        st.progress(investment_score, text=f"Investment ratio: {investment_ratio*100:.1f}% of income (15% weight)")
        st.progress(goal_progress, text=f"Average goal progress: {goal_progress*100:.1f}% (10% weight)")

# ========================================================================
# TAB 2 — MULTI-GOAL PLANNER WITH SCENARIO EXPLORATION
# ========================================================================
with tab2:
    st.header("Multi-Goal Planner")
    st.caption("Add every goal the family is working toward. FinPath explores three "
               "strategies and shows the trade-offs explicitly — it never picks silently.")

    with st.form("add_goal_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        goal_name = c1.text_input("Goal name", placeholder="e.g. House, Wedding, Education")
        goal_target = c2.number_input("Target amount (₹)", min_value=1000, value=500000, step=10000)
        goal_years = c3.number_input("Years away", min_value=0.5, value=5.0, step=0.5)
        goal_saved = c4.number_input("Already saved (₹)", min_value=0, value=0, step=5000)
        submitted = st.form_submit_button("+ Add goal")
        if submitted and goal_name:
            st.session_state.goals.append({
                "name": goal_name, "target": goal_target, "years": goal_years, "saved": goal_saved
            })
            st.rerun()

    if not st.session_state.goals:
        st.info("No goals added yet. Add one above to see the scenario comparison.")
    else:
        st.subheader("Active goals")
        for i, g in enumerate(st.session_state.goals):
            gc1, gc2, gc3, gc4, gc5 = st.columns([3, 2, 2, 2, 1])
            gc1.write(f"**{g['name']}**")
            gc2.write(f"₹{g['target']:,.0f}")
            gc3.write(f"{g['years']} yrs")
            gc4.write(f"₹{g['saved']:,.0f} saved")
            if gc5.button("✕", key=f"del_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

        st.divider()
        st.subheader("Scenario exploration")

        # Each scenario keeps a different number of months of expenses locked away
        # as an untouchable emergency buffer before allocating surplus to goals.
        scenarios = {
            "Conservative": {"buffer_months": 6, "color": "🟢"},
            "Balanced": {"buffer_months": 4, "color": "🟡"},
            "Aggressive": {"buffer_months": 2, "color": "🔴"},
        }

        cols = st.columns(3)
        for idx, (name, cfg) in enumerate(scenarios.items()):
            with cols[idx]:
                st.markdown(f"### {cfg['color']} {name}")
                required_buffer = cfg["buffer_months"] * monthly_expenses
                buffer_gap = max(0, required_buffer - emergency_fund)
                available_for_goals = max(0, monthly_surplus - (buffer_gap / 12 if buffer_gap > 0 else 0))

                total_remaining = sum(max(0, g["target"] - g["saved"]) for g in st.session_state.goals)
                if available_for_goals > 0 and total_remaining > 0:
                    months_to_complete_all = total_remaining / available_for_goals
                    years_to_complete = months_to_complete_all / 12
                else:
                    years_to_complete = float("inf")

                st.metric("Monthly buffer target", f"{cfg['buffer_months']} months")
                st.metric("Available for goals/month", f"₹{available_for_goals:,.0f}")
                if years_to_complete == float("inf"):
                    st.metric("All goals complete in", "Not reachable at current surplus")
                else:
                    st.metric("All goals complete in", f"{years_to_complete:.1f} years")

        st.divider()
        st.caption(
            "⚠️ This is a simplified, transparent rule-based model (buffer-first allocation), "
            "matching the algorithm documented in the project proposal. The full version adds "
            "per-goal priority weighting and automatic re-planning on emergency events."
        )

# ========================================================================
# TAB 3 — FRAUD SHIELD
# ========================================================================
with tab3:
    st.header("Fraud Shield")
    st.caption("Paste a suspicious SMS or message below. Uses a Hugging Face classifier "
               "when available, with a transparent rule-based backup signal — exactly as "
               "documented in the proposal's security architecture.")

    RISK_KEYWORDS = {
        "click here": 25, "click the link": 25, "urgent": 15, "verify now": 20,
        "otp": 20, "won": 20, "congratulations": 15, "claim now": 25,
        "act now": 15, "limited time": 10, "bank account blocked": 30,
        "kyc": 15, "suspended": 15, "prize": 20, "lottery": 25,
        "guaranteed": 10, "free": 5, "loan approved": 15, "processing fee": 20,
    }

    def rule_based_score(text: str):
        text_lower = text.lower()
        score = 0
        matched = []
        for kw, weight in RISK_KEYWORDS.items():
            if kw in text_lower:
                score += weight
                matched.append(kw)
        return min(100, score), matched

    @st.cache_resource(show_spinner=False)
    def load_hf_classifier():
        try:
            from transformers import pipeline
            clf = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-sms-spam-detection")
            return clf
        except Exception:
            return None

    message_text = st.text_area("Paste the message here", height=120,
                                 placeholder="e.g. Congratulations! You have won Rs 50,000. Click here to claim now.")

    if st.button("Check message", type="primary"):
        if not message_text.strip():
            st.warning("Paste a message first.")
        else:
            clf = load_hf_classifier()
            hf_result = None
            if clf is not None:
                try:
                    hf_result = clf(message_text)[0]
                except Exception:
                    hf_result = None

            rule_score, matched_keywords = rule_based_score(message_text)

            if hf_result is not None:
                hf_score = hf_result["score"] * 100 if hf_result["label"].lower() in ("spam", "1", "label_1") else (100 - hf_result["score"] * 100)
                final_score = round((hf_score + rule_score) / 2)
                source_note = "Combined score: Hugging Face model + rule-based signal"
            else:
                final_score = rule_score
                source_note = ("Rule-based signal only — Hugging Face model unavailable in this environment "
                                "(no internet access to huggingface.co). On your own machine or when deployed "
                                "to Streamlit Cloud, the real classifier loads automatically.")

            flagged = final_score >= 40
            st.session_state.fraud_checks.append({"text": message_text, "score": final_score, "flagged": flagged})

            if flagged:
                st.error(f"⚠️ Likely scam — risk score {final_score}/100")
            else:
                st.success(f"✅ Looks safe — risk score {final_score}/100")

            if matched_keywords:
                st.write("**Flagged phrases:**", ", ".join(matched_keywords))
            st.caption(source_note)

    if st.session_state.fraud_checks:
        st.divider()
        st.subheader("Family Digital Safety Score")
        recent = st.session_state.fraud_checks[-10:]
        flagged_count = sum(1 for c in recent if c["flagged"])
        safety_score = max(0, 100 - flagged_count * 15)
        st.metric("Safety score (this session)", f"{safety_score} / 100")
        st.caption(f"{flagged_count} flagged message(s) out of {len(recent)} checked this session.")

st.divider()
st.caption("FinPath prototype — built for the Sovereign Technology for India challenge. "
           "Core logic (health score, scenario planning, fraud scoring) matches the algorithms "
           "documented in the project proposal, Sections 10.1–10.9.")
