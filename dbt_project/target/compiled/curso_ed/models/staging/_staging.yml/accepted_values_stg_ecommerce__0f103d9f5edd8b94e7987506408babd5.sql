
    
    

with all_values as (

    select
        status_pedido as value_field,
        count(*) as n_records

    from "lakehouse"."staging"."stg_ecommerce__pedidos"
    group by status_pedido

)

select *
from all_values
where value_field not in (
    'faturado','cancelado','em_aberto','estornado'
)


