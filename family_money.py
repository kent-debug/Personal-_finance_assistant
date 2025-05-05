import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configure page
st.set_page_config(layout="wide")
st.title("Personal Financial Advisor Dashboard")

# User inputs
st.sidebar.header("Income & Settings")
monthly_income = st.sidebar.number_input("Monthly Salary (UGX)", min_value=0, value=5000000, step=100000)
current_savings = st.sidebar.number_input("Current Savings (UGX)", min_value=0, value=0, step=100000)
savings_goal = st.sidebar.number_input("Monthly Savings Goal (UGX)", min_value=0, value=500000, step=100000)
risk_appetite = st.sidebar.select_slider("Risk Appetite", options=["Low", "Medium", "High"], value="Medium")

# Constants
MONTHS_IN_TERM = 3

# Data setup
def load_data():
    # Groceries
    groceries = [
        {"Item": "Rice", "Quantity": "3 kgs", "Price": 13500, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Tooth paste", "Quantity": "1 piece", "Price": 6000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Shoe polish", "Quantity": "1", "Price": 3500, "Priority": "Low", "Frequency": "Monthly"},
        {"Item": "Gizzards", "Quantity": "1 pack", "Price": 15000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Viennas", "Quantity": "1 pack", "Price": 12000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Milk", "Quantity": "1 box", "Price": 24000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Irish potatoes", "Quantity": "1 month supply", "Price": 30000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Baby oil", "Quantity": "1", "Price": 15000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Sugar", "Quantity": "2 kgs", "Price": 8000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Beef", "Quantity": "1 kg", "Price": 15000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Chicken", "Quantity": "1 kg", "Price": 15000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Squishy drink", "Quantity": "10", "Price": 20000, "Priority": "Low", "Frequency": "Monthly"},
        {"Item": "Soap", "Quantity": "1 bar", "Price": 6000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Eggs", "Quantity": "1 tray", "Price": 12500, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Bread", "Quantity": "1 big", "Price": 6000, "Priority": "High", "Frequency": "Weekly"},
        {"Item": "Spaghetti", "Quantity": "10 packs", "Price": 20000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Onions", "Quantity": "1 kg", "Price": 6000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Green pepper", "Quantity": "", "Price": 2000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Drinks", "Quantity": "", "Price": 20000, "Priority": "Low", "Frequency": "Monthly"},
        {"Item": "Carrots", "Quantity": "", "Price": 3000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Ginger", "Quantity": "0.5 kg", "Price": 3000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Item": "Tomatoes", "Quantity": "", "Price": 6000, "Priority": "High", "Frequency": "Monthly"},
        {"Item": "Medicine (Azithromycin)", "Quantity": "", "Price": 7000, "Priority": "High", "Frequency": "As needed"},
    ]
    
    # Bills and fixed expenses
    bills = [
        {"Category": "Rent", "Amount": 500000, "Priority": "Critical", "Frequency": "Monthly"},
        {"Category": "Water", "Amount": 24000, "Priority": "Critical", "Frequency": "Monthly"},
        {"Category": "Electricity", "Amount": 40000, "Priority": "Critical", "Frequency": "Monthly"},
        {"Category": "Garbage", "Amount": 10000, "Priority": "Critical", "Frequency": "Monthly"},
        {"Category": "Laundry", "Amount": 12000*4, "Priority": "High", "Frequency": "Monthly"},
        {"Category": "Fuel", "Amount": 50000*4, "Priority": "High", "Frequency": "Monthly"},
        {"Category": "Tithe", "Amount": monthly_income*0.1, "Priority": "High", "Frequency": "Monthly"},
        {"Category": "Family dates", "Amount": 150000, "Priority": "Medium", "Frequency": "Monthly"},
        {"Category": "Skin care", "Amount": 200000/3, "Priority": "Low", "Frequency": "Monthly"},
        {"Category": "Pig farming", "Amount": 250000, "Priority": "Medium", "Frequency": "One-time"},
        {"Category": "Health fund", "Amount": 100000, "Priority": "High", "Frequency": "Monthly"},
        {"Category": "School fees (Eliana)", "Amount": 700000/MONTHS_IN_TERM, "Priority": "Critical", "Frequency": "Monthly"},
        {"Category": "Gifts", "Amount": 50000, "Priority": "Medium", "Frequency": "Monthly"},
    ]
    
    # Convert to DataFrames
    groceries_df = pd.DataFrame(groceries)
    bills_df = pd.DataFrame(bills)
    
    # Adjust weekly items to monthly
    weekly_items = groceries_df[groceries_df["Frequency"] == "Weekly"]
    weekly_items["Price"] = weekly_items["Price"] * 4
    weekly_items["Frequency"] = "Monthly"
    groceries_df.update(weekly_items)
    
    return groceries_df, bills_df

groceries_df, bills_df = load_data()

# Calculate totals
total_groceries = groceries_df["Price"].sum()
total_bills = bills_df["Amount"].sum()
total_fixed_expenses = total_bills + total_groceries
disposable_income = monthly_income - total_fixed_expenses

# Budget options
def generate_budget_options(income, fixed_expenses, savings_goal, risk):
    remaining = income - fixed_expenses
    
    if risk == "Low":
        # Conservative approach - prioritize savings
        option1 = {
            "Savings": min(savings_goal, remaining),
            "Investments": max(0, remaining - savings_goal) * 0.3,
            "Discretionary": max(0, remaining - savings_goal) * 0.7,
            "Description": "Conservative: Prioritizes savings goal, limits discretionary spending"
        }
        option2 = {
            "Savings": min(savings_goal * 1.2, remaining),
            "Investments": max(0, remaining - savings_goal * 1.2) * 0.2,
            "Discretionary": max(0, remaining - savings_goal * 1.2) * 0.8,
            "Description": "Moderate Conservative: Slightly higher savings, balanced spending"
        }
    elif risk == "Medium":
        # Balanced approach
        option1 = {
            "Savings": min(savings_goal * 0.8, remaining),
            "Investments": max(0, remaining - savings_goal * 0.8) * 0.5,
            "Discretionary": max(0, remaining - savings_goal * 0.8) * 0.5,
            "Description": "Balanced: Moderate savings with equal investments and discretionary"
        }
        option2 = {
            "Savings": min(savings_goal * 0.9, remaining),
            "Investments": max(0, remaining - savings_goal * 0.9) * 0.6,
            "Discretionary": max(0, remaining - savings_goal * 0.9) * 0.4,
            "Description": "Growth Focus: Higher investments with reasonable savings"
        }
    else:  # High
        # Aggressive approach - prioritize investments
        option1 = {
            "Savings": min(savings_goal * 0.5, remaining),
            "Investments": max(0, remaining - savings_goal * 0.5) * 0.8,
            "Discretionary": max(0, remaining - savings_goal * 0.5) * 0.2,
            "Description": "Aggressive Growth: Maximizes investments, minimal discretionary"
        }
        option2 = {
            "Savings": min(savings_goal * 0.7, remaining),
            "Investments": max(0, remaining - savings_goal * 0.7) * 0.7,
            "Discretionary": max(0, remaining - savings_goal * 0.7) * 0.3,
            "Description": "Balanced Aggressive: Strong investments with some savings buffer"
        }
    
    return option1, option2

budget_option1, budget_option2 = generate_budget_options(monthly_income, total_fixed_expenses, savings_goal, risk_appetite)

# Recommendations
def generate_recommendations(groceries, bills, budget_options):
    recommendations = []
    
    # Check if fixed expenses exceed income
    if total_fixed_expenses > monthly_income:
        recommendations.append(("Critical", "Your fixed expenses exceed your income! You need to reduce expenses or increase income."))
    
    # Identify lower priority expenses that could be reduced
    low_priority_groceries = groceries[groceries["Priority"].isin(["Low", "Medium"])].sort_values("Price", ascending=False)
    if not low_priority_groceries.empty:
        recommendations.append(("High", f"Consider reducing low/medium priority groceries like: {', '.join(low_priority_groceries.head(3)['Item'].tolist())}"))
    
    medium_priority_bills = bills[bills["Priority"] == "Medium"].sort_values("Amount", ascending=False)
    if not medium_priority_bills.empty:
        recommendations.append(("Medium", f"Potential to reduce medium priority bills: {', '.join(medium_priority_bills.head(3)['Category'].tolist())}"))
    
    # Check if savings goal is realistic
    if budget_option1["Savings"] < savings_goal * 0.8:
        recommendations.append(("High", f"Your savings goal may be too ambitious. Consider adjusting from {savings_goal:,} UGX to {int(monthly_income * 0.1):,} UGX as a starting point."))
    
    # Check one-time expenses
    one_time_expenses = bills[bills["Frequency"] == "One-time"]
    if not one_time_expenses.empty:
        recommendations.append(("Medium", f"Plan for one-time expenses: {', '.join(one_time_expenses['Category'].tolist())}"))
    
    return recommendations

recommendations = generate_recommendations(groceries_df, bills_df, [budget_option1, budget_option2])

# Display dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Income Summary")
    st.metric("Monthly Income", f"{monthly_income:,} UGX")
    st.metric("Current Savings", f"{current_savings:,} UGX")
    st.metric("Savings Goal", f"{savings_goal:,} UGX")

with col2:
    st.subheader("Fixed Expenses")
    st.metric("Total Groceries", f"{total_groceries:,} UGX")
    st.metric("Total Bills", f"{total_bills:,} UGX")
    st.metric("Total Fixed Expenses", f"{total_fixed_expenses:,} UGX")

with col3:
    st.subheader("Disposable Income")
    st.metric("After Fixed Expenses", f"{disposable_income:,} UGX")
    st.metric("Savings Goal Feasibility", 
              f"{(budget_option1['Savings']/savings_goal*100 if savings_goal > 0 else 100):.0f}%",
              delta=f"{(budget_option1['Savings'] - savings_goal):+,} UGX")

# Budget options
st.subheader("Budget Options")
budget_col1, budget_col2 = st.columns(2)

with budget_col1:
    st.markdown("**Option 1**")
    st.write(budget_option1["Description"])
    st.metric("Savings", f"{budget_option1['Savings']:,.0f} UGX")
    st.metric("Investments", f"{budget_option1['Investments']:,.0f} UGX")
    st.metric("Discretionary", f"{budget_option1['Discretionary']:,.0f} UGX")

with budget_col2:
    st.markdown("**Option 2**")
    st.write(budget_option2["Description"])
    st.metric("Savings", f"{budget_option2['Savings']:,.0f} UGX")
    st.metric("Investments", f"{budget_option2['Investments']:,.0f} UGX")
    st.metric("Discretionary", f"{budget_option2['Discretionary']:,.0f} UGX")

# Expense details with filters
st.subheader("Expense Details")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    priority_filter = st.multiselect("Filter by Priority", options=["Critical", "High", "Medium", "Low"], default=["Critical", "High"])

with col2:
    category_filter = st.selectbox("Filter by Category", options=["All", "Groceries", "Bills"])

with col3:
    frequency_filter = st.multiselect("Filter by Frequency", options=["Monthly", "Weekly", "One-time", "As needed"], default=["Monthly"])

# Apply filters
if category_filter == "All":
    filtered_groceries = groceries_df[
        (groceries_df["Priority"].isin(priority_filter)) & 
        (groceries_df["Frequency"].isin(frequency_filter))
    ]
    filtered_bills = bills_df[
        (bills_df["Priority"].isin(priority_filter)) & 
        (bills_df["Frequency"].isin(frequency_filter))
    ]
    filtered_expenses = pd.concat([
        filtered_groceries[["Item", "Price", "Priority", "Frequency"]].rename(columns={"Item": "Description", "Price": "Amount"}),
        filtered_bills[["Category", "Amount", "Priority", "Frequency"]].rename(columns={"Category": "Description"})
    ])
else:
    if category_filter == "Groceries":
        filtered_expenses = groceries_df[
            (groceries_df["Priority"].isin(priority_filter)) & 
            (groceries_df["Frequency"].isin(frequency_filter))
        ][["Item", "Price", "Priority", "Frequency"]].rename(columns={"Item": "Description", "Price": "Amount"})
    else:
        filtered_expenses = bills_df[
            (bills_df["Priority"].isin(priority_filter)) & 
            (bills_df["Frequency"].isin(frequency_filter))
        ][["Category", "Amount", "Priority", "Frequency"]].rename(columns={"Category": "Description"})

st.dataframe(
    filtered_expenses.sort_values(["Priority", "Amount"], ascending=[True, False]),
    column_config={
        "Description": "Item",
        "Amount": st.column_config.NumberColumn("Amount (UGX)", format="%,d")
    },
    hide_index=True,
    use_container_width=True
)

# Recommendations
st.subheader("Recommendations & Risks")
for priority, text in recommendations:
    if priority == "Critical":
        st.error(f"🚨 {text}")
    elif priority == "High":
        st.warning(f"⚠️ {text}")
    else:
        st.info(f"ℹ️ {text}")

# Savings projection
if st.checkbox("Show Savings Projection (12 months)"):
    monthly_savings = budget_option1["Savings"]
    savings_data = []
    current = current_savings
    for month in range(1, 13):
        current += monthly_savings
        savings_data.append({
            "Month": datetime(2023, month, 1).strftime("%b %Y"),
            "Amount": current,
            "Monthly Addition": monthly_savings
        })
    
    savings_df = pd.DataFrame(savings_data)
    st.line_chart(savings_df, x="Month", y="Amount")
    st.dataframe(savings_df, hide_index=True,
                column_config={
                    "Amount": st.column_config.NumberColumn("Total Savings (UGX)", format="%,d"),
                    "Monthly Addition": st.column_config.NumberColumn("Monthly Addition (UGX)", format="%,d")
                })