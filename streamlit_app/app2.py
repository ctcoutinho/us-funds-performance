import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
from utils import (
    config_menu_footer, generate_card, generate_long_text,generate_investment_profile,create_donut_chart, empty_lines, get_delta, color_highlighter
)

# Connect to your DuckDB database
def connect_to_db():
    return duckdb.connect(database='/home/spartaco/Projects/us-funds-performance/us-funds-project.db', read_only=True)

con = connect_to_db()
st.set_page_config(layout="wide")
# Streamlit page configuration
st.title("📈 US-funds stats | Streamlit")

def get_etf_facts (con, selected_symbol: str) -> pd.DataFrame:
    """Get fact table info about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_fact_table_query = """
              SELECT
                  fund_short_name,
                  fund_long_name,
                  currency,
                  fund_category,
                  fund_family,
                  exchange_code,
                  exchange_name,
                  exchange_timezone,
                  investment_strategy,
                  investment_type,
                  size_type
              FROM "us-funds-project".main_etfs.dim_etf
              WHERE fund_symbol=?
          """
    return con.execute(etf_fact_table_query, (selected_symbol,)).df()

def get_etf_top_10_holdings (con, selected_symbol: str) -> pd.DataFrame:
    """
    Get top 10 holdings about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_top_10_holdings_query ="""
            select
                holding_name as Company,
                (holding_weight * 100) as 'Portfolio Weight in %'
            from "us-funds-project".main_etfs.dim_holdings
            where fund_symbol=?
            order by holding_weight desc
          """
    
    return con.execute(etf_top_10_holdings_query, (selected_symbol,)).df()

def get_portfolio_weight (con, selected_symbol: str) -> pd.DataFrame:
    """
    Get top 10 holdings about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_portfolio_weight_query ="""
            select
                holding_name as Company,
                (holding_weight * 100) as 'Portfolio Weight in %'
            from "us-funds-project".main_etfs.dim_holdings_enriched
            where fund_symbol=?
            order by holding_weight desc
          """
    
    return con.execute(etf_portfolio_weight_query, (selected_symbol,)).df()

def get_etf_percentage_of_net_assets (con, selected_symbol: str) -> pd.DataFrame:
    """
    Get top 10 holdings about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_perc_net_assets_query ="""
            select
                fund_symbol,
                sum(holding_weight) as '% Net assets'
            from "us-funds-project".main_etfs.dim_holdings
            where fund_symbol=?
            group by fund_symbol
          """

    return con.execute(etf_perc_net_assets_query, (selected_symbol,)).df()

def get_etf_basic_info(con, selected_symbol: str) -> pd.DataFrame:
    """Get basic info about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_basic_info_query = """
              SELECT
                  fund_short_name,
                  fund_long_name,
                  currency,
                  fund_category,
                  fund_family,
                  exchange_code,
                  exchange_name,
                  exchange_timezone,
                  investment_strategy,
                  investment_type,
                  size_type
              FROM "us-funds-project".main_etfs.dim_etf
              WHERE fund_symbol=?
          """
    return con.execute(etf_basic_info_query, (selected_symbol,)).df()

def get_min_max_dates_by_fund(con) -> pd.DataFrame:
    """Get minimum and maximum dates for each fund symbol.
    
    Args:
        con: The database connection object.
        
    Returns:
        A DataFrame with the minimum and maximum dates for each fund symbol.
    """
    get_dates_by_fund_query = """
                SELECT 
                    fund_symbol,
                    min(price_date) as min_date,
                    max(price_date) as max_date
                FROM "us-funds-project".main_etfs.fact_etfs
                GROUP BY fund_symbol
                order by fund_symbol
           """
    return con.execute(get_dates_by_fund_query).df()

def display_fund_selection(con):
    """Display UI elements for fund selection and details.
    
    Args:
        con: The database connection object.
    """
    df_funds_dates = get_min_max_dates_by_fund(con)
    
    if not df_funds_dates.empty:

        sorted_symbols = df_funds_dates['fund_symbol'].sort_values()
        
        selected_symbol = st.sidebar.selectbox('Fund Symbol', sorted_symbols)
        if selected_symbol:  # Ensure selected_symbol is not None or empty
            show_fund_details(con, selected_symbol)
    else:
        st.write("No funds found.")

def show_fund_details(con, selected_symbol: str):
    # Fetch the min and max dates for the selected symbol directly within this function
    df_funds_dates = get_min_max_dates_by_fund(con)
    selected_fund_data = df_funds_dates[df_funds_dates["fund_symbol"] == selected_symbol]
    
    if not selected_fund_data.empty:
        min_date, max_date = pd.to_datetime(selected_fund_data["min_date"].iloc[0]), pd.to_datetime(selected_fund_data["max_date"].iloc[0])

        # Use a try-except block or check the length of the returned value to handle the case where an end date isn't specified
        date_selection = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        
        # Check if date_selection is a tuple with 2 elements (start_date and end_date)
        if isinstance(date_selection, tuple) and len(date_selection) == 2:
            start_date, end_date = date_selection
            st.write(f"Selected Date Range: {start_date} - {end_date}")
        else:
            # Handle the case where date_selection does not contain 2 elements
            st.error("Please select a valid date range.")
            return  # Exit the function early

        # Fetch and display ETF basic info
        df_dim_etf = get_etf_basic_info(con, selected_symbol)
        df_top_10_holdings = get_etf_top_10_holdings(con, selected_symbol)
        df_portfolio_weight = get_portfolio_weight(con, selected_symbol)
        df_percentage_of_net_assets = get_etf_percentage_of_net_assets(con, selected_symbol)
        if not df_dim_etf.empty:
            st.subheader("Selected Fund")
            generate_card(f"{selected_symbol}")
            st.text(f"For {selected_symbol}, we can provide data between the {min_date.date()} and {max_date.date()}")


###         Profile and Investment
            st.header("Profile and Investment")

            generate_investment_profile(fund_long_name = f"{df_dim_etf['fund_long_name'].iloc[0]}",
                                        fund_category=f"{df_dim_etf['fund_category'].iloc[0]}",
                                        inception_date=f"none",
                                        fund_family= f"{df_dim_etf['fund_family'].iloc[0]}",
                                        currency=f"{df_dim_etf['currency'].iloc[0]}",
                                        exchange_name = f"{df_dim_etf['exchange_name'].iloc[0]}",
                                        exchange_code = f"{df_dim_etf['exchange_code'].iloc[0]}",
                                        region = f"US"
                                        )
###         Investment strategy            
            st.subheader("Investment strategy")
            generate_long_text(f"Investment Strategy: {df_dim_etf['investment_strategy'].iloc[0]}")
           
            col1, col2 = st.columns(2)
            with col1:  
                st.subheader("Top 10 Holdings")
                st.dataframe(df_top_10_holdings,hide_index=True)

            with col2:  
                fig = create_donut_chart(
                labels=df_top_10_holdings['Company'],
                values=df_top_10_holdings['Portfolio Weight in %'],
                hole_size=0.4,  # Example of customizing the hole size
                title_text='Portfolio Weight by Company'
                )

            # Display the chart in the Streamlit app
                st.plotly_chart(fig)
            
            col1, col2, col3 = st.columns(3)  # Adjust the number of columns as needed
            
            with col1:


                generate_card(f"Currency: {df_dim_etf['currency'].iloc[0]}")
                generate_card(f"Fund Family: {df_dim_etf['fund_family'].iloc[0]}")
                generate_card(f"Exchange Timezone: {df_dim_etf['exchange_timezone'].iloc[0]}")
            
            with col2:
                generate_card(f"Fund Long Name: {df_dim_etf['fund_long_name'].iloc[0]}")
                generate_card(f"Fund Category: {df_dim_etf['fund_category'].iloc[0]}")
                generate_card(f"Exchange Code: {df_dim_etf['exchange_code'].iloc[0]}")
                
            
            with col3:
                generate_card(f"Exchange Name: {df_dim_etf['exchange_name'].iloc[0]}")
                generate_card(f"Investment Type: {df_dim_etf['investment_type'].iloc[0]}")
                generate_card(f"Size Type: {df_dim_etf['size_type'].iloc[0]}")
                # Add more cards or information here as needed

        else:
            st.write("No basic information found for the selected ETF.")

# Main
if __name__ == "__main__":
    display_fund_selection(con)
