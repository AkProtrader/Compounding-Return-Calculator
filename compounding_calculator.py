import streamlit as st
import matplotlib.pyplot as plt
import random

def compound_trading_calculator(capital, gain_percent, loss_percent, rr_ratio, days):
    risk, reward = map(int, rr_ratio.split(':'))
    total_parts = risk + reward
    win_ratio = reward / total_parts
    lose_ratio = risk / total_parts

    daily_capital = [capital]
    total_wins = 0
    total_losses = 0

    for _ in range(days):
        if random.random() <= win_ratio:
            capital *= (1 + gain_percent / 100)
            total_wins += 1
        else:
            capital *= (1 - loss_percent / 100)
            total_losses += 1
        daily_capital.append(capital)

    return {
        "Final Capital": round(capital, 2),
        "Total Profit ₹": round(capital - daily_capital[0], 2),
        "Total Winning Trades": total_wins,
        "Total Losing Trades": total_losses,
        "Capital History": [round(c, 2) for c in daily_capital]
    }

# Streamlit App UI
st.set_page_config(page_title="Trading Compounding Calculator", layout="centered", initial_sidebar_state="auto")
st.title("📈 Trading Compounding Calculator")

st.markdown("Simulate compounding growth based on your trading strategy.")

# Inputs
initial_capital = st.number_input("Initial Capital (₹)", value=100000, step=1000)
gain_percent = st.number_input("Gain per Winning Trade (%)", value=2.0, step=0.1)
loss_percent = st.number_input("Loss per Losing Trade (%)", value=1.0, step=0.1)
rr_ratio = st.text_input("Risk : Reward Ratio (e.g., 1:2)", value="1:2")
days = st.slider("Number of Trading Days", min_value=1, max_value=365, value=30)

# Run Calculation
if st.button("Calculate Compounding"):
    result = compound_trading_calculator(initial_capital, gain_percent, loss_percent, rr_ratio, days)

    st.success(f"📊 Final Capital: ₹{result['Final Capital']}")
    st.metric("💰 Total Profit", f"₹{result['Total Profit ₹']}")
    st.metric("✅ Winning Trades", result['Total Winning Trades'])
    st.metric("❌ Losing Trades", result['Total Losing Trades'])

    # Chart
    st.line_chart(result['Capital History'], use_container_width=True)
