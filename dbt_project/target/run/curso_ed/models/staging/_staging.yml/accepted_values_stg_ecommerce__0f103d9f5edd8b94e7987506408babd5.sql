
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

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



  
  
      
    ) dbt_internal_test