import os
from io import BytesIO
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
import requests
import streamlit as st
import yfinance as yf

# --------------------------------------------------
# ENVIRONMENT & PORTABLE ASSET CONFIGURATION
# --------------------------------------------------

# Resolve the directory containing this script to create robust relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_ICON_PATH = os.path.join(BASE_DIR, "assets", "lloyds_logo.png")

# High-resolution rasterized PNG fallback to prevent Streamlit rendering errors
REMOTE_PNG_URL = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7b/Lloyds_Bank_logo.svg/512px-Lloyds_Bank_logo.svg.png"

# Safely verify and assign the web-safe page favicon asset
if os.path.exists(LOCAL_ICON_PATH):
    page_icon_asset = Image.open(LOCAL_ICON_PATH)
else:
    page_icon_asset = REMOTE_PNG_URL

# --------------------------------------------------
# STREAMLIT INTERFACE INITIALIZATION
# --------------------------------------------------
st.set_page_config(
    page_title="Lloyds Equity Intelligence Engine",
    page_icon=page_icon_asset,
    layout="wide",
)


# --------------------------------------------------
# MEMORY-CACHED IMAGE PIPELINE
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def load_sidebar_logo():
    """Attempts to load the application logo locally from relative paths.

    Falls back to an explicit web transmission request if deployed in cloud containers.
    """
    if os.path.exists(LOCAL_ICON_PATH):
        try:
            return Image.open(LOCAL_ICON_PATH)
        except Exception:
            pass  # Fall through to remote fallback if the image file is corrupted

    try:
        response = requests.get(REMOTE_PNG_URL, timeout=5)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception:
        return None


sidebar_logo = load_sidebar_logo()
if sidebar_logo:
    st.sidebar.image(sidebar_logo, width=180)

# --------------------------------------------------
# SIDEBAR CONTROL PANEL
# --------------------------------------------------
st.sidebar.title("Configuration Panel")

symbol = st.sidebar.text_input("Stock Ticker Symbol", "LLOY.L")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
run = st.sidebar.button("Execute Pipeline")

# Enhanced Application Branding Title
st.title("📊 Lloyds Equity Intelligence Engine")

# --------------------------------------------------
# DATA EXTREMENESS & ENGINE PROCESSING PIPELINE
# --------------------------------------------------
if run:
    with st.spinner("Executing financial calculations and gathering telemetry..."):
        # Fetch target ticker historical equity metrics
        df = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
        )

        if df.empty:
            st.error(
                f"Data pipeline failure: No information returned for symbol '{symbol}'."
            )
            st.stop()

        df.dropna(inplace=True)

        # Clean complex MultiIndex structural columns returned by newer yfinance versions
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # --------------------------------------------------
        # FEATURE ENGINEERING & ALGORITHMIC METRICS
        # --------------------------------------------------
        # Intraday tracking vectors
        df["Price_Change"] = df["Close"] - df["Open"]
        df["Daily_Return_Pct"] = (df["Close"] / df["Open"] - 1.0) * 100.0

        # Simple Moving Averages (Trend Isolation)
        df["SMA_50"] = df["Close"].rolling(window=50, min_periods=1).mean()
        df["SMA_200"] = df["Close"].rolling(window=200, min_periods=1).mean()

        # Moving Average Convergence Divergence (MACD Momentum)
        ema12 = df["Close"].ewm(span=12, adjust=False).mean()
        ema26 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

        # Relative Strength Index (RSI Momentum Oscillator)
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        # Using exponential weighting matches standard structural RSI formulas cleaner
        rs = (
            gain.ewm(com=13, adjust=False).mean()
            / loss.ewm(com=13, adjust=False).mean()
        )
        df["RSI"] = 100.0 - (100.0 / (1.0 + rs))

        # Bollinger Bands (Volatility Thresholds)
        ma20 = df["Close"].rolling(window=20, min_periods=1).mean()
        std20 = df["Close"].rolling(window=20, min_periods=1).std()
        df["BB_Upper"] = ma20 + (2.0 * std20)
        df["BB_Lower"] = ma20 - (2.0 * std20)

        # Temporal dimension feature extractions
        df["Month"] = df.index.month_name()
        df["Month_Num"] = df.index.month
        df["Quarter"] = df.index.to_period("Q").astype(str)
        df["Day"] = df.index.day_name()

        # Macro Bound Tracking Metrics (Rolling 252 trading day window approximation)
        df["52W_High"] = df["Close"].rolling(window=252, min_periods=1).max()
        df["52W_Low"] = df["Close"].rolling(window=252, min_periods=1).min()

    # --------------------------------------------------
    # KEY PERFORMANCE INDICATOR (KPI) METRIC BLOCKS
    # --------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Latest Close Price", f"£{df['Close'].iloc[-1]:.2f}")
    c2.metric("Rolling 52W High (Avg)", f"£{df['52W_High'].mean():.2f}")
    c3.metric("Rolling 52W Low (Avg)", f"£{df['52W_Low'].mean():.2f}")
    c4.metric("Aggregate Trading Volume", f"{int(df['Volume'].sum()):,}")
    c5.metric("Current RSI Momentum", f"{df['RSI'].iloc[-1]:.2f}")

    # --------------------------------------------------
    # DATA VISUALIZATION VECTOR ENGINE
    # --------------------------------------------------

    # Chart 1: Structural Equity Valuation with Trend Lines
    fig_price = go.Figure()
    fig_price.add_trace(
        go.Scatter(x=df.index, y=df["Close"], name="Closing Price")
    )
    fig_price.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA_50"],
            name="50-Day SMA",
            line=dict(dash="dot"),
        )
    )
    fig_price.add_trace(
        go.Scatter(
            x=df.index,
            y=df["SMA_200"],
            name="200-Day SMA",
            line=dict(dash="dash"),
        )
    )
    fig_price.update_layout(
        title="Price Valuation & Trend Moving Averages",
        xaxis_title="Timeline Date",
        yaxis_title="Price (£)",
        hovermode="x unified",
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # Chart 2: Candlestick Volatility Mapping (Bollinger Bands)
    fig_candle = go.Figure()
    fig_candle.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Market Candlestick",
        )
    )
    fig_candle.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_Upper"],
            name="Bollinger Band Upper",
            line=dict(color="rgba(173, 216, 230, 0.6)"),
        )
    )
    fig_candle.add_trace(
        go.Scatter(
            x=df.index,
            y=df["BB_Lower"],
            name="Bollinger Band Lower",
            line=dict(color="rgba(173, 216, 230, 0.6)"),
            fill="tonexty",
            fillcolor="rgba(173, 216, 230, 0.1)",
        )
    )
    fig_candle.update_layout(
        title="Price Variance Profile (Candlesticks & Volatility Bands)",
        xaxis_title="Timeline Date",
        yaxis_title="Price (£)",
        xaxis_rangeslider_visible=False,
    )
    st.st.plotly_chart(fig_candle, use_container_width=True)

    # Chart 3: MACD Convergence Dynamics
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD Core"))
    fig_macd.add_trace(
        go.Scatter(
            x=df.index, y=df["Signal"], name="Signal Vector", line=dict(dash="dot")
        )
    )
    fig_macd.update_layout(
        title="Moving Average Convergence Divergence (MACD)",
        xaxis_title="Timeline Date",
        yaxis_title="Delta Value",
        hovermode="x unified",
    )
    st.plotly_chart(fig_macd, use_container_width=True)

    # Chart 4: Relative Strength Index Tracking Oscillator
    fig_rsi = go.Figure()
    fig_rsi.add_trace(
        go.Scatter(
            x=df.index, y=df["RSI"], name="RSI Value", line=dict(color="purple")
        )
    )
    fig_rsi.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        annotation_text="Overbought Market Threshold (70)",
    )
    fig_rsi.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="Oversold Market Threshold (30)",
    )
    fig_rsi.update_layout(
        title="Relative Strength Index Velocity Profile",
        xaxis_title="Timeline Date",
        yaxis_title="Oscillator Index (0-100)",
        yaxis=dict(range=[10, 90]),
    )
    st.plotly_chart(fig_rsi, use_container_width=True)

    # Chart 5: Volumetric Spatial Distribution Analysis
    monthly = (
        df.groupby(["Month_Num", "Month"])["Volume"]
        .sum()
        .reset_index()
        .sort_values("Month_Num")
    )
    fig_month = go.Figure(
        go.Bar(
            y=monthly["Month"],
            x=monthly["Volume"],
            orientation="h",
            marker=dict(color="teal"),
        )
    )
    fig_month.update_layout(
        title="Monthly Aggregate Asset Volume Distribution",
        xaxis_title="Accumulated Volume Track",
        yaxis_title="Calendar Month",
    )
    st.plotly_chart(fig_month, use_container_width=True)

    # --------------------------------------------------
    # DATA DOWNLOAD CONTROLLER
    # --------------------------------------------------
    st.markdown("---")
    st.download_button(
        label="📥 Export Engine Processed Data Array (CSV)",
        data=df.to_csv().encode("utf-8"),
        file_name=f"processed_{symbol}_metrics.csv",
        mime="text/csv",
    )

else:
    st.info(
        "Awaiting target initialization. Configure parameters inside the controls panel and select Execute Pipeline."
    )
