
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    page_icon="🍽️",
    layout="wide"
)

DATA_FILE = Path("online food delivery dataset.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.astype(str).str.strip()
    df = df.loc[:, ~df.columns.str.lower().str.startswith("unnamed")]
    for col in ["Age", "Monthly Income", "Family size"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df = load_data()

st.title("🍽️ Online Food Delivery Customer Dashboard")
st.caption("Interactive analysis of customer demographics, income and ordering behavior.")

with st.sidebar:
    st.header("🔎 Filters")
    occupations = sorted(df["Occupation"].dropna().astype(str).unique())
    selected = st.selectbox("Occupation", ["All"] + occupations)

filtered = df if selected == "All" else df[df["Occupation"].astype(str) == selected]

total_customers = len(filtered)
avg_age = filtered["Age"].mean() if len(filtered) else 0
positive = (filtered["Output"].astype(str).str.strip().str.lower() == "yes").sum()

c1, c2, c3 = st.columns(3)
c1.metric("👥 Total Customers", f"{total_customers:,}")
c2.metric("🎂 Average Age", f"{avg_age:.1f}")
c3.metric("🛵 Orders / Positive Output", f"{positive:,}")

st.subheader("💰 Income vs Ordering Behavior")

income = filtered.copy()
income["Output"] = income["Output"].astype(str).str.strip()
income = income.dropna(subset=["Monthly Income", "Output"])

fig1 = px.histogram(
    income,
    x="Monthly Income",
    color="Output",
    barmode="group",
    title="Monthly Income by Ordering Behavior",
    labels={"Monthly Income": "Monthly Income", "Output": "Orders Food?"},
    marginal="box"
)
fig1.update_layout(template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🎂 Customer Age Distribution")

ages = filtered.dropna(subset=["Age"])
fig2 = px.histogram(
    ages,
    x="Age",
    nbins=15,
    title="Distribution of Customer Age",
    labels={"Age": "Customer Age", "count": "Customers"},
    marginal="box"
)
fig2.update_layout(template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("📊 View filtered customer data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
