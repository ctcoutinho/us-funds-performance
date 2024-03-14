import os
import duckdb
import pandas as pd


def connect_to_db():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the database file relative to the current script
    db_path = os.path.join(current_dir, "..", "us-funds-project.db")
    return duckdb.connect(database=db_path, read_only=True)


def get_etf_facts(con, selected_symbol: str) -> pd.DataFrame:
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


def get_etf_top_10_holdings(con, selected_symbol: str) -> pd.DataFrame:
    """
    Get top 10 holdings about the selected ETF.

    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.

    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_top_10_holdings_query = """
            select
                holding_name as Company,
                (holding_weight * 100) as 'Portfolio Weight in %'
            from "us-funds-project".main_etfs.dim_holdings
            where fund_symbol=?
            order by holding_weight desc
          """

    return con.execute(etf_top_10_holdings_query, (selected_symbol,)).df()


def get_etf_percentage_of_net_assets(con, selected_symbol: str) -> pd.DataFrame:
    """
    Get top 10 holdings about the selected ETF.

    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.

    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_perc_net_assets_query = """
            select
                fund_symbol,
                round((sum(holding_weight) * 100),2) as '% Net assets'
            from "us-funds-project".main_etfs.dim_holdings
            where fund_symbol=?
            group by fund_symbol
          """

    return con.execute(etf_perc_net_assets_query, (selected_symbol,)).df()


def get_etf_sectors(con, selected_symbol: str) -> pd.DataFrame:
    """
    Get sectors about the selected ETF.

    Args:
        con: The database connection object.
        selected_symbol: The symbol for the ETF.

    Returns:
        A DataFrame with the ETF's basic information.
    """
    etf_sectors_query = """
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
