import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Company Sales Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------------- themes
THEMES = {
    "Light": {
        "bg": "#F7F9FC",
        "sidebar": "#E8EEF7",
        "card": "#FFFFFF",
        "text": "#1B2430",
        "muted": "#4A5568",
        "grid": "#D5DCE6",
        "accent": "#2563EB",
        "palette": ["#2563EB", "#E11D48", "#059669", "#D97706", "#7C3AED", "#0891B2"],
    },
    "Dark": {
        "bg": "#0F1722",
        "sidebar": "#172233",
        "card": "#1C2A3D",
        "text": "#F1F5F9",
        "muted": "#B6C2D2",
        "grid": "#33445C",
        "accent": "#60A5FA",
        "palette": ["#60A5FA", "#F87171", "#34D399", "#FBBF24", "#A78BFA", "#22D3EE"],
    },
}

with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Theme", ["Light", "Dark"], horizontal=True)
t = THEMES[mode]


def apply_css(t):
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {t['bg']}; color: {t['text']}; }}
        header[data-testid="stHeader"] {{ background: {t['bg']}; }}
        section[data-testid="stSidebar"] {{ background-color: {t['sidebar']}; }}
        h1, h2, h3, h4, h5, h6, p, label, span, li, div[data-testid="stMarkdownContainer"],
        .stRadio label, .stSelectbox label, .stMultiSelect label, .stCheckbox label {{
            color: {t['text']} !important;
        }}
        /* metric cards */
        div[data-testid="stMetric"] {{
            background: {t['card']}; border: 1px solid {t['grid']};
            border-radius: 12px; padding: 14px 18px;
        }}
        div[data-testid="stMetricValue"] {{ color: {t['accent']} !important; }}
        div[data-testid="stMetricLabel"] p {{ color: {t['muted']} !important; }}
        /* inputs */
        div[data-baseweb="select"] > div {{
            background-color: {t['card']} !important; color: {t['text']} !important;
            border-color: {t['grid']} !important;
        }}
        div[data-baseweb="select"] span, div[data-baseweb="select"] input {{
            color: {t['text']} !important;
        }}
        ul[role="listbox"], div[data-baseweb="popover"] li {{
            background-color: {t['card']} !important; color: {t['text']} !important;
        }}
        /* tabs / expanders / dataframes */
        button[data-baseweb="tab"] p {{ color: {t['text']} !important; }}
        div[data-testid="stExpander"] {{
            background: {t['card']}; border: 1px solid {t['grid']}; border-radius: 10px;
        }}
        div[data-testid="stDataFrame"] {{ border: 1px solid {t['grid']}; border-radius: 8px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


apply_css(t)


def style_axes(fig, axes, t):
    """Make matplotlib figures match the selected theme."""
    fig.patch.set_facecolor(t["card"])
    for ax in axes:
        ax.set_facecolor(t["card"])
        ax.tick_params(colors=t["text"])
        ax.xaxis.label.set_color(t["text"])
        ax.yaxis.label.set_color(t["text"])
        ax.title.set_color(t["text"])
        for spine in ax.spines.values():
            spine.set_color(t["grid"])
        ax.grid(True, color=t["grid"], alpha=0.5, linewidth=0.7)
        ax.set_axisbelow(True)
        leg = ax.get_legend()
        if leg:
            leg.get_frame().set_facecolor(t["card"])
            leg.get_frame().set_edgecolor(t["grid"])
            for txt in leg.get_texts():
                txt.set_color(t["text"])


# ---------------------------------------------------------------- data
st.title("📊 Company Sales Dashboard")

with st.sidebar:
    uploaded = st.file_uploader("Upload CSV (optional)", type="csv")


@st.cache_data
def load_data(file_bytes=None):
    if file_bytes is not None:
        return pd.read_csv(io.BytesIO(file_bytes))
    return pd.read_csv("company_sales_data.csv")


try:
    df = load_data(uploaded.getvalue() if uploaded else None)
except FileNotFoundError:
    st.error("`company_sales_data.csv` not found. Put it next to app.py or upload it from the sidebar.")
    st.stop()

PRODUCTS = {
    "facecream": "Face Cream",
    "facewash": "Face Wash",
    "toothpaste": "Tooth Paste",
    "bathingsoap": "Bathing Soap",
    "shampoo": "Shampoo",
    "moisturizer": "Moisturizer",
}
missing = [c for c in ["month_number", "total_profit", "total_units", *PRODUCTS] if c not in df.columns]
if missing:
    st.error(f"Missing columns in the CSV: {', '.join(missing)}")
    st.stop()

# ---------------------------------------------------------------- overview
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Profit", f"{df['total_profit'].sum():,.0f}")
c2.metric("Total Units", f"{df['total_units'].sum():,.0f}")
c3.metric("Best Month", int(df.loc[df["total_profit"].idxmax(), "month_number"]))
c4.metric("Duplicates", int(df.duplicated().sum()))

with st.expander("🔎 Data overview"):
    tab1, tab2, tab3 = st.tabs(["Head", "Columns & types", "Missing values"])
    with tab1:
        st.dataframe(df.head(), use_container_width=True)
    with tab2:
        info = pd.DataFrame({"dtype": df.dtypes.astype(str), "non-null": df.notna().sum()})
        st.dataframe(info, use_container_width=True)
    with tab3:
        st.dataframe(df.isnull().sum().rename("missing"), use_container_width=True)

# ---------------------------------------------------------------- chart picker
CHARTS = [
    "Month vs Total Profit (Line)",
    "Month vs Sales of All Products (Line)",
    "Total Profit by Month (Bar)",
    "Total Profit by Month (Scatter)",
    "Total Profit Share by Month (Pie)",
    "Multi-chart Dashboard (2x2)",
    "Total Units Distribution (Histogram)",
]

with st.sidebar:
    st.divider()
    chart = st.selectbox("Choose a graph", CHARTS)
    selected = list(PRODUCTS)
    if chart == "Month vs Sales of All Products (Line)":
        selected = st.multiselect(
            "Products", list(PRODUCTS), default=list(PRODUCTS), format_func=PRODUCTS.get
        )

st.subheader(chart)
x = df["month_number"]
pal = t["palette"]

if chart == CHARTS[0]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, df["total_profit"], color=pal[0], marker="o", linewidth=2.5)
    ax.set(title="Month VS Total Profit", xlabel="Month", ylabel="Total Profit")
    style_axes(fig, [ax], t)

elif chart == CHARTS[1]:
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, col in enumerate(selected):
        ax.plot(x, df[col], label=PRODUCTS[col], color=pal[i % len(pal)], marker="o", linewidth=2)
    ax.set(title="Month VS Sales", xlabel="Month", ylabel="Sales")
    if selected:
        ax.legend()
    style_axes(fig, [ax], t)

elif chart == CHARTS[2]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x, df["total_profit"], color=pal[0])
    ax.set(title="Total Profit by Month", xlabel="Month", ylabel="Total Profit")
    style_axes(fig, [ax], t)

elif chart == CHARTS[3]:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(x, df["total_profit"], color=pal[1], s=80, edgecolors=t["text"])
    ax.set(title="Total Profit by Month", xlabel="Month", ylabel="Total Profit")
    style_axes(fig, [ax], t)

elif chart == CHARTS[4]:
    fig, ax = plt.subplots(figsize=(7, 7))
    explode = [0.1 if i == df["total_profit"].idxmax() else 0 for i in df.index]
    wedges, texts, autotexts = ax.pie(
        df["total_profit"],
        labels=x,
        autopct="%1.1f%%",
        explode=explode,
        colors=plt.cm.tab20.colors,
        wedgeprops={"edgecolor": t["card"]},
    )
    for txt in texts:
        txt.set_color(t["text"])
    for txt in autotexts:
        txt.set_color("#111111")
        txt.set_fontsize(9)
    ax.set_title("Profit share by month (best month pulled out)", color=t["text"])
    fig.patch.set_facecolor(t["card"])

elif chart == CHARTS[5]:
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs[0, 0].plot(x, df["facecream"], color=pal[0], marker="o")
    axs[0, 0].set(title="Face Cream", xlabel="Month")
    axs[0, 1].bar(x, df["bathingsoap"], color=pal[2])
    axs[0, 1].set(title="Bathing Soap", xlabel="Month")
    axs[1, 0].scatter(x, df["facewash"], color=pal[1], s=60)
    axs[1, 0].set(title="Face Wash", xlabel="Month")
    axs[1, 1].hist(df["total_units"], color=pal[4], edgecolor=t["card"])
    axs[1, 1].set(title="Total Units", xlabel="Units")
    style_axes(fig, axs.flatten(), t)
    fig.tight_layout()

else:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df["total_units"], bins=10, color=pal[4], edgecolor=t["card"])
    ax.set(title="Total Units Distribution", xlabel="Total Units", ylabel="Frequency")
    style_axes(fig, [ax], t)

st.pyplot(fig, use_container_width=True)
plt.close(fig)