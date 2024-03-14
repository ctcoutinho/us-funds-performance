{{ config(
    materialized='table',
    schema='etfs'
    )
}}

with __src AS (
    select
        fund_symbol,
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
        fund_sector_utilities
    from {{ ref("stg_etf") }}
    group by all
),

__unioned AS (

    select
        fund_symbol,
        'Basic Materials' AS sector,
        fund_sector_basic_materials AS weight
    from __src
    union all
    select
        fund_symbol,
        'Communication Services',
        fund_sector_communication_services
    from __src
    union all
    select
        fund_symbol,
        'Consumer Cyclical',
        fund_sector_consumer_cyclical
    from __src
    union all
    select
        fund_symbol,
        'Consumer Defensive',
        fund_sector_consumer_defensive
    from __src
    union all
    select
        fund_symbol,
        'Energy',
        fund_sector_energy
    from __src
    union all
    select
        fund_symbol,
        'Financial Services',
        fund_sector_financial_services
    from __src
    union all
    select
        fund_symbol,
        'Healthcare',
        fund_sector_healthcare
    from __src
    union all
    select
        fund_symbol,
        'Industrials',
        fund_sector_industrials
    from __src
    union all
    select
        fund_symbol,
        'Real Estate',
        fund_sector_real_estate
    from __src
    union all
    select
        fund_symbol,
        'Technology',
        fund_sector_technology
    from __src
    union all
    select
        fund_symbol,
        'Utilities',
        fund_sector_utilities
    from __src

)

select * from __unioned ORDER BY fund_symbol ASC, weight DESC
