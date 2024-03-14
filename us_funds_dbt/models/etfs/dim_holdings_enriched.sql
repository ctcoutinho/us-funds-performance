{{ config(
    materialized='table',
    schema='etfs'
    )
}}

with __dim_holdings as (
    select * from {{ ref("dim_holdings") }}
),

__aggregated as (
    select
        fund_symbol,
        100 - (sum(holding_weight) * 100) as "Remaining Assets"
    from {{ ref("dim_holdings") }}
    group by fund_symbol
),

__unioned as (
    select
        fund_symbol,
        'Remaining Assets' as holding_name,
        "Remaining Assets" as holding_weight
    from __aggregated
    union all
    select
        fund_symbol,
        holding_name,
        holding_weight
    from __dim_holdings
)

select * from __unioned
order by fund_symbol asc, holding_weight desc
