import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
    
    # Profit margin at live allocation (convert to percentage)
    profit_margin_live = (1 - (total_allocation / total_eval_spend)) * 100
    
    # Total company profits from 1st payout
    total_company_profit = (total_users * payout_rate * payout_size) * company_profit_split
    
    # Profit margin after 1st payout considered (convert to percentage)
    profit_margin_after_payout = (1 - ((total_allocation - total_company_profit) / total_eval_spend)) * 100
    
    return profit_margin_after_payout  # Return the profit margin after payout

def main():
    st.title("Optimal Financial Scenario Finder")
    
    # User inputs for Live Allocation and ranges
    st.sidebar.header("Input Parameters")
    
    # Live Allocation (fixed value)
    live_allocation = st.sidebar.number_input("Live Allocation ($)", min_value=0, max_value=10000, value=2000)
    
    # Adjustable ranges
    pass_rate_min = st.sidebar.number_input("Minimum Expected Pass Rate (%)", min_value=0.0, max_value=100.0, value=8.0)
    pass_rate_max = st.sidebar.number_input("Maximum Expected Pass Rate (%)", min_value=0.0, max_value=100.0, value=25.0)
    pass_rate_step = st.sidebar.number_input("Pass Rate Step Size (%)", min_value=0.1, max_value=10.0, value=1.0)
    
    price_min = st.sidebar.number_input("Minimum Price ($)", min_value=0, max_value=1000, value=100)
    price_max = st.sidebar.number_input("Maximum Price ($)", min_value=0, max_value=1000, value=250)
    price_step = st.sidebar.number_input("Price Step Size ($)", min_value=1, max_value=100, value=25)
    
    allocation_min = st.sidebar.number_input("Minimum Allocation ($)", min_value=0, max_value=10000, value=1500)
    allocation_max = st.sidebar.number_input("Maximum Allocation ($)", min_value=0, max_value=10000, value=3000)
    allocation_step = st.sidebar.number_input("Allocation Step Size ($)", min_value=1, max_value=1000, value=250)
    
    # Payout and profit split inputs
    payout_size = st.sidebar.number_input("Payout Size ($)", min_value=0, max_value=10000, value=1000)
    payout_rate = st.sidebar.number_input("Payout Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100  # Convert % to decimal
    company_profit_split = st.sidebar.number_input("Company Profit Split (%)", min_value=0.0, max_value=100.0, value=20.0) / 100  # Convert % to decimal
    
    # Generate ranges for pass rate, price, and allocation
    pass_rates = np.arange(pass_rate_min, pass_rate_max + pass_rate_step, pass_rate_step)
    prices = np.arange(price_min, price_max + price_step, price_step)
    allocations = np.arange(allocation_min, allocation_max + allocation_step, allocation_step)
    
    # Create a grid of pass rates and prices for the 3D plot
    X, Y = np.meshgrid(pass_rates, prices)
    Z = np.zeros_like(X)  # Profit margins after payout
    
    # Calculate profit margins for each combination of pass rate and price
    for i in range(len(pass_rates)):
        for j in range(len(prices)):
            Z[j, i] = calculate_metrics(
                pass_rates[i], prices[j], live_allocation, payout_size, payout_rate, company_profit_split
            )
    
    # Create a 3D surface plot
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(
        title="Profit Margin After Payout (%)",
        scene=dict(
            xaxis_title="Pass Rate (%)",
            yaxis_title="Price ($)",
            zaxis_title="Profit Margin After Payout (%)",
        ),
        margin=dict(l=0, r=0, b=0, t=40),
    )
    
    # Display the 3D plot
    st.header("Profit Margin After Payout")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
