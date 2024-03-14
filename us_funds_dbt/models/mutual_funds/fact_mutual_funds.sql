{{ config(
    materialized='table',
    schema='mutual_funds'
    )
}}

with src_mutual_fund_prices as (
    select
        fund_symbol,
        price_date,
        nav_per_share
    from {{ ref('stg_mutual_funds_prices') }}
),

src_mutual_funds as (
    select
        fund_symbol,
        total_net_assets,
        year_to_date_return,
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
        morningstar_overall_rating,
        morningstar_risk_rating,
        inception_date,
        last_dividend,
        last_cap_gain,
        annual_holdings_turnover,
        fund_annual_report_net_expense_ratio,
        category_annual_report_net_expense_ratio,
        fund_prospectus_net_expense_ratio,
        fund_prospectus_gross_expense_ratio,
        fund_max_12b1_fee,
        fund_max_front_end_sales_load,
        category_max_front_end_sales_load,
        fund_max_deferred_sales_load,
        category_max_deferred_sales_load,
        fund_year3_expense_projection,
        fund_year5_expense_projection,
        fund_year10_expense_projection,
        asset_cash,
        asset_stocks,
        asset_bonds,
        asset_others,
        asset_preferred,
        asset_convertible,
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
        category_price_book_ratio,
        fund_price_cashflow_ratio,
        category_price_cashflow_ratio,
        fund_price_earning_ratio,
        category_price_earning_ratio,
        fund_price_sales_ratio,
        category_price_sales_ratio,
        fund_median_market_cap,
        category_median_market_cap,
        fund_year3_earnings_growth,
        category_year3_earnings_growth,
        fund_bond_maturity,
        category_bond_maturity,
        fund_bond_duration,
        category_bond_duration,
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
        morningstar_return_rating,
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
        fund_return_last_bull_market,
        category_return_last_bull_market,
        fund_return_last_bear_market,
        category_return_last_bear_market,
        years_up,
        years_down,
        fund_return_2020,
        category_return_2020,
        fund_return_2019,
        category_return_2019,
        fund_return_2018,
        category_return_2018,
        fund_return_2017,
        category_return_2017,
        fund_return_2016,
        category_return_2016,
        fund_return_2015,
        category_return_2015,
        fund_return_2014,
        category_return_2014,
        fund_return_2013,
        category_return_2013,
        fund_return_2012,
        category_return_2012,
        fund_return_2011,
        category_return_2011,
        fund_return_2010,
        category_return_2010,
        fund_return_2009,
        category_return_2009,
        fund_return_2008,
        category_return_2008,
        fund_return_2007,
        category_return_2007,
        fund_return_2006,
        category_return_2006,
        fund_return_2005,
        category_return_2005,
        fund_return_2004,
        category_return_2004,
        fund_return_2003,
        category_return_2003,
        fund_return_2002,
        category_return_2002,
        fund_return_2001,
        category_return_2001,
        fund_return_2000,
        category_return_2000,
        quarters_up,
        quarters_down,
        fund_return_2021_q3,
        fund_return_2021_q2,
        fund_return_2021_q1,
        fund_return_2020_q4,
        fund_return_2020_q3,
        fund_return_2020_q2,
        fund_return_2020_q1,
        fund_return_2019_q4,
        fund_return_2019_q3,
        fund_return_2019_q2,
        fund_return_2019_q1,
        fund_return_2018_q4,
        fund_return_2018_q3,
        fund_return_2018_q2,
        fund_return_2018_q1,
        fund_return_2017_q4,
        fund_return_2017_q3,
        fund_return_2017_q2,
        fund_return_2017_q1,
        fund_return_2016_q4,
        fund_return_2016_q3,
        fund_return_2016_q2,
        fund_return_2016_q1,
        fund_return_2015_q4,
        fund_return_2015_q3,
        fund_return_2015_q2,
        fund_return_2015_q1,
        fund_return_2014_q4,
        fund_return_2014_q3,
        fund_return_2014_q2,
        fund_return_2014_q1,
        fund_return_2013_q4,
        fund_return_2013_q3,
        fund_return_2013_q2,
        fund_return_2013_q1,
        fund_return_2012_q4,
        fund_return_2012_q3,
        fund_return_2012_q2,
        fund_return_2012_q1,
        fund_return_2011_q4,
        fund_return_2011_q3,
        fund_return_2011_q2,
        fund_return_2011_q1,
        fund_return_2010_q4,
        fund_return_2010_q3,
        fund_return_2010_q2,
        fund_return_2010_q1,
        fund_return_2009_q4,
        fund_return_2009_q3,
        fund_return_2009_q2,
        fund_return_2009_q1,
        fund_return_2008_q4,
        fund_return_2008_q3,
        fund_return_2008_q2,
        fund_return_2008_q1,
        fund_return_2007_q4,
        fund_return_2007_q3,
        fund_return_2007_q2,
        fund_return_2007_q1,
        fund_return_2006_q4,
        fund_return_2006_q3,
        fund_return_2006_q2,
        fund_return_2006_q1,
        fund_return_2005_q4,
        fund_return_2005_q3,
        fund_return_2005_q2,
        fund_return_2005_q1,
        fund_return_2004_q4,
        fund_return_2004_q3,
        fund_return_2004_q2,
        fund_return_2004_q1,
        fund_return_2003_q4,
        fund_return_2003_q3,
        fund_return_2003_q2,
        fund_return_2003_q1,
        fund_return_2002_q4,
        fund_return_2002_q3,
        fund_return_2002_q2,
        fund_return_2002_q1,
        fund_return_2001_q4,
        fund_return_2001_q3,
        fund_return_2001_q2,
        fund_return_2001_q1,
        fund_return_2000_q4,
        fund_return_2000_q3,
        fund_return_2000_q2,
        fund_return_2000_q1,
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
        fund_treynor_ratio_10years,
        fund_return_category_rank_ytd,
        fund_return_category_rank_1month,
        fund_return_category_rank_3months,
        fund_return_category_rank_1year,
        fund_return_category_rank_3years,
        fund_return_category_rank_5years,
        load_adj_return_1year,
        load_adj_return_3years,
        load_adj_return_5years,
        load_adj_return_10years,
        sustainability_score,
        sustainability_rank,
        esg_peer_group,
        esg_peer_count,
        esg_score,
        peer_esg_min,
        peer_esg_avg,
        peer_esg_max,
        environment_score,
        peer_environment_min,
        peer_environment_avg,
        peer_environment_max,
        social_score,
        peer_social_min,
        peer_social_avg,
        peer_social_max,
        governance_score,
        peer_governance_min,
        peer_governance_avg,
        peer_governance_max
    from {{ ref("stg_mutual_funds") }}
),

__joined as (
    select
        smfp.*,
        smf.*
    from src_mutual_funds as smf
    left join src_mutual_fund_prices as smfp
        on smf.fund_symbol = smfp.fund_symbol
)

select * from __joined