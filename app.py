"""
app.py
------
Streamlit frontend for the Fake Python Jobs scraper.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd

from scraper import fetch_page, parse_job_cards, to_dataframe

SITE_URL = "https://realpython.github.io/fake-jobs/"

st.set_page_config(
    page_title="Job Listings Scraper",
    page_icon="🧭",
    layout="wide",
)


# --------------------------------------------------------------------------
# Data loading (cached so repeat interactions don't re-hit the network)
# --------------------------------------------------------------------------
@st.cache_data(ttl=600, show_spinner=False)
def load_jobs(url: str) -> pd.DataFrame:
    html = fetch_page(url)
    jobs = parse_job_cards(html)
    return to_dataframe(jobs)


# --------------------------------------------------------------------------
# Sidebar — controls
# --------------------------------------------------------------------------
st.sidebar.header("Controls")
st.sidebar.caption(f"Source: {SITE_URL}")

if st.sidebar.button("🔄 Scrape / Refresh listings", use_container_width=True):
    load_jobs.clear()

keyword = st.sidebar.text_input("Search title or company", placeholder="e.g. python, developer")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data refreshes from cache every 10 minutes, or immediately if you "
    "click **Scrape / Refresh listings**."
)

# --------------------------------------------------------------------------
# Main content
# --------------------------------------------------------------------------
st.title("🧭 Job Listings Scraper")
st.write(
    "Scrapes job postings from the "
    f"[Fake Python Jobs site]({SITE_URL}) and lets you search, filter, "
    "and download the results."
)

try:
    with st.spinner("Fetching job listings..."):
        df = load_jobs(SITE_URL)
except Exception as exc:  # noqa: BLE001 — surface any scrape failure to the user
    st.error(f"Couldn't fetch job listings: {exc}")
    st.stop()

if df.empty:
    st.warning("No job listings were found on the page.")
    st.stop()

# Location filter, built from whatever locations are actually present
locations = ["All locations"] + sorted(df["location"].unique().tolist())
location_choice = st.sidebar.selectbox("Filter by location", locations)

# Apply filters
filtered_df = df.copy()
if keyword:
    mask = (
        filtered_df["title"].str.contains(keyword, case=False, na=False)
        | filtered_df["company"].str.contains(keyword, case=False, na=False)
    )
    filtered_df = filtered_df[mask]
if location_choice != "All locations":
    filtered_df = filtered_df[filtered_df["location"] == location_choice]

# --------------------------------------------------------------------------
# Summary metrics
# --------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total listings", len(df))
col2.metric("Matching filters", len(filtered_df))
col3.metric("Unique companies", df["company"].nunique())

st.markdown("---")

# --------------------------------------------------------------------------
# Results table
# --------------------------------------------------------------------------
st.subheader("Listings")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "title": "Job Title",
        "company": "Company",
        "location": "Location",
        "url": st.column_config.LinkColumn("Apply Link", display_text="Apply →"),
    },
)

st.download_button(
    "⬇️ Download filtered results as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="job_listings.csv",
    mime="text/csv",
    use_container_width=False,
)

# --------------------------------------------------------------------------
# Quick charts
# --------------------------------------------------------------------------
with st.expander("📊 Top locations and companies"):
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.caption("Top 10 locations by number of listings")
        st.bar_chart(df["location"].value_counts().head(10))
    with chart_col2:
        st.caption("Top 10 companies by number of listings")
        st.bar_chart(df["company"].value_counts().head(10))
