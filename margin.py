import streamlit as st
import pandas as pd
import numpy as np

# Fixed parameters (from Excel)
SAMPLE_SIZE = 1000

def calculate_metrics(pass_rate, price, allocation, payout_size, payout_rate, company_profit_split):
    """
    Calculate financial metrics for a given pass rate, price, and allocation.
    """
    # Total evaluation spend (with 25% discount for resets)
    total_eval_spend = (price * SAMPLE_SIZE) * 0.75
    
    # Total users expected to become live
    total_users = SAMPLE_SIZE * (pass_rate / 100)  # Convert % to decimal
    
    # Total allocation for users who pass
    total_allocation = total_users * allocation
    
    # Profit margin at live allocation
    profit_margin_live = 1 - (total_allocation / total_eval_spend)
    
    # Total company profits from 1st payout
    total_company_profit = (total_users * payout_rate * payout_size) * company_profit_split
    
    # Profit margin after 1st payout considered
    profit_margin_after_payout = 1 - ((total_allocation - total_company_profit) / total_eval_spend)
    
    # Additional metrics for transparency
    total_eval_spend_discounted = total_eval_spend
    total_users_live = total_users
    total_allocation_users_pass = total_allocation
    percent_funds_paid_out = total_allocation / total_eval_spend
    profit_margin_live_allocation = profit_margin_live
    total_company_profit_payout = total_company_profit
    profit_margin_after_payout_considered = profit_margin_after_payout
    
    return {
        "Total Eval Spend (Discounted)": total_eval_spend_discounted,
        "Total Users Expected to Become Live": total_users_live,
        "Total Allocation of Users Who Pass": total_allocation_users_pass,
        "% Of Funds Paid Out in Allocation To Traders": percent_funds_paid_out,
        "Profit Margins at Live Allocation": profit_margin_live_allocation,
        "Total Company Profits of 1st Payout": total_company_profit_payout,
        "Profit Margin After 1st Payout Considered": profit_margin_after_payout_considered,
    }

def main():
    st.title("Optimal Financial Scenario Finder")
    
    # User inputs for ranges and steps
    st.sidebar.header("Input Parameters")
    
    # Adjustable variables
    pass_rate_min = st.sidebar.number_input("Minimum Expected Pass Rate (%)", min_value=0.0, max_value=100.0, value=8.0)
    pass_rate_max = st.sidebar.number_input("Maximum Expected Pass Rate (%)", min_value=0.0, max_value=100.0, value=25.0)
    pass_rate_step = st.sidebar.number_input("Pass Rate Step Size (%)", min_value=0.1, max_value=10.0, value=1.0)
    
    price_min = st.sidebar.number_input("Minimum Price ($)", min_value=0, max_value=1000, value=100)
    price_max = st.sidebar.number_input("Maximum Price ($)", min_value=0, max_value=1000, value=250)
    price_step = st.sidebar.number_input("Price Step Size ($)", min_value=1, max_value=100, value=25)
    
    allocation_min = st.sidebar.number_input("Minimum Allocation ($)", min_value=0, max_value=10000, value=1500)
    allocation_max = st.sidebar.number_input("Maximum Allocation ($)", min_value=0, max_value=10000, value=3000)
    allocation_step = st.sidebar.number_input("Allocation Step Size ($)", min_value=1, max_value=1000, value=250)
    
    payout_size = st.sidebar.number_input("Payout Size ($)", min_value=0, max_value=10000, value=1000)
    payout_rate = st.sidebar.number_input("Payout Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100  # Convert % to decimal
    company_profit_split = st.sidebar.number_input("Company Profit Split (%)", min_value=0.0, max_value=100.0, value=20.0) / 100  # Convert % to decimal
    
    # Generate ranges for pass rate, price, and allocation
    pass_rates = np.arange(pass_rate_min, pass_rate_max + pass_rate_step, pass_rate_step)
    prices = np.arange(price_min, price_max + price_step, price_step)
    allocations = np.arange(allocation_min, allocation_max + allocation_step, allocation_step)
    
    # Calculate all combinations
    results = []
    for pass_rate in pass_rates:
        for price in prices:
            for allocation in allocations:
                metrics = calculate_metrics(pass_rate, price, allocation, payout_size, payout_rate, company_profit_split)
                results.append({
                    "Pass Rate (%)": pass_rate,
                    "Price ($)": price,
                    "Allocation ($)": allocation,
                    **metrics
                })
    
    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    
    # Display the results
    st.header("Financial Scenarios")
    st.write(df)
    
    # Allow user to select a row for detailed metrics
    st.header("Detailed Metrics for Selected Scenario")
    selected_index = st.number_input("Enter the row number to view detailed metrics:", min_value=0, max_value=len(df) - 1, value=0)
    
    if selected_index >= 0 and selected_index < len(df):
        selected_row = df.iloc[selected_index]
        st.write("### Selected Scenario Details")
        st.write(selected_row)
    else:
        st.write("Please select a valid row number.")

if __name__ == "__main__":
    main()
