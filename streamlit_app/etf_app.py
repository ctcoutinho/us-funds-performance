import streamlit as st
import os
import duckdb
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime
from utils import (
    config_menu_footer,
    generate_card,
    generate_long_text,
    generate_investment_profile,
    create_donut_chart,
    create_candlestick_chart,
    create_volume_chart,
    empty_lines,
    get_delta,
    color_highlighter,
)
from queries import (
    connect_to_db,
    get_etf_top_10_holdings,
    get_min_max_dates_by_fund,
    get_etf_basic_info,
    get_etf_sectors,
    get_etf_facts,
    get_etf_percentage_of_net_assets,
)

# Streamlit page configuration
st.set_page_config(layout="wide")
st.title("📈 US-funds stats | Streamlit")

con = connect_to_db()

def display_fund_selection(con):
    """Display UI elements for fund selection and details.

    Args:
        con: The database connection object.
    """
    df_funds_dates = get_min_max_dates_by_fund(con)

    if not df_funds_dates.empty:

        sorted_symbols = df_funds_dates["fund_symbol"].sort_values()

        selected_symbol = st.sidebar.selectbox("Fund Symbol", sorted_symbols)
        if selected_symbol:  # Ensure selected_symbol is not None or empty
            show_fund_details(con, selected_symbol)
    else:
        st.write("No funds found.")


def show_fund_details(con, selected_symbol: str):
    # Fetch the min and max dates for the selected symbol directly within this function
    df_funds_dates = get_min_max_dates_by_fund(con)
    selected_fund_data = df_funds_dates[
        df_funds_dates["fund_symbol"] == selected_symbol
    ]

    if not selected_fund_data.empty:
        min_date, max_date = pd.to_datetime(
            selected_fund_data["min_date"].iloc[0]
        ), pd.to_datetime(selected_fund_data["max_date"].iloc[0])

        # Use a try-except block or check the length of the returned value to handle the case where an end date isn't specified
        date_selection = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

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
        df_percentage_of_net_assets = get_etf_percentage_of_net_assets(
            con, selected_symbol
        )
        df_fact_etf = get_etf_facts(con, selected_symbol)
        df_fact_etf["total_net_assets"] = df_fact_etf["total_net_assets"].apply(
            lambda x: "${:,.2f}".format(x)
        )
        df_fact_etf["inception_date"] = pd.to_datetime(
            df_fact_etf["inception_date"]
        ).dt.date
        df_fact_etf["price_date"] = pd.to_datetime(df_fact_etf["price_date"])
        df_valuation_ratios = df_fact_etf[
            [
                "fund_price_book_ratio",
                "fund_price_cashflow_ratio",
                "fund_price_earning_ratio",
                "fund_price_sales_ratio",
            ]
        ]
        df_valuation_ratios = df_valuation_ratios.drop_duplicates()
        df_risk_metrics = df_fact_etf[
            [
                "fund_alpha_3years",
                "fund_beta_3years",
                "fund_mean_annual_return_3years",
                "fund_r_squared_3years",
                "fund_stdev_3years",
                "fund_sharpe_ratio_3years",
                "fund_treynor_ratio_3years",
                "fund_alpha_5years",
                "fund_beta_5years",
                "fund_mean_annual_return_5years",
                "fund_r_squared_5years",
                "fund_stdev_5years",
                "fund_sharpe_ratio_5years",
                "fund_treynor_ratio_5years",
                "fund_alpha_10years",
                "fund_beta_10years",
                "fund_mean_annual_return_10years",
                "fund_r_squared_10years",
                "fund_stdev_10years",
                "fund_sharpe_ratio_10years",
                "fund_treynor_ratio_10years",
            ]
        ]
        df_risk_metrics = df_risk_metrics.drop_duplicates()
        df_risk_metrics = df_risk_metrics.melt(var_name="Metric", value_name="Value")
        if not df_dim_etf.empty:
            st.subheader("Selected Fund")
            generate_card(f"{selected_symbol}")
            st.text(
                f"For {selected_symbol}, we can provide data between the {min_date.date()} and {max_date.date()}"
            )

            ##         Profile and Investment
            st.header("Profile and Investment")

            generate_investment_profile(
                fund_long_name=f"{df_dim_etf['fund_long_name'].iloc[0]}",
                fund_category=f"{df_dim_etf['fund_category'].iloc[0]}",
                fund_family=f"{df_dim_etf['fund_family'].iloc[0]}",
                currency=f"{df_dim_etf['currency'].iloc[0]}",
                exchange_name=f"{df_dim_etf['exchange_name'].iloc[0]}",
                exchange_code=f"{df_dim_etf['exchange_code'].iloc[0]}",
                region=f"US",
                inception_date=f"{df_fact_etf['inception_date'].iloc[0]}",
                total_net_assets=f"{df_fact_etf['total_net_assets'].iloc[0]}",
            )
            ###         Investment strategy
            st.subheader("Investment strategy")
            generate_long_text(
                f"Investment Strategy: {df_dim_etf['investment_strategy'].iloc[0]}"
            )

            st.header("Valuation and Quality Metrics")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 10 Holdings")
                st.dataframe(df_top_10_holdings, hide_index=True)

            with col2:
                st.subheader("Portfolio Weight by Company")
                fig = create_donut_chart(
                    labels=df_top_10_holdings["Company"],
                    values=df_top_10_holdings["Portfolio Weight in %"],
                    hole_size=0.4,  # Example of customizing the hole size
                    title_text=f"Top 10 holdings as % of portfolio : {df_percentage_of_net_assets['% Net assets'].iloc[0]} % Net assets",
                )

                # Display donut chart
                st.plotly_chart(fig)

            st.subheader("Valuation Ratio")
            st.dataframe(
                df_valuation_ratios,
                column_config={
                    "fund_price_book_ratio": "Fund Price/Book Ratio",
                    "fund_price_cashflow_ratio": "Fund Price/Cashflow Ratio",
                    "fund_price_earning_ratio": "Fund Price/Earning Ratio",
                    "fund_price_sales_ratio": "Fund Price/Sales Ratio",
                },
                hide_index=True,
            )
            st.subheader("Sector Allocation")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Sectors")
                st.dataframe(df_sectors, hide_index=True)

            with col2:
                fig = create_donut_chart(
                    labels=df_sectors["sector"],
                    values=df_sectors["Weight in %"],
                    hole_size=0.4,  # Example of customizing the hole size
                    title_text=f"",
                )
                # Display donut chart
                st.plotly_chart(fig)

            st.header("Risk Metrics")
            st.dataframe(
                df_risk_metrics,
                column_config={
                    "fund_alpha_3years": "Alpha 3years",
                    "fund_beta_3years": "Beta 3years",
                    "fund_mean_annual_return_3years": "Mean Annual Return 3years",
                    "fund_r_squared_3years": "R Squared 3years",
                    "fund_stdev_3years": "Standard Deviation 3years",
                    "fund_sharpe_ratio_3years": "Sharpe Ratio 3years",
                    "fund_treynor_ratio_3years": "Treynor Ratio 3years",
                    "fund_alpha_5years": "Alpha 5years",
                    "fund_beta_5years": "Beta 5years",
                    "fund_mean_annual_return_5years": "Mean Annual Return 5years",
                    "fund_r_squared_5years": "R Squared 5years",
                    "fund_stdev_5years": "Standard Deviation 5years",
                    "fund_sharpe_ratio_5years": "Sharpe Ratio 5years",
                    "fund_treynor_ratio_5years": "Treynor Ratio 5years",
                    "fund_alpha_10years": "Alpha 10years",
                    "fund_beta_10years": "Beta 10years",
                    "fund_mean_annual_return_10years": "Mean Annual Return 10years",
                    "fund_r_squared_10years": "R Squared 10years",
                    "fund_stdev_10years": "Standard Deviation 10years",
                    "fund_sharpe_ratio_10years": "Sharpe Ratio 10years",
                    "fund_treynor_ratio_10years": "Treynor Ratio 10years",
                },
                hide_index=True,
                height=780,
            )
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
