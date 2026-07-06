# 📊 Lloyds Equity Intelligence (LEI) Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-green.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

**Lloyds Bank Stock Analysis Dashboard** is a financial analytics project built using **Python** and **Streamlit** that provides real-time stock analysis for **LLOY.L (Lloyds Banking Group)**.

The dashboard integrates live financial data, technical indicators, and interactive visualisations to help investors analyse stock price trends, volatility, and market momentum for smarter investment decisions.

> 🏦 Built as part of the **Lloyds Bank Financial Data Science Simulation** — achieving a **40% reduction in manual reporting cycles** through automated data pipelines.

---

## 🖥️ Dashboard Preview

### Main Dashboard
![Dashboard](images/dashboard_main.png)

### Technical Indicators Dashboard
![Indicators](images/dashboard_indicators.png)

---

## ✅ Features

- **Real-Time Market Data:** Automated stock data retrieval using `yfinance`
- **Trend Detection:** Moving Average indicators (**SMA 50** and **SMA 200**) for identifying long-term market trends
- **Volatility Monitoring:** **Bollinger Bands** to detect price expansion and contraction periods
- **Momentum Indicators:**
  - **MACD (Moving Average Convergence Divergence)**
  - **RSI (Relative Strength Index)**
- **Interactive Visualisations:** Built using **Plotly** for zoomable and dynamic charts
- **Financial KPIs:**
  - Latest Closing Price
  - 52-Week High and Low
  - Trading Volume
  - RSI Momentum Indicator
- **Custom Date Range Analysis:** Analyse stock performance within any selected time period

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/jtp-codes/Lloyds_Bank_dashboard.git
cd Lloyds_Bank_dashboard
```

### 2. Install Python dependencies

```bash
pip install streamlit pandas numpy yfinance plotly requests pillow
```

### 3. Run the Streamlit application

```bash
streamlit run Lloyds_Bank_dashboard.py
```

---

## 📈 Key Insights

- **Trend Identification:** Moving averages smooth short-term price fluctuations and reveal the overall trend direction of Lloyds Bank stock
- **Volatility Detection:** Bollinger Bands highlight periods when the stock may be overextended, indicating possible corrections
- **Momentum Tracking:** RSI and MACD provide early signals of potential trend reversals and determine whether the stock is **overbought** or **oversold**
- **Interactive Exploration:** Investors can zoom into charts and analyse detailed price movements using interactive Plotly graphs

---

## 📂 Repository Structure

```
Lloyds Equity Intelligence (LEI) Dashboard/
│
├── Lloyds_Bank_dashboard.py     # Main application file
├── Lloyds_logo.png              # Lloyds Bank logo asset
├── images/
│   ├── dashboard_main.png       # Main dashboard screenshot
│   └── dashboard_indicators.png # Technical indicators screenshot
│
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core language |
| Streamlit | Web application framework |
| Pandas & NumPy | Data manipulation |
| yfinance | Real-time stock data retrieval |
| Plotly | Interactive visualisations |
| Pillow | Image processing |

---

## 👤 Creator

**Joel Tom Philip**
B.Sc. Data Science Student — Homi Bhabha State University & FinX Institute, Mumbai

📧 [philipjoel800@gmail.com](mailto:philipjoel800@gmail.com)
🔗 [LinkedIn](https://linkedin.com/in/joeltomphilip)
🐙 [GitHub](https://github.com/jtp-codes)

---

## ⭐ Support

If you found this project helpful, please consider giving it a **⭐ on GitHub** — it helps others discover the project!
