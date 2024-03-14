{{ config(
    materialized='table',
    schema='etfs'
    )
}}

with src_etf as (
    select
        fund_symbol,
        top10_holdings
    from {{ ref("stg_etf") }}
),

split_varchar as (
    select
        fund_symbol,
        SPLIT(top10_holdings, ',') as holdings_array
    from src_etf
),

__unnesting as (
    select
        fund_symbol,
        TRIM(SPLIT_PART(holding, ':', 1)) as holding_name,
        TRIM(SPLIT_PART(holding, ':', 2)) as holding_weight
    from split_varchar, UNNEST(split_varchar.holdings_array) as t (holding)
),

__cleaned as (
    select
        fund_symbol,
        TRIM(REPLACE(holding_name, '"', '')) as holding_name,
        TRY_CAST(holding_weight as double) as holding_weight
    from __unnesting
)

select * from __cleaned
