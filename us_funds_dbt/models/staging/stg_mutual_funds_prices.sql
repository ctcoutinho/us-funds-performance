{{ config(
    materialized='table',
    partition_by=['fund_symbol','price_date_year']
    ) }}

select
    *,
    extract('year' from price_date) as price_date_year
from {{ source('us-funds', 'mutual_fund_prices') }}