{{ config(
    materialized='table',
    schema='etfs'
    )
}}

with src_etf as (
    select
        fund_symbol,
        quote_type,
        region,
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
    from {{ ref("stg_etf") }}
)

select * from src_etf
