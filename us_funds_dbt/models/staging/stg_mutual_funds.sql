{{ config(materialized='table') }}

select * from {{ source('us-funds', 'mutual_funds') }}