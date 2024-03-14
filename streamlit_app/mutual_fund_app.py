import streamlit as st
import os
import duckdb
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
from utils import (
    config_menu_footer, generate_card, generate_long_text,generate_investment_profile,create_donut_chart,create_candlestick_chart, create_volume_chart,empty_lines, get_delta, color_highlighter
)


def connect_to_db():
    # Get the current script directory 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the database file relative to the current script
    db_path = os.path.join(current_dir, '..', 'us-funds-project.db')
    return duckdb.connect(database=db_path, read_only=True)

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
                fund_symbol,
                price_date,
                open,
                high,
                low,
                close,
                adj_close,
                volume,
                avg_vol_3month,
                avg_vol_10day,
                total_net_assets,
                day50_moving_average,
                day200_moving_average,
                week52_high_low_change,
                week52_high_low_change_perc,
                week52_high,
                week52_high_change,
                week52_high_change_perc,
                week52_low,
                week52_low_change,
                week52_low_change_perc,
                fund_yield,
                inception_date,
                annual_holdings_turnover,
                fund_annual_report_net_expense_ratio,
                category_annual_report_net_expense_ratio,
                asset_stocks,
                asset_bonds,
                fund_sector_basic_materials,
                fund_sector_communication_services,
                fund_sector_consumer_cyclical,
                fund_sector_consumer_defensive,
                fund_sector_energy,
                fund_sector_financial_services,
                fund_sector_healthcare,
                fund_sector_industrials,
                fund_sector_real_estate,
                fund_sector_technology,
                fund_sector_utilities,
                fund_price_book_ratio,
                fund_price_cashflow_ratio,
                fund_price_earning_ratio,
                fund_price_sales_ratio,
                fund_bond_maturity,
                fund_bond_duration,
                fund_bonds_us_government,
                fund_bonds_aaa,
                fund_bonds_aa,
                fund_bonds_a,
                fund_bonds_bbb,
                fund_bonds_bb,
                fund_bonds_b,
                fund_bonds_below_b,
                fund_bonds_others,
                top10_holdings_total_assets,
                returns_as_of_date,
                fund_return_ytd,
                category_return_ytd,
                fund_return_1month,
                category_return_1month,
                fund_return_3months,
                category_return_3months,
                fund_return_1year,
                category_return_1year,
                fund_return_3years,
                category_return_3years,
                fund_return_5years,
                category_return_5years,
                fund_return_10years,
                category_return_10years,
                years_up,
                years_down,
                fund_alpha_3years,
                fund_beta_3years,
                fund_mean_annual_return_3years,
                fund_r_squared_3years,
                fund_stdev_3years,
                fund_sharpe_ratio_3years,
                fund_treynor_ratio_3years,
                fund_alpha_5years,
                fund_beta_5years,
                fund_mean_annual_return_5years,
                fund_r_squared_5years,
                fund_stdev_5years,
                fund_sharpe_ratio_5years,
                fund_treynor_ratio_5years,
                fund_alpha_10years,
                fund_beta_10years,
                fund_mean_annual_return_10years,
                fund_r_squared_10years,
                fund_stdev_10years,
                fund_sharpe_ratio_10years,
                fund_treynor_ratio_10years
              FROM "us-funds-project".main_etfs.fact_etfs
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
                round((sum(holding_weight) * 100),2) as '% Net assets'
            from "us-funds-project".main_etfs.dim_holdings
            where fund_symbol=?
            group by fund_symbol
          """

    return con.execute(etf_perc_net_assets_query, (selected_symbol,)).df()

def get_etf_sectors (con, selected_symbol: str) -> pd.DataFrame:
    """
    Get sectors about the selected ETF.
    
    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.
        
    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_sectors_query ="""
            select
                sector,
                (weight * 100) as 'Weight in %'
            from "us-funds-project".main_etfs.dim_sectors
            where fund_symbol=?
            order by weight desc
          """
    
    return con.execute(etf_sectors_query, (selected_symbol,)).df()

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
        df_sectors = get_etf_sectors(con, selected_symbol)
        df_percentage_of_net_assets = get_etf_percentage_of_net_assets(con, selected_symbol)
        df_fact_etf = get_etf_facts(con,selected_symbol)
        df_fact_etf['total_net_assets'] = df_fact_etf['total_net_assets'].apply(lambda x: "${:,.2f}".format(x))
        df_fact_etf['inception_date'] = pd.to_datetime(df_fact_etf['inception_date']).dt.date
        df_fact_etf['price_date'] = pd.to_datetime(df_fact_etf['price_date'])
        df_valuation_ratios = df_fact_etf[['fund_price_book_ratio','fund_price_cashflow_ratio','fund_price_earning_ratio','fund_price_sales_ratio']]
        df_valuation_ratios = df_valuation_ratios.drop_duplicates()
        if not df_dim_etf.empty:
            st.subheader("Selected Fund")
            generate_card(f"{selected_symbol}")
            st.text(f"For {selected_symbol}, we can provide data between the {min_date.date()} and {max_date.date()}")


##         Profile and Investment
            st.header("Profile and Investment")

            generate_investment_profile(fund_long_name = f"{df_dim_etf['fund_long_name'].iloc[0]}",
                                        fund_category=f"{df_dim_etf['fund_category'].iloc[0]}",
                                        fund_family= f"{df_dim_etf['fund_family'].iloc[0]}",
                                        currency=f"{df_dim_etf['currency'].iloc[0]}",
                                        exchange_name = f"{df_dim_etf['exchange_name'].iloc[0]}",
                                        exchange_code = f"{df_dim_etf['exchange_code'].iloc[0]}",
                                        region = f"US",
                                        inception_date = f"{df_fact_etf['inception_date'].iloc[0]}",
                                        total_net_assets = f"{df_fact_etf['total_net_assets'].iloc[0]}"
                                        )
###         Investment strategy            
            st.subheader("Investment strategy")
            generate_long_text(f"Investment Strategy: {df_dim_etf['investment_strategy'].iloc[0]}")

            st.header("Valuation and Quality Metrics")
            col1, col2 = st.columns(2)
            with col1:  
                st.subheader("Top 10 Holdings")
                st.dataframe(df_top_10_holdings,hide_index=True)

            with col2:
                st.subheader("Portfolio Weight by Company")
                fig = create_donut_chart(
                labels=df_top_10_holdings['Company'],
                values=df_top_10_holdings['Portfolio Weight in %'],
                hole_size=0.4,  # Example of customizing the hole size
                title_text=f"Top 10 holdings as % of portfolio : {df_percentage_of_net_assets['% Net assets'].iloc[0]} % Net assets"
                )

                # Display donut chart
                st.plotly_chart(fig)

            st.subheader("Valuation Ratio")
            st.dataframe( df_valuation_ratios, column_config = {"fund_price_book_ratio" : "Fund Price/Book Ratio",
                                                            "fund_price_cashflow_ratio":"Fund Price/Cashflow Ratio",
                                                            "fund_price_earning_ratio":"Fund Price/Earning Ratio",
                                                            "fund_price_sales_ratio":"Fund Price/Sales Ratio",
                                                            },hide_index=True)
            st.subheader("Sector Allocation")
            fig = create_donut_chart(
            labels=df_sectors['sector'],
            values=df_sectors['Weight in %'],
            hole_size=0.4,  # Example of customizing the hole size
            title_text=f""
            )

            # Display donut chart
            st.plotly_chart(fig)

            st.header("Risk Metrics")

            st.header("Price & Volume data")
            # Generate and display the candlestick chart
            fig = create_candlestick_chart(df_fact_etf)
            st.plotly_chart(fig)
            # Generate and display the volume chart
            volume_fig = create_volume_chart(df_fact_etf)
            st.plotly_chart(volume_fig)
            
        else:
            st.write("No basic information found for the selected ETF.")

# Main
if __name__ == "__main__":
    display_fund_selection(con)
