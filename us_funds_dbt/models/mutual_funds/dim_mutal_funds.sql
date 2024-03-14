{{ config(
    materialized='table',
    schema='mutual_funds'
    )
}}

with src_mutual_funds as (
    select
        fund_symbol,
        quote_type,
        region,
        fund_short_name,
        fund_long_name,
        currency,
        subsequent_investment,
        fund_category,
        fund_family,
        exchange_code,
        exchange_name,
        exchange_timezone,
        management_name,
        management_bio,
        management_start_date,
        investment_strategy,
        investment_type
    from {{ ref("stg_mutual_funds") }}
)

select * from src_mutual_funds
