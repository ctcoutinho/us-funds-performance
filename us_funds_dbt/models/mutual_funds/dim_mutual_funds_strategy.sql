{{ config(
    materialized='table',
    schema='mutual_funds'
    )
}}

with stg_mutual_funds as (
    select
        fund_symbol,
        investment_strategy,
        investment_type,
        size_type
    from {{ ref("stg_mutual_funds") }}
)

select * from stg_mutual_funds
