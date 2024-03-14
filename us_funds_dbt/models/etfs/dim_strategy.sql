{{ config(
    materialized='table',
    schema='etfs'
    )
}}


with src_etf as (
    select
        fund_symbol,
        investment_strategy,
        investment_type,
        size_type
    from {{ ref("stg_etf") }}
)

select * from src_etf
