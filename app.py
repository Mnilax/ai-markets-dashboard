"""AI Model-Release Market Dashboard — Streamlit app."""

import streamlit as st
import pandas as pd
from aimarkets.fetch import load_snapshot

st.set_page_config(page_title="AI Markets Dashboard", page_icon="🤖", layout="wide")

# Load data
@st.cache_data
def load_markets():
    return [market.model_dump() for market in load_snapshot()]

markets = load_markets()

# Header
st.title("🤖 AI Prediction Markets Dashboard")
st.caption("Snapshot of AI model releases, regulation, capability milestones, and corporate events")
st.markdown("> ⚠️ *Data from cached snapshot. Not financial advice — markets update in real-time.*")

if not markets:
    st.warning("No market data found. Add data/snapshot.json.")
    st.stop()

df = pd.DataFrame(markets)

# Sidebar filters
st.sidebar.header("Filters")
categories = sorted(df["category"].unique())
selected_cats = st.sidebar.multiselect("Category", categories, default=categories)
sort_by = st.sidebar.selectbox("Sort by", ["yes_price", "volume", "close_date"], index=0)
ascending = sort_by == "close_date"

# Filter and sort
filtered = df[df["category"].isin(selected_cats)]
if sort_by == "close_date":
    filtered = filtered.copy()
    filtered["close_date"] = filtered["close_date"].replace("", pd.NA)
filtered = filtered.sort_values(sort_by, ascending=ascending, na_position="last")

# Category labels
CAT_LABELS = {
    "model_release": "🚀 Model Releases",
    "regulation": "⚖️ Regulation",
    "capability": "🧠 Capability Milestones",
    "corporate": "🏢 Corporate Events",
}

# Metrics row
col1, col2, col3, col4 = st.columns(4)
for col, cat in zip([col1, col2, col3, col4], ["model_release", "regulation", "capability", "corporate"]):
    cat_df = filtered[filtered["category"] == cat]
    col.metric(CAT_LABELS.get(cat, cat), f"{len(cat_df)} markets",
               f"Avg: {cat_df['yes_price'].mean():.0%}" if len(cat_df) > 0 else "—")

st.divider()

# Display by category
for cat in selected_cats:
    cat_df = filtered[filtered["category"] == cat].copy()
    if cat_df.empty:
        continue

    st.subheader(CAT_LABELS.get(cat, cat))

    for _, row in cat_df.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
            c1.markdown(f"**{row['question']}**")
            prob = row["yes_price"]
            color = "🟢" if prob >= 0.7 else "🟡" if prob >= 0.4 else "🔴"
            c2.metric("P(YES)", f"{color} {prob:.0%}")
            c3.metric("Volume", f"${row['volume']:,.0f}")
            c4.markdown(f"[{row['source']}]({row['url']})")

    st.divider()

# Footer
st.caption("Data sources: Kalshi, Polymarket | Built for research purposes")
