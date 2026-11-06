
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        segmento_cliente as value_field,
        count(*) as n_records

    from "lakehouse"."intermediate"."int_clientes__metricas"
    group by segmento_cliente

)

select *
from all_values
where value_field not in (
    'vip','alto_valor','em_risco','regular'
)



  
  
      
    ) dbt_internal_test