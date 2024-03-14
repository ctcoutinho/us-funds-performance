{{ config(materialized='table') }}

select * from {{ source('us-funds', 'etfs_prices') }}