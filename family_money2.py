import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Configure page
st.set_page_config(layout="wide")
st.title("💰 Personal Financial Advisor Dashboard")

# User inputs
with st.sidebar:
    st.header("Income & Settings")
    monthly_income = st.number_input("Monthly Salary (UGX)", min_value=0, value=5000000, step=100000)
    current_savings = st.number_input("Current Savings (UGX)", min_value=0, value=0, step=100000)
    savings_goal = st.number_input("Monthly Savings Goal (UGX)", min_value=0, value=500000, step=100000)
    risk_appetite = st.select_slider("Risk Appetite", options=["Low", "Medium", "High"], value="Medium")
    st.markdown("---")
    st.caption("Adjust spending priorities:")
    essential_cut = st.slider("Essential spending adjustment", 0, 20, 0, help="Reduce essential expenses by this percentage if needed")
    discretionary_cut = st.slider("Discretionary spending adjustment", 0, 50, 0, help="Reduce discretionary expenses by this percentage if needed")

# Constants
MONTHS_IN_TERM = 3

# Data setup with enhanced categories
def load_data():
    # Groceries with enhanced categories
    groceries = [
        {"Item": "Rice", "Quantity": "3 kgs", "Price": 13500, "Priority": "Essential", "Category": "Food Staples", "Flexibility": "Low"},
        {"Item": "Tooth paste", "Quantity": "1 piece", "Price": 6000, "Priority": "Essential", "Category": "Personal Care", "Flexibility": "Medium"},
        {"Item": "Shoe polish", "Quantity": "1", "Price": 3500, "Priority": "Discretionary", "Category": "Personal Care", "Flexibility": "High"},
        {"Item": "Gizzards", "Quantity": "1 pack", "Price": 15000, "Priority": "Nice-to-have", "Category": "Protein", "Flexibility": "High"},
        {"Item": "Viennas", "Quantity": "1 pack", "Price": 12000, "Priority": "Nice-to-have", "Category": "Protein", "Flexibility": "High"},
        {"Item": "Milk", "Quantity": "1 box", "Price": 24000, "Priority": "Essential", "Category": "Dairy", "Flexibility": "Medium"},
        {"Item": "Irish potatoes", "Quantity": "1 month supply", "Price": 30000, "Priority": "Essential", "Category": "Food Staples", "Flexibility": "Low"},
        {"Item": "Baby oil", "Quantity": "1", "Price": 15000, "Priority": "Essential", "Category": "Personal Care", "Flexibility": "Medium"},
        {"Item": "Sugar", "Quantity": "2 kgs", "Price": 8000, "Priority": "Essential", "Category": "Food Staples", "Flexibility": "Medium"},
        {"Item": "Beef", "Quantity": "1 kg", "Price": 15000, "Priority": "Nice-to-have", "Category": "Protein", "Flexibility": "High"},
        {"Item": "Chicken", "Quantity": "1 kg", "Price": 15000, "Priority": "Nice-to-have", "Category": "Protein", "Flexibility": "High"},
        {"Item": "Squishy drink", "Quantity": "10", "Price": 20000, "Priority": "Discretionary", "Category": "Beverages", "Flexibility": "High"},
        {"Item": "Soap", "Quantity": "1 bar", "Price": 6000, "Priority": "Essential", "Category": "Personal Care", "Flexibility": "Low"},
        {"Item": "Eggs", "Quantity": "1 tray", "Price": 12500, "Priority": "Essential", "Category": "Protein", "Flexibility": "Medium"},
        {"Item": "Bread", "Quantity": "1 big", "Price": 6000, "Priority": "Essential", "Category": "Food Staples", "Flexibility": "Medium"},
        {"Item": "Spaghetti", "Quantity": "10 packs", "Price": 20000, "Priority": "Essential", "Category": "Food Staples", "Flexibility": "Medium"},
        {"Item": "Onions", "Quantity": "1 kg", "Price": 6000, "Priority": "Essential", "Category": "Vegetables", "Flexibility": "Medium"},
        {"Item": "Green pepper", "Quantity": "", "Price": 2000, "Priority": "Nice-to-have", "Category": "Vegetables", "Flexibility": "High"},
        {"Item": "Drinks", "Quantity": "", "Price": 20000, "Priority": "Discretionary", "Category": "Beverages", "Flexibility": "High"},
        {"Item": "Carrots", "Quantity": "", "Price": 3000, "Priority": "Nice-to-have", "Category": "Vegetables", "Flexibility": "High"},
        {"Item": "Ginger", "Quantity": "0.5 kg", "Price": 3000, "Priority": "Nice-to-have", "Category": "Vegetables", "Flexibility": "High"},
        {"Item": "Tomatoes", "Quantity": "", "Price": 6000, "Priority": "Essential", "Category": "Vegetables", "Flexibility": "Medium"},
        {"Item": "Medicine (Azithromycin)", "Quantity": "", "Price": 7000, "Priority": "Essential", "Category": "Healthcare", "Flexibility": "Low"},
    ]
    
    # Bills and fixed expenses with enhanced categories
    bills = [
        {"Category": "Rent", "Amount": 500000, "Priority": "Critical", "Flexibility": "None", "Type": "Housing"},
        {"Category": "Water", "Amount": 24000, "Priority": "Critical", "Flexibility": "Low", "Type": "Utilities"},
        {"Category": "Electricity", "Amount": 40000, "Priority": "Critical", "Flexibility": "Medium", "Type": "Utilities"},
        {"Category": "Garbage", "Amount": 10000, "Priority": "Critical", "Flexibility": "Low", "Type": "Utilities"},
        {"Category": "Laundry", "Amount": 12000*4, "Priority": "Essential", "Flexibility": "High", "Type": "Personal Care"},
        {"Category": "Fuel", "Amount": 50000*4, "Priority": "Essential", "Flexibility": "Medium", "Type": "Transport"},
        {"Category": "Tithe", "Amount": monthly_income*0.1, "Priority": "Essential", "Flexibility": "Medium", "Type": "Donations"},
        {"Category": "Family dates", "Amount": 150000, "Priority": "Discretionary", "Flexibility": "High", "Type": "Entertainment"},
        {"Category": "Skin care", "Amount": 200000/3, "Priority": "Discretionary", "Flexibility": "High", "Type": "Personal Care"},
        {"Category": "Pig farming", "Amount": 250000, "Priority": "Investment", "Flexibility": "High", "Type": "Investments"},
        {"Category": "Health fund", "Amount": 100000, "Priority": "Essential", "Flexibility": "Medium", "Type": "Healthcare"},
        {"Category": "School fees (Eliana)", "Amount": 700000/MONTHS_IN_TERM, "Priority": "Critical", "Flexibility": "None", "Type": "Education"},
        {"Category": "Gifts", "Amount": 50000, "Priority": "Discretionary", "Flexibility": "High", "Type": "Gifts"},
    ]
    
    # Convert to DataFrames
    groceries_df = pd.DataFrame(groceries)
    bills_df = pd.DataFrame(bills)
    
    # Adjust weekly items to monthly
    weekly_items = groceries_df[groceries_df["Item"] == "Bread"]
    weekly_items["Price"] = weekly_items["Price"] * 4
    groceries_df.update(weekly_items)
    
    return groceries_df, bills_df

groceries_df, bills_df = load_data()

# Apply user-requested spending cuts
def apply_spending_cuts(groceries_df, bills_df, essential_cut, discretionary_cut):
    # Apply cuts to groceries
    groceries_df["Original Price"] = groceries_df["Price"]
    groceries_df.loc[groceries_df["Priority"].isin(["Essential", "Critical"]), "Price"] *= (1 - essential_cut/100)
    groceries_df.loc[groceries_df["Priority"].isin(["Nice-to-have", "Discretionary"]), "Price"] *= (1 - discretionary_cut/100)
    
    # Apply cuts to bills
    bills_df["Original Amount"] = bills_df["Amount"]
    bills_df.loc[bills_df["Priority"].isin(["Essential", "Critical"]), "Amount"] *= (1 - essential_cut/100)
    bills_df.loc[bills_df["Priority"].isin(["Discretionary", "Investment"]), "Amount"] *= (1 - discretionary_cut/100)
    
    return groceries_df, bills_df

groceries_df, bills_df = apply_spending_cuts(groceries_df, bills_df, essential_cut, discretionary_cut)

# Calculate totals
total_groceries = groceries_df["Price"].sum()
total_bills = bills_df["Amount"].sum()
total_fixed_expenses = total_bills + total_groceries
disposable_income = monthly_income - total_fixed_expenses

# Automatic spending adjustment when expenses exceed income
def auto_adjust_spending(groceries_df, bills_df, monthly_income):
    total_expenses = groceries_df["Price"].sum() + bills_df["Amount"].sum()
    
    if total_expenses <= monthly_income:
        return groceries_df, bills_df, False
    
    # Calculate needed reduction
    overspend_amount = total_expenses - monthly_income
    st.warning(f"⚠️ You're overspending by {overspend_amount:,.0f} UGX. Automatic adjustments being applied.")
    
    # Create adjustment plan
    adjustment_plan = []
    
    # First target discretionary expenses
    discretionary_groceries = groceries_df[groceries_df["Priority"].isin(["Discretionary", "Nice-to-have"])].copy()
    discretionary_bills = bills_df[bills_df["Priority"].isin(["Discretionary"])].copy()
    
    total_discretionary = discretionary_groceries["Price"].sum() + discretionary_bills["Amount"].sum()
    
    if total_discretionary > 0:
        reduction_factor = min(1, overspend_amount / total_discretionary)
        if reduction_factor < 1:
            # Apply reduction to discretionary items
            discretionary_groceries["Price"] *= (1 - reduction_factor)
            discretionary_bills["Amount"] *= (1 - reduction_factor)
            
            # Update main dataframes
            groceries_df.update(discretionary_groceries)
            bills_df.update(discretionary_bills)
            
            adjustment_plan.append(f"Reduced discretionary spending by {reduction_factor*100:.0f}%")
            
            # Recalculate overspend
            total_expenses = groceries_df["Price"].sum() + bills_df["Amount"].sum()
            overspend_amount = total_expenses - monthly_income
    
    # If still overspending, target flexible essential expenses
    if overspend_amount > 0:
        flexible_essentials_groceries = groceries_df[
            (groceries_df["Priority"].isin(["Essential"])) & 
            (groceries_df["Flexibility"].isin(["Medium", "High"]))
        ].copy()
        
        flexible_essentials_bills = bills_df[
            (bills_df["Priority"].isin(["Essential"])) & 
            (bills_df["Flexibility"].isin(["Medium", "High"]))
        ].copy()
        
        total_flexible_essentials = flexible_essentials_groceries["Price"].sum() + flexible_essentials_bills["Amount"].sum()
        
        if total_flexible_essentials > 0:
            reduction_factor = min(0.5, overspend_amount / total_flexible_essentials)  # Max 50% reduction for essentials
            
            if reduction_factor > 0:
                flexible_essentials_groceries["Price"] *= (1 - reduction_factor)
                flexible_essentials_bills["Amount"] *= (1 - reduction_factor)
                
                groceries_df.update(flexible_essentials_groceries)
                bills_df.update(flexible_essentials_bills)
                
                adjustment_plan.append(f"Reduced flexible essential spending by {reduction_factor*100:.0f}%")
                
                # Recalculate overspend
                total_expenses = groceries_df["Price"].sum() + bills_df["Amount"].sum()
                overspend_amount = total_expenses - monthly_income
    
    # If still overspending after all adjustments
    if overspend_amount > 0:
        adjustment_plan.append(f"Unable to fully balance budget. Still overspending by {overspend_amount:,.0f} UGX. Consider increasing income.")
    
    return groceries_df, bills_df, adjustment_plan

# Apply automatic adjustments if needed
adjusted_groceries, adjusted_bills, adjustment_plan = auto_adjust_spending(groceries_df.copy(), bills_df.copy(), monthly_income)
if adjustment_plan:
    groceries_df, bills_df = adjusted_groceries, adjusted_bills
    total_groceries = groceries_df["Price"].sum()
    total_bills = bills_df["Amount"].sum()
    total_fixed_expenses = total_bills + total_groceries
    disposable_income = monthly_income - total_fixed_expenses

# Budget options with enhanced logic
def generate_budget_options(income, fixed_expenses, savings_goal, risk):
    remaining = income - fixed_expenses
    
    if remaining <= 0:
        return {
            "Option 1": {
                "Savings": 0,
                "Investments": 0,
                "Discretionary": 0,
                "Description": "No surplus after fixed expenses. Need to reduce costs.",
                "Feasible": False
            },
            "Option 2": {
                "Savings": 0,
                "Investments": 0,
                "Discretionary": 0,
                "Description": "No surplus after fixed expenses. Need to reduce costs.",
                "Feasible": False
            }
        }
    
    if risk == "Low":
        options = {
            "Option 1": {
                "Savings": min(savings_goal, remaining * 0.7),
                "Investments": remaining * 0.2,
                "Discretionary": remaining * 0.1,
                "Description": "Conservative: 70% savings, 20% investments, 10% discretionary",
                "Feasible": True
            },
            "Option 2": {
                "Savings": min(savings_goal, remaining * 0.6),
                "Investments": remaining * 0.3,
                "Discretionary": remaining * 0.1,
                "Description": "Moderate Conservative: 60% savings, 30% investments, 10% discretionary",
                "Feasible": True
            }
        }
    elif risk == "Medium":
        options = {
            "Option 1": {
                "Savings": min(savings_goal, remaining * 0.5),
                "Investments": remaining * 0.4,
                "Discretionary": remaining * 0.1,
                "Description": "Balanced: 50% savings, 40% investments, 10% discretionary",
                "Feasible": True
            },
            "Option 2": {
                "Savings": min(savings_goal, remaining * 0.4),
                "Investments": remaining * 0.5,
                "Discretionary": remaining * 0.1,
                "Description": "Growth Focus: 40% savings, 50% investments, 10% discretionary",
                "Feasible": True
            }
        }
    else:  # High
        options = {
            "Option 1": {
                "Savings": min(savings_goal, remaining * 0.3),
                "Investments": remaining * 0.6,
                "Discretionary": remaining * 0.1,
                "Description": "Aggressive: 30% savings, 60% investments, 10% discretionary",
                "Feasible": True
            },
            "Option 2": {
                "Savings": min(savings_goal, remaining * 0.2),
                "Investments": remaining * 0.7,
                "Discretionary": remaining * 0.1,
                "Description": "Very Aggressive: 20% savings, 70% investments, 10% discretionary",
                "Feasible": True
            }
        }
    
    # Ensure numbers add up correctly
    for option in options.values():
        total = option["Savings"] + option["Investments"] + option["Discretionary"]
        if total > remaining:
            adjustment_factor = remaining / total
            option["Savings"] *= adjustment_factor
            option["Investments"] *= adjustment_factor
            option["Discretionary"] *= adjustment_factor
    
    return options

budget_options = generate_budget_options(monthly_income, total_fixed_expenses, savings_goal, risk_appetite)

# Enhanced recommendations
def generate_recommendations(groceries, bills, budget_options, monthly_income):
    recommendations = []
    total_expenses = groceries["Price"].sum() + bills["Amount"].sum()
    
    # Check if fixed expenses exceed income
    if total_expenses > monthly_income:
        overspend_amount = total_expenses - monthly_income
        recommendations.append(
            ("Critical", 
             f"Your expenses exceed income by {overspend_amount:,.0f} UGX! "
             "The system has automatically adjusted your spending. "
             "Consider permanent reductions in discretionary items."))
    
    # Savings goal feasibility
    feasible_savings = min(budget_options["Option 1"]["Savings"], budget_options["Option 2"]["Savings"])
    if feasible_savings < savings_goal * 0.8:
        recommendations.append(
            ("High", 
             f"Your savings goal may be too ambitious. Current feasible savings: {feasible_savings:,.0f} UGX vs goal: {savings_goal:,.0f} UGX. "
             "Consider adjusting your savings target or reducing expenses."))
    
    # High-cost items analysis
    top_groceries = groceries.nlargest(3, "Price")
    if not top_groceries.empty:
        recommendations.append(
            ("Medium", 
             f"Highest grocery costs: {', '.join([f'{x.Item} ({x.Price:,.0f} UGX)' for x in top_groceries.itertuples()])}. "
             "Consider cheaper alternatives or reducing quantities."))
    
    top_bills = bills.nlargest(3, "Amount")
    if not top_bills.empty:
        recommendations.append(
            ("Medium", 
             f"Highest bills: {', '.join([f'{x.Category} ({x.Amount:,.0f} UGX)' for x in top_bills.itertuples()])}. "
             "Review for potential savings."))
    
    # Discretionary spending analysis
    discretionary_spending = groceries[groceries["Priority"] == "Discretionary"]["Price"].sum() + \
                           bills[bills["Priority"] == "Discretionary"]["Amount"].sum()
    if discretionary_spending > monthly_income * 0.15:
        recommendations.append(
            ("High", 
             f"High discretionary spending: {discretionary_spending:,.0f} UGX ({discretionary_spending/monthly_income*100:.0f}% of income). "
             "Consider reducing non-essential expenses."))
    
    # One-time expenses
    one_time_expenses = bills[bills["Type"] == "Investments"]
    if not one_time_expenses.empty:
        recommendations.append(
            ("Medium", 
             f"Investment expenses coming up: {', '.join(one_time_expenses['Category'].tolist())}. "
             "Plan accordingly to avoid cash flow issues."))
    
    return recommendations

recommendations = generate_recommendations(groceries_df, bills_df, budget_options, monthly_income)

# Create visualizations
def create_visualizations(groceries_df, bills_df, monthly_income, budget_options):
    # Expense breakdown
    expense_data = pd.concat([
        groceries_df[["Item", "Price", "Category"]].rename(columns={"Item": "Description"}).assign(Type="Groceries"),
        bills_df[["Category", "Amount", "Type"]].rename(columns={"Category": "Description", "Amount": "Price"})
    ])
    
    # Category breakdown
    category_spending = expense_data.groupby("Type")["Price"].sum().reset_index()
    category_spending["Percentage"] = category_spending["Price"] / monthly_income * 100
    
    # Priority breakdown
    priority_spending = pd.concat([
        groceries_df[["Priority", "Price"]],
        bills_df[["Priority", "Amount"]].rename(columns={"Amount": "Price"})
    ]).groupby("Priority")["Price"].sum().reset_index()
    
    # Budget options visualization
    budget_data = pd.DataFrame([
        {"Option": "Option 1", "Type": "Savings", "Amount": budget_options["Option 1"]["Savings"]},
        {"Option": "Option 1", "Type": "Investments", "Amount": budget_options["Option 1"]["Investments"]},
        {"Option": "Option 1", "Type": "Discretionary", "Amount": budget_options["Option 1"]["Discretionary"]},
        {"Option": "Option 2", "Type": "Savings", "Amount": budget_options["Option 2"]["Savings"]},
        {"Option": "Option 2", "Type": "Investments", "Amount": budget_options["Option 2"]["Investments"]},
        {"Option": "Option 2", "Type": "Discretionary", "Amount": budget_options["Option 2"]["Discretionary"]}
    ])
    
    return {
        "expense_breakdown": expense_data,
        "category_spending": category_spending,
        "priority_spending": priority_spending,
        "budget_data": budget_data
    }

visualizations = create_visualizations(groceries_df, bills_df, monthly_income, budget_options)

# Display dashboard
tab1, tab2, tab3 = st.tabs(["Overview", "Expense Analysis", "Budget Planning"])

with tab1:
    st.header("Financial Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Income", f"{monthly_income:,.0f} UGX")
        st.metric("Current Savings", f"{current_savings:,.0f} UGX")
    
    with col2:
        st.metric("Total Expenses", f"{total_fixed_expenses:,.0f} UGX", 
                 delta=f"{-total_fixed_expenses/monthly_income*100:.1f}% of income")
        st.metric("Disposable Income", f"{disposable_income:,.0f} UGX",
                 delta=f"{disposable_income/monthly_income*100:.1f}% of income" if disposable_income > 0 else "Negative")
    
    with col3:
        st.metric("Savings Goal", f"{savings_goal:,.0f} UGX")
        feasible_savings = min(budget_options["Option 1"]["Savings"], budget_options["Option 2"]["Savings"])
        st.metric("Feasible Savings", f"{feasible_savings:,.0f} UGX",
                 delta=f"{(feasible_savings - savings_goal):+,.0f} UGX" if savings_goal > 0 else "")
    
    st.markdown("---")
    
    # Expense breakdown chart
    st.subheader("Expense Breakdown")
    fig = px.pie(visualizations["category_spending"], values="Price", names="Type", 
                 title="Spending by Category")
    st.plotly_chart(fig, use_container_width=True, key=f"pie_chart_{np.random.randint(1000)}")
    
    # Priority spending chart
    st.subheader("Spending by Priority")
    fig = px.bar(visualizations["priority_spending"], x="Priority", y="Price", 
                 color="Priority", text="Price",
                 title="Total Spending by Priority Level")
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True, key=f"bar_chart_{np.random.randint(1000)}")

with tab2:
    st.header("Detailed Expense Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        priority_filter = st.multiselect("Filter by Priority", 
                                       options=groceries_df["Priority"].unique().tolist() + bills_df["Priority"].unique().tolist(),
                                       default=["Critical", "Essential"])
    
    with col2:
        category_filter = st.multiselect("Filter by Category", 
                                       options=groceries_df["Category"].unique().tolist() + bills_df["Type"].unique().tolist(),
                                       default=[])
    
    with col3:
        flexibility_filter = st.multiselect("Flexibility", 
                                          options=["None", "Low", "Medium", "High"],
                                          default=["High", "Medium"])
    
    # Apply filters
    filtered_groceries = groceries_df[
        (groceries_df["Priority"].isin(priority_filter)) & 
        (groceries_df["Category"].isin(category_filter) if category_filter else True) &
        (groceries_df["Flexibility"].isin(flexibility_filter))
    ]
    
    filtered_bills = bills_df[
        (bills_df["Priority"].isin(priority_filter)) & 
        (bills_df["Type"].isin(category_filter) if category_filter else True) &
        (bills_df["Flexibility"].isin(flexibility_filter))
    ]
    
    # Combine and display
    filtered_groceries = filtered_groceries.rename(columns={"Item": "Description", "Category": "Category", "Price": "Price"})
    filtered_bills = filtered_bills.rename(columns={"Category": "Description", "Type": "Category", "Amount": "Price"})
    
    expense_details = pd.concat([
        filtered_groceries[["Description", "Category", "Price", "Priority", "Flexibility"]],
        filtered_bills[["Description", "Category", "Price", "Priority", "Flexibility"]]
    ], ignore_index=True)
    
    st.dataframe(
        expense_details.sort_values(["Priority", "Price"], ascending=[True, False]),
        hide_index=True,
        use_container_width=True
    )
    
    # Top expenses visualization
    st.subheader("Top Expenses")
    top_expenses = expense_details.nlargest(10, "Price")
    if not top_expenses.empty:
        fig = px.bar(top_expenses, x="Description", y="Price", color="Priority",
                    title="Top 10 Expenses by Amount")
        st.plotly_chart(fig, use_container_width=True, key=f"top_expenses_{np.random.randint(1000)}")

with tab3:
    st.header("Budget Planning & Recommendations")
    
    # Budget options
    st.subheader("Budget Allocation Options")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{list(budget_options.keys())[0]}**")
        st.write(budget_options["Option 1"]["Description"])
        
        fig = px.pie(
            pd.DataFrame({
                "Type": ["Savings", "Investments", "Discretionary"],
                "Amount": [
                    budget_options["Option 1"]["Savings"],
                    budget_options["Option 1"]["Investments"],
                    budget_options["Option 1"]["Discretionary"]
                ]
            }),
            values="Amount", names="Type",
            title="Budget Allocation"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"budget_pie1_{np.random.randint(1000)}")
        
        st.metric("Total Allocated", 
                 f"{budget_options['Option 1']['Savings'] + budget_options['Option 1']['Investments'] + budget_options['Option 1']['Discretionary']:,.0f} UGX",
                 delta=f"{disposable_income - (budget_options['Option 1']['Savings'] + budget_options['Option 1']['Investments'] + budget_options['Option 1']['Discretionary']):+,.0f} UGX remaining")
    
    with col2:
        st.markdown(f"**{list(budget_options.keys())[1]}**")
        st.write(budget_options["Option 2"]["Description"])
        
        fig = px.pie(
            pd.DataFrame({
                "Type": ["Savings", "Investments", "Discretionary"],
                "Amount": [
                    budget_options["Option 2"]["Savings"],
                    budget_options["Option 2"]["Investments"],
                    budget_options["Option 2"]["Discretionary"]
                ]
            }),
            values="Amount", names="Type",
            title="Budget Allocation"
        )
        st.plotly_chart(fig, use_container_width=True, key=f"budget_pie2_{np.random.randint(1000)}")
        
        st.metric("Total Allocated", 
                 f"{budget_options['Option 2']['Savings'] + budget_options['Option 2']['Investments'] + budget_options['Option 2']['Discretionary']:,.0f} UGX",
                 delta=f"{disposable_income - (budget_options['Option 2']['Savings'] + budget_options['Option 2']['Investments'] + budget_options['Option 2']['Discretionary']):+,.0f} UGX remaining")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("Recommendations & Action Items")
    for priority, text in recommendations:
        if priority == "Critical":
            with st.error(f"**{priority} Priority**: {text}"):
                pass
        elif priority == "High":
            with st.warning(f"**{priority} Priority**: {text}"):
                pass
        else:
            with st.info(f"**{priority} Priority**: {text}"):
                pass
    
    # Spending Adjustments by Priority Table
    st.subheader("Spending Adjustments by Priority")
    
    # Create a summary of original vs adjusted spending by priority
    def create_adjustment_summary(groceries_df, bills_df):
        # Combine groceries and bills
        all_expenses = pd.concat([
            groceries_df[["Item", "Original Price", "Price", "Priority"]].rename(columns={"Item": "Description"}),
            bills_df[["Category", "Original Amount", "Amount", "Priority"]].rename(columns={
                "Category": "Description",
                "Original Amount": "Original Price",
                "Amount": "Price"
            })
        ])
        
        # Calculate adjustments
        all_expenses["Adjustment"] = all_expenses["Price"] - all_expenses["Original Price"]
        all_expenses["% Change"] = (all_expenses["Adjustment"] / all_expenses["Original Price"]) * 100
        
        # Group by priority
        priority_summary = all_expenses.groupby("Priority").agg({
            "Original Price": "sum",
            "Price": "sum",
            "Adjustment": "sum",
            "% Change": "mean"
        }).reset_index()
        
        priority_summary = priority_summary.rename(columns={
            "Original Price": "Original Amount",
            "Price": "Adjusted Amount",
            "Adjustment": "Total Adjustment",
            "% Change": "Avg % Change"
        })
        
        # Calculate percentage of income
        priority_summary["% of Income"] = (priority_summary["Adjusted Amount"] / monthly_income) * 100
        
        return priority_summary.sort_values("Adjusted Amount", ascending=False), all_expenses
    
    priority_summary, detailed_adjustments = create_adjustment_summary(groceries_df, bills_df)
    
    # Show summary table
    st.write("**Summary of Spending Adjustments by Priority Level**")
    st.dataframe(
        priority_summary.style.format({
            "Original Amount": "{:,.0f} UGX",
            "Adjusted Amount": "{:,.0f} UGX",
            "Total Adjustment": "{:,.0f} UGX",
            "Avg % Change": "{:.1f}%",
            "% of Income": "{:.1f}%"
        }),
        hide_index=True,
        use_container_width=True
    )
    
    # Detailed adjustments table with filters
    st.write("**Detailed Item-by-Item Adjustments**")
    
    adj_col1, adj_col2 = st.columns(2)
    with adj_col1:
        adj_priority_filter = st.multiselect(
            "Filter by Priority (Detailed)",
            options=detailed_adjustments["Priority"].unique(),
            default=["Critical", "Essential"]
        )
    with adj_col2:
        show_only_adjusted = st.checkbox("Show only adjusted items", value=True)
    
    # Apply filters
    filtered_adjustments = detailed_adjustments[
        detailed_adjustments["Priority"].isin(adj_priority_filter)
    ]
    if show_only_adjusted:
        filtered_adjustments = filtered_adjustments[filtered_adjustments["Adjustment"] != 0]
    
    # Ensure unique column names and reset index to avoid conflicts
    filtered_adjustments = filtered_adjustments.rename(columns={
        "Original Price": "Original_Price",
        "Price": "Adjusted_Price",
        "Adjustment": "Amount_Adjusted",
        "% Change": "Percentage_Change"
    }).reset_index(drop=True)
    
    # Display detailed adjustments
    st.dataframe(
        filtered_adjustments.sort_values(["Priority", "Amount_Adjusted"]).style.format({
            "Original_Price": "{:,.0f} UGX",
            "Adjusted_Price": "{:,.0f} UGX",
            "Amount_Adjusted": "{:,.0f} UGX",
            "Percentage_Change": "{:.1f}%"
        }).apply(lambda x: ["background: #ffcccc" if v < 0 else "" for v in x], 
               subset=["Amount_Adjusted"]),
        column_config={
            "Description": "Item/Expense",
            "Original_Price": "Original Amount",
            "Adjusted_Price": "Adjusted Amount",
            "Amount_Adjusted": st.column_config.NumberColumn(
                "Amount Saved",
                format="%,d UGX",
                help="Negative values indicate spending reductions"
            ),
            "Percentage_Change": st.column_config.NumberColumn(
                "% Change",
                format="%.1f%%",
                help="Percentage reduction from original amount"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Add some analysis of the adjustments
    total_reduction = priority_summary["Total Adjustment"].sum()
    if total_reduction < 0:
        st.info(f"💡 Total spending reduced by **{-total_reduction:,.0f} UGX** across all categories")
    
    # Show impact on savings
    if disposable_income > 0:
        original_disposable = monthly_income - (groceries_df["Original Price"].sum() + bills_df["Original Amount"].sum())
        savings_impact = disposable_income - original_disposable
        if savings_impact > 0:
            st.success(f"📈 These adjustments increased your disposable income by **{savings_impact:,.0f} UGX**")
    
    # Savings projection
    st.subheader("Savings Projection")
    if st.checkbox("Show 12-month projection"):
        selected_option = st.radio("Use budget option:", ["Option 1", "Option 2"])
        monthly_savings = budget_options[selected_option]["Savings"]
        
        savings_data = []
        current = current_savings
        for month in range(1, 13):
            current += monthly_savings
            savings_data.append({
                "Month": datetime(2023, month, 1).strftime("%b %Y"),
                "Amount": current,
                "Monthly Addition": monthly_savings,
                "Cumulative Savings": current
            })
        
        savings_df = pd.DataFrame(savings_data)
        
        fig = px.line(savings_df, x="Month", y="Cumulative Savings", 
                     title="12-Month Savings Projection",
                     markers=True)
        fig.update_traces(line_color="green")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(savings_df, hide_index=True)